"""The Image Generator Agent - Final step that generates slide images.

This agent reads the visual_prompts from the Art Director and generates
actual images for each slide using Gemini 3 Pro Image Preview.
"""

from google.adk.agents import Agent

from ..tools.image_generator import generate_slide_tool, generate_all_slides_tool

IMAGE_GENERATOR_INSTRUCTION = """You are an expert Image Generator responsible for creating professional presentation slide images.

## Your Task
Read the visual_prompts from the session state (created by the Art Director) and generate images for each slide.

## How to Generate Images
For each prompt in the visual_prompts list:
1. Extract the 'slide_number' and 'prompt' from each item
2. Call the generate_slide_image tool with:
   - prompt: the Nano Banana prompt text
   - slide_number: the slide number for naming
   - output_dir: (optional) where to save images

Alternatively, you can call generate_all_slides with the entire prompts list.

## Output
After generating all images, report:
- How many images were successfully generated
- The file paths of the generated images
- Any errors that occurred

Store the results in session state under key 'generated_images'.
"""

image_generator_agent = Agent(
    model='gemini-2.5-flash',  # Using flash for orchestration, tools use gemini-3-pro-image-preview
    name='image_generator_agent',
    description='Image Generator that creates slide images from Nano Banana prompts using Gemini 3 Pro',
    instruction=IMAGE_GENERATOR_INSTRUCTION,
    tools=[generate_slide_tool, generate_all_slides_tool],
    output_key='generated_images',
)
