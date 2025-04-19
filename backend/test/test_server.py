from fastapi.testclient import TestClient
from server import app
import json
import shutil
import os
import fitz
from PyPDF2 import PdfReader


folder_path="/home/ngotrisi/OCR_SAD/backend/storage"

def read_pdf_with_pypdf2(path):
    reader = PdfReader(path)

    return "\n".join(page.extract_text() or "" for page in reader.pages).strip()


def delete_storage():
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        shutil.rmtree(folder_path)
        print(f"Folder '{folder_path}' deleted.")
    else:
        print(f"Folder '{folder_path}' does not exist.")

client= TestClient(app)
def test_ocr_upload():
    file_path='/home/ngotrisi/OCR_SAD/backend/test/dai viet su ky toan thu-tap 1-340@.pdf'
    with open(file_path,"rb") as f:
        response= client.post(
            "/ocr/",
            files= {"file": (file_path, f, "application/pdf")},
        )
    assert response.status_code==200

    with open('output/result_test.json','w', encoding= 'utf8') as json_file:
        json.dump(response.json()['message'],json_file,ensure_ascii=False,indent=4)
    id = response.json()['pdf_id']


    # response_prepare= client.post(
    #     "/prepare_qa/",
    #     params={"pdf_id": id}
    # )
    # assert response_prepare.status_code==200

    # print(response_prepare.json())

    # try:
    #     response_question = client.post(
    #         "/question/",
    #         json={
    #             "pdf_id": 1,
    #             "question": "What is the main topic of this document?"
    #         }
    #     )

    #     if response_question.status_code != 200:
    #         raise Exception(
    #             f"Expected status 200 but got {response_question.status_code}. "
    #             f"Response body: {response_question.text}"
    #         )

    #     print("✅ Test passed. Response:", response_question.json())

    # except Exception as e:
    #     print("❌ Test failed:", str(e))
    
    from services.qa_bot.pdf_qa_db import delete_db
    delete_db()
    delete_storage()


def read_pdf_text(file_path: str) -> str:
    """
    Reads text from a PDF file using PyMuPDF (fitz).
    
    :param file_path: Path to the PDF file
    :return: Combined text from all pages
    """
    try:
        doc = fitz.open(file_path)
        all_text = []

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text("text")
            all_text.append(text)

        doc.close()
        return "\n".join(all_text)

    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""


if __name__ =="__main__":
    test_ocr_upload()
    # a=read_pdf_with_pypdf2('/home/ngotrisi/OCR_SAD/backend/test/dai viet su ky toan thu-tap 1-340@.pdf')
    # print(a)