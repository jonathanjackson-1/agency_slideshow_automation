"""The Image Generator Agent - Generates slide images using Gemini 3 Pro Image Preview.

This agent takes the visual prompts from the Art Director and generates
actual images for each slide using the gemini-3-pro-image-preview model.
"""

import os
import base64
from datetime import datetime
from typing import Optional

from google import genai
from google.genai import types
from google.adk.tools import FunctionTool


# Default output directory for generated slides
DEFAULT_OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "public", "slides")


def get_output_directory(base_dir: Optional[str] = None) -> str:
    """Get or create a timestamped output directory for slides.
    
    Args:
        base_dir: Base directory for output. Defaults to agent/public/slides/
    
    Returns:
        Path to the output directory with timestamp subfolder.
    """
    if base_dir is None:
        base_dir = DEFAULT_OUTPUT_DIR
    
    # Create timestamp-based subfolder (e.g., "2024-12-11_020000")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    output_path = os.path.join(base_dir, timestamp)
    
    os.makedirs(output_path, exist_ok=True)
    return output_path


def generate_slide_image(
    prompt: str,
    slide_number: int,
    output_dir: Optional[str] = None
) -> dict:
    """Generate an image for a slide using Gemini 3 Pro Image Preview.
    
    Args:
        prompt: The Nano Banana-style prompt for image generation.
        slide_number: The slide number (1-9) for naming the output file.
        output_dir: Optional directory to save images. Defaults to public/slides/<timestamp>/
    
    Returns:
        dict with:
            - success: bool indicating if generation succeeded
            - image_path: path to the saved image file
            - error: error message if generation failed
    """
    try:
        # Initialize the Genai client
        client = genai.Client()
        
        # Generate the image
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=[prompt],
            config=types.GenerateContentConfig(
                image_config=types.ImageConfig(
                    aspect_ratio="16:9",
                    image_size="2K",
                )
            )
        )
        
        # Process the response
        if response.candidates and len(response.candidates) > 0:
            candidate = response.candidates[0]
            
            # Look for image parts in the response
            for part in candidate.content.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    # Extract image data
                    image_data = part.inline_data.data
                    mime_type = part.inline_data.mime_type
                    
                    # Determine file extension
                    ext = 'png'
                    if 'jpeg' in mime_type or 'jpg' in mime_type:
                        ext = 'jpg'
                    elif 'webp' in mime_type:
                        ext = 'webp'
                    
                    # Use default output path if not specified
                    if output_dir is None:
                        output_dir = get_output_directory()
                    else:
                        os.makedirs(output_dir, exist_ok=True)
                    
                    image_path = os.path.join(output_dir, f"slide_{slide_number:02d}.{ext}")
                    
                    # Save the image
                    with open(image_path, 'wb') as f:
                        if isinstance(image_data, str):
                            f.write(base64.b64decode(image_data))
                        else:
                            f.write(image_data)
                    
                    return {
                        "success": True,
                        "image_path": image_path,
                        "error": None
                    }
        
        return {
            "success": False,
            "image_path": None,
            "error": "No image data found in response"
        }
        
    except Exception as e:
        return {
            "success": False,
            "image_path": None,
            "error": str(e)
        }


def generate_all_slides(
    prompts: list[dict],
    output_dir: Optional[str] = None
) -> dict:
    """Generate images for all slides in the deck.
    
    Args:
        prompts: List of dicts with 'slide_number' and 'prompt' keys.
        output_dir: Optional directory to save images. Defaults to public/slides/<timestamp>/
    
    Returns:
        dict with:
            - success: bool indicating if all generations succeeded
            - images: list of generated image paths
            - output_directory: path to the folder containing all slides
            - errors: list of any errors encountered
    """
    # Create a shared output directory for all slides in this batch
    if output_dir is None:
        output_dir = get_output_directory()
    else:
        os.makedirs(output_dir, exist_ok=True)
    
    results = {
        "success": True,
        "images": [],
        "output_directory": output_dir,
        "errors": []
    }
    
    for item in prompts:
        slide_num = item.get("slide_number", 1)
        prompt = item.get("prompt", "")
        
        result = generate_slide_image(prompt, slide_num, output_dir)
        
        if result["success"]:
            results["images"].append(result["image_path"])
        else:
            results["success"] = False
            results["errors"].append(f"Slide {slide_num}: {result['error']}")
    
    return results


# Create ADK FunctionTools
generate_slide_tool = FunctionTool(func=generate_slide_image)
generate_all_slides_tool = FunctionTool(func=generate_all_slides)

