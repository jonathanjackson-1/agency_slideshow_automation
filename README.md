# 🎨 Pitch Deck Generator Agent

A **Google ADK Sequential Agent** workflow that automates the creation of professional sales pitch decks. Feed it your agency offer document, and it generates fully-rendered presentation slides using AI.

## 🚀 Overview

This agent pipeline transforms agency offers (text or DOCX files) into polished pitch deck images through a three-stage AI workflow:

```
┌─────────────────┐    ┌──────────────────┐    ┌────────────────────┐
│   Strategist    │───▶│   Art Director   │───▶│  Image Generator   │
│     Agent       │    │      Agent       │    │       Agent        │
└─────────────────┘    └──────────────────┘    └────────────────────┘
    ▲                        │                         │
    │                        │                         │
  Input:                  Creates:                 Generates:
  Offer Doc             Nano Banana               Slide Images
  (.docx/text)          Prompts                   (16:9, 2K)
```

## ⚙️ How It Works

### Agent 1: The Strategist 🎯

**Role**: Sales Director

The Strategist analyzes your agency offer and creates a structured 6-9 slide sales narrative following the proven copywriting framework:

| Slide | Purpose |
|-------|---------|
| **Problem** | Identify the pain point your target audience faces |
| **Agitation** | Amplify the problem, show the cost of inaction |
| **Solution** | Present your agency's approach as the answer |
| **Case Study** | Provide social proof with results and metrics |
| **Offer** | Detail what's included in the service package |
| **Pricing** | Present pricing tiers or investment levels |
| **CTA** | Clear call to action with next steps |

**Output**: A structured `deck_plan` with titles, bullet points, and visual concepts for each slide.

---

### Agent 2: The Art Director 🎨

**Role**: Visual Prompt Engineer

The Art Director translates the deck plan into detailed **Nano Banana image generation prompts**. Each prompt includes:

- Layout specifications (element positioning)
- Background styles (gradients, colors)
- Exact text to render (titles, bullet points)
- Visual elements (charts, icons, imagery)
- Technical specifications for high-quality output

**Output**: A `visual_prompts` list with optimized prompts for each slide.

---

### Agent 3: The Image Generator 🖼️

**Role**: Render Engine

The Image Generator takes each visual prompt and creates actual images using **Gemini 3 Pro Image Preview**. Images are:

- 16:9 aspect ratio (presentation-ready)
- 2K resolution
- Saved to `agent/public/slides/<timestamp>/`
- Named sequentially: `slide_01.png`, `slide_02.png`, etc.

**Output**: Generated images stored in `generated_images` session state.

---

## 📦 Installation

### Prerequisites

- Python 3.10+
- Google ADK CLI installed
- Google Cloud project with Gemini API access

### Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd agency_slideshow_automation
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # macOS/Linux
   # or
   .venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install google-adk google-genai python-docx pydantic
   ```

4. **Configure environment variables**
   
   Create a `.env` file in the `agent/` directory:
   ```bash
   cd agent
   cp .env.example .env  # or create manually
   ```
   
   Add your Google API credentials:
   ```env
   GOOGLE_API_KEY=your_api_key_here
   # or use Application Default Credentials
   GOOGLE_CLOUD_PROJECT=your_project_id
   ```

---

## 🏃 Running the Agent

### Option 1: ADK Web Interface (Recommended)

Start the interactive web UI:

```bash
cd agent
adk web
```

Then open your browser to the displayed URL (typically `http://localhost:8000`).

### Option 2: ADK CLI

Run the agent directly from command line:

```bash
cd agent
adk run agent
```

### Option 3: Python Script

Use the agent programmatically:

```python
from agent import root_agent

# Run the agent with your offer
result = root_agent.run(
    "Create a pitch deck for my SEO agency. We offer: "
    "- Technical SEO audits "
    "- Content strategy "
    "- Link building "
    "Pricing: $2,500/month"
)
```

---

## 📝 Usage Examples

### From Text Input

Simply describe your agency offer to the agent and/or input your offer document (pdf only):

```
Create a pitch deck for my social media marketing agency.

We help e-commerce brands scale their Instagram and TikTok presence.

Services:
- Content creation (30 posts/month)
- Community management
- Influencer partnerships
- Analytics reporting

Pricing starts at $3,000/month.
```

### From DOCX File

Provide the path to your offer document:

```
Create a pitch deck from /path/to/my-agency-offer.docx
```

The Strategist agent will automatically call the `read_docx_text` tool to extract the content.

---

## 📁 Project Structure

```
agency_slideshow_automation/
├── agent/
│   ├── __init__.py          # Package root, exports root_agent
│   ├── agent.py              # Main SequentialAgent definition
│   ├── .env                  # Environment variables (not in git)
│   ├── .gitignore
│   │
│   ├── agents/               # Sub-agent definitions
│   │   ├── __init__.py
│   │   ├── strategist.py     # Agent 1: Sales narrative planning
│   │   ├── art_director.py   # Agent 2: Visual prompt generation
│   │   └── image_generator.py # Agent 3: Image rendering
│   │
│   ├── models/               # Pydantic schemas
│   │   ├── __init__.py
│   │   └── schemas.py        # SlidePlan, DeckPlan, NanoBananaPrompt
│   │
│   ├── tools/                # ADK FunctionTools
│   │   ├── __init__.py
│   │   ├── document_tools.py # DOCX reading and conversion
│   │   └── image_generator.py # Gemini 3 image generation
│   │
│   └── public/
│       └── slides/           # Generated slide images output
│           └── <timestamp>/  # Each run creates a timestamped folder
│               ├── slide_01.png
│               ├── slide_02.png
│               └── ...
```

---

## 🔧 Configuration

### Agent Models

Each agent uses a specific Gemini model:

| Agent | Model | Purpose |
|-------|-------|---------|
| Strategist | `gemini-2.0-flash` | Fast text generation |
| Art Director | `gemini-2.5-flash` | Complex prompt engineering |
| Image Generator (orchestration) | `gemini-2.5-flash` | Tool coordination |
| Image Generation (rendering) | `gemini-3-pro-image-preview` | Actual image creation |

### Image Output Settings

Default image configuration in `tools/image_generator.py`:

```python
types.ImageConfig(
    aspect_ratio="16:9",
    image_size="2K",
)
```

---

## 🛠️ Available Tools

### Document Tools

| Tool | Function | Description |
|------|----------|-------------|
| `read_docx_tool` | `read_docx_text()` | Extract text from DOCX files |
| `docx_to_pdf_tool` | `convert_docx_to_pdf()` | Convert DOCX to PDF |

### Image Tools

| Tool | Function | Description |
|------|----------|-------------|
| `generate_slide_tool` | `generate_slide_image()` | Generate a single slide image |
| `generate_all_slides_tool` | `generate_all_slides()` | Batch generate all slides |

---

## 📊 Output Format

### Deck Plan (from Strategist)

```json
{
  "slides": [
    {
      "slide_number": 1,
      "title": "Your Organic Traffic Is Stagnant",
      "body_content": [
        "90% of web pages get zero Google traffic",
        "Your competitors are stealing market share"
      ],
      "visual_concept": "A flat line graph with competitor lines trending up"
    }
  ],
  "offer_summary": "SEO and content marketing agency services"
}
```

### Visual Prompts (from Art Director)

```json
{
  "prompts": [
    {
      "slide_number": 1,
      "prompt": "A professional presentation slide with title 'Organic Growth Strategy'. Dark navy gradient background. Bulleted list on left: '- SEO Optimization', '- Content Marketing'. Glowing upward chart on right. High readability text. Professional presentation layout. Aspect ratio 16:9. High fidelity, 4k, clear text rendering."
    }
  ]
}
```

---

## ⚠️ Troubleshooting

### DOCX Files Not Reading

Make sure `python-docx` is installed:
```bash
pip install python-docx
```

### Image Generation Fails

1. Verify your Google API key has access to `gemini-3-pro-image-preview`
2. Check your quota limits in Google Cloud Console
3. Ensure the output directory is writable

### Agent Not Found

Run the agent from inside the `agent/` directory:
```bash
cd agent
adk web
```

---
