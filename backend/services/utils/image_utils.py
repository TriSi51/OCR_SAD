import base64
from pathlib import Path

def image_to_base64(image_path:str) -> str:
    """
    suport jpg, jpeg, png
    
    """
    image_path = Path(image_path)
    if not image_path.is_file():
        raise FileNotFoundError(f"Image not found: {image_path}")
    
    with open(image_path, 'rb') as file:
        encoded_string= base64.b64encode(file.read()).decode('utf-8')
    
    return encoded_string
