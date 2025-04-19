import re
import base64
from typing import List,Dict,Any
from io import BytesIO
from PIL import Image
from pathlib import Path
from pdf2image import convert_from_path


PROMPT_TEXT: str = (
    "Convert image to a clean HTML with inline or embedded CSS code. "
    "Preserve the original layout, font sizes, positions, and formatting as accurately as possible. "
    "For tabular data, use <table>, <thead>, <tbody>, <tr>, <th>, and <td> with correct rowspan/colspan to reflect merged cells. "
    "Ensure the final HTML visually matches the original layout of the image, with consistent spacing, alignment, and structure."
)

PROMPT_TEXT_PDF: str = (
    # Task
    "You are given one **scanned page** from a PDF. "
    "Re‑create that page as clean HTML with inline or embedded CSS. "
    # Accuracy requirements
    "Preserve original layout, reading order, font sizes, text positions, line breaks, "
    "and any bold/italic/underline styling. "
    "Correct small skew or noise typical of scans, but do NOT re‑flow or rewrite text. "
    # Tables
    "If you detect tabular data, use semantic elements "
    "<table>, <thead>, <tbody>, <tr>, <th>, <td> and apply proper rowspan/colspan "
    "so the table renders exactly like the source. "
    # Images and graphics
    "Embed non‑text graphics (e.g., logos, charts) as <img> with base64‑encoded data URI "
    "or leave a clear HTML comment placeholder such as <!-- figure 1 here --> if extraction fails. "    
    # Output format
    "Return ONLY the HTML string (no markdown code fences) so it can be saved directly."
)

def extract_code_html(output:str) -> str:
    """
    Extract code html from a string containing a ```html ... ``` code block
    
    """
    match= re.search(r"```html\s*([\s\S]+ ?)\s*```", output, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return match


    
def image_to_base64(image_path:str) -> str:
    """
    suport jpg, jpeg, png
    
    """
    image_path = Path(image_path)
    if not image_path.is_file():
        raise FileNotFoundError(f"Image not found: {image_path}")
    
    with open(image_path, 'rb') as file:
        return base64.b64encode(file.read()).decode('utf-8')
    

def convert_pdf_to_images(path:str) -> List[Image.Image]:
    images = convert_from_path(path,first_page=4, last_page=10)
    return images

def convert_images_to_base64(images: List[Image.Image]) -> List[str]:
    base64_list=[]
    for image in images:
        buffered= BytesIO()
        image.save(buffered,format="PNG")
        img_bytes= buffered.getvalue()
        img_base64= base64.b64encode(img_bytes).decode('utf-8')
        base64_list.append(img_base64)

    return base64_list

def build_message_template_for_ocr(base64_images: List[str]) -> List[Dict[str,Any]]:
    """
    This function is built for batch completion
    """

    messages=[]
    for base64_image in base64_images:
        message={
            "role": "user",
            "content": [
                {"type": "text", "text": PROMPT_TEXT_PDF},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                        "detail": "high"
                    }
                },
            ],
        }
        messages.append([message])
    return messages
