from fastapi import APIRouter,UploadFile, File
from services.utils.code_utils import convert_pdf_to_images,convert_images_to_base64
from services.ocr import get_ocr_response_for_list_images
import tempfile


router= APIRouter()

@router.post('/ocr/')
async def perform_pdf_ocr(file: UploadFile= File(...)):
    suffix = f".{file.filename.split('.')[-1]}" if '.' in file.filename else ''
    with tempfile.NamedTemporaryFile(delete=True, suffix= suffix) as tmp:
        contents= await file.read()
        tmp.write(contents)
        tmp.flush()

        images= convert_pdf_to_images(tmp.name)
        base64_images= convert_images_to_base64(images)
        return await get_ocr_response_for_list_images(base64_images)

        



