"""Tools for context ingestion and document processing."""

from .document_tools import (
    docx_to_pdf_tool,
    read_docx_tool,
    convert_docx_to_pdf,
    read_docx_text,
)

from .image_generator import (
    generate_slide_tool,
    generate_all_slides_tool,
    generate_slide_image,
    generate_all_slides,
)

__all__ = [
    "docx_to_pdf_tool",
    "read_docx_tool",
    "convert_docx_to_pdf",
    "read_docx_text",
    "generate_slide_tool",
    "generate_all_slides_tool",
    "generate_slide_image",
    "generate_all_slides",
]
