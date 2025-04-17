import re
import base64
from typing import List,Dict,Any
from io import BytesIO
from PIL import Image
from pathlib import Path
from pdf2image import convert_from_path
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
    messages=[]

    for base64_image in base64_images:
        message={
            "role": "user",
            "content": [
                {"type": "text", "text": "Convert image to a clean HTML with inline or embedded CSS code."},
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
