from fastapi import APIRouter,UploadFile, File, HTTPException
from services.utils.code_utils import convert_pdf_to_images,convert_images_to_base64
from services.ocr import get_ocr_response_for_list_images
from services.qa_bot.qa_engine import build_index_from_text,query_pdf
import tempfile
from pydantic import BaseModel

router= APIRouter()

@router.post('/ocr/')
async def perform_pdf_ocr(file: UploadFile= File(...)):
    suffix = f".{file.filename.split('.')[-1]}" if '.' in file.filename else ''
    with tempfile.NamedTemporaryFile(delete=True, suffix= suffix) as tmp:
        contents= await file.read()
        tmp.write(contents)
        tmp.flush()
        #Save to database
        from services.qa_bot.pdf_qa_db import save_pdf_binary
        pdf_id= save_pdf_binary(file.filename , contents)

        #OCR task
        images= convert_pdf_to_images(tmp.name)
        base64_images= convert_images_to_base64(images)
        message= await get_ocr_response_for_list_images(base64_images)
        return {"pdf_id": pdf_id, "message": message}

@router.post("/prepare_qa/")
async def prepare_pdf_qa(pdf_id: int):
    build_index_from_text(pdf_id)
    return {"message": "QA-ready"}
    
class QuestionRequest(BaseModel):
    pdf_id:int
    question:str

@router.post("/question/")
async def question(request: QuestionRequest):
    try:
        answer= query_pdf(request.pdf_id, request.question)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error answering question: {e}")
    
    return answer

