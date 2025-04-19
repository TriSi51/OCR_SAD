from PIL import Image
import google.generativeai as genai
import json
import os
import asyncio
from services.utils.code_utils import convert_pdf_to_images,convert_images_to_base64
from services.ocr import get_ocr_response_for_list_images
# from services import convert_images_to_base64, convert_pdf_to_images, get_ocr_response_for_list_images
from dotenv import load_dotenv
import tempfile

load_dotenv(override=True)

os.environ['LITELLM_LOG'] = 'DEBUG'




def run_gemini():
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

    # Load the image
    image = Image.open('/home/ngotrisi/OCR_SAD/backend/test/ocr_test.jpg')

    # Initialize the Gemini model
    model = genai.GenerativeModel('gemini-2.5-pro-preview-03-25')

    # Define the prompt to extract HTML
    prompt = (
        "Convert image to a clean HTML with inline or embedded CSS code. "
        "Preserve the original layout, font sizes, positions, and formatting as accurately as possible. "
        "For tabular data, use <table>, <thead>, <tbody>, <tr>, <th>, and <td> with correct rowspan/colspan to reflect merged cells; "
        "Ensure the final HTML visually matches the original layout of the image, with consistent spacing, alignment, and structure."
    )
    # Generate the content
    response = model.generate_content([prompt, image])
    rp= response.to_dict()
    json_path='output/result.json'
    html_path='output/output.html'
    for filename in [json_path,html_path]:
        if os.path.exists(filename):
            os.remove(filename)
            print(f"done removing file: {filename}")

    with open(json_path, 'w',encoding='utf8') as json_file:
        json.dump(rp, json_file, ensure_ascii=False,indent= 4)

    # Save the HTML output
    with open(html_path, 'w', encoding='utf-8') as f:   
        f.write(response.text)


async def run_batch_completion(pdf_path:str):
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()
    suffix = ".pdf"
    with tempfile.NamedTemporaryFile(delete=True, suffix= suffix) as tmp:
        tmp.write(pdf_bytes)
        tmp.flush()

        images= convert_pdf_to_images(tmp.name)
        base64_images= convert_images_to_base64(images)
        return await get_ocr_response_for_list_images(base64_images)


if __name__ == "__main__":

    # file_pdf= "/home/ngotrisi/OCR_SAD/backend/test/dai viet su ky toan thu-tap 1-340@.pdf"
    # asyncio.run(run_batch_completion(file_pdf))
    run_gemini()