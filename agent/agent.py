"""Pitch Deck Generator - Google ADK Sequential Agent Workflow.

This module implements a multi-agent pipeline for generating sales pitch decks:
1. Strategist Agent: Analyzes offers → Creates a multi-slide deck structure
2. Art Director Agent: Takes deck structure → Generates Nano Banana image prompts
3. Image Generator Agent: Takes prompts → Generates actual slide images

Usage:
    adk web  # Start the ADK web interface
    adk run agent  # Run the agent from command line
"""

from google.adk.agents import SequentialAgent

from .agents import strategist_agent, art_director_agent, image_generator_agent


# The main sequential agent that orchestrates the pitch deck generation workflow
# Execution order: strategist_agent → art_director_agent → image_generator_agent
root_agent = SequentialAgent(
    name='pitch_deck_generator',
    description=(
        'A sequential workflow that generates professional sales pitch decks. '
        'First, the Strategist creates a multi-slide narrative structure. '
        'Then, the Art Director converts each slide into Nano Banana image prompts. '
        'Finally, the Image Generator creates actual slide images using Gemini 3 Pro.'
    ),
    sub_agents=[
        strategist_agent,       # Step 1: Analyze offer → Create deck plan
        art_director_agent,     # Step 2: Deck plan → Visual prompts
        image_generator_agent,  # Step 3: Visual prompts → Generated images
    ],
)
