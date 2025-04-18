from fastapi.testclient import TestClient
from server import app
import json
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
        json.dump(response.json(),json_file,ensure_ascii=False,indent=4)






test_ocr_upload()