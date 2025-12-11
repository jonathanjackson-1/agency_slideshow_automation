"""Pydantic schemas for pitch deck generation workflow.

These models define the structured data passed between agents in the sequential workflow.
"""

from typing import List
from pydantic import BaseModel, Field


class SlidePlan(BaseModel):
    """Represents a single slide in the pitch deck.
    
    Attributes:
        slide_number: The position of this slide in the deck (1-9).
        title: The headline/title of the slide.
        body_content: Bullet points or key messages for the slide.
        visual_concept: Description of the visual element for this slide.
    """
    slide_number: int = Field(..., ge=1, le=9, description="Slide position (1-9)")
    title: str = Field(..., description="The headline/title of the slide")
    body_content: List[str] = Field(
        default_factory=list,
        description="Bullet points or key messages"
    )
    visual_concept: str = Field(
        ..., 
        description="Description of the visual element (e.g., 'A minimal graph showing 30% growth')"
    )


class DeckPlan(BaseModel):
    """Complete pitch deck structure with all slides.
    
    The deck follows a multi-slide sales narrative structure:
    1. Problem
    2. Agitation  
    3. Solution
    4. Case Study
    5. Offer
    6. Pricing
    7. CTA (Call to Action)
    """
    slides: List[SlidePlan] = Field(
        ..., 
        min_length=6, 
        max_length=9,
        description="List of 6-9 slide plans following the sales narrative"
    )
    offer_summary: str = Field(
        ..., 
        description="Brief summary of the agency offer being pitched"
    )


class NanoBananaPrompt(BaseModel):
    """Image generation prompt optimized for Nano Banana model.
    
    Contains the formatted prompt with all required specifications for
    high-quality presentation slide rendering.
    """
    slide_number: int = Field(..., ge=1, le=7, description="Corresponding slide number")
    prompt: str = Field(
        ..., 
        description="Full image generation prompt with text rendering specs"
    )
    
    @property
    def formatted_prompt(self) -> str:
        """Returns the prompt with required Nano Banana specifications appended."""
        specs = "High readability text. Professional presentation layout. Aspect ratio 16:9. High fidelity, 4k, clear text rendering."
        return f"{self.prompt} {specs}"


class VisualPromptSet(BaseModel):
    """Collection of all Nano Banana prompts for the complete deck."""
    prompts: List[NanoBananaPrompt] = Field(
        ...,
        min_length=6,
        max_length=9,
        description="List of 6-9 image generation prompts"
    )
