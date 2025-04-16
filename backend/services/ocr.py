import litellm
from litellm import acompletion
from litellm.utils import ModelResponse
import json
import asyncio
from config.model_config import load_api_key
from utils.image_utils import image_to_base64
litellm.set_verbose= True
def load_model():
    model = "gemini/gemini-1.5-pro-001"
    return model

def temp_load_image(image_path:str) -> str:
    
    return image_to_base64(image_path=image_path) 


async def get_response(image_path: str) -> ModelResponse:
    response= await acompletion(
        model= load_model(),
        messages= [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Convert image to a clean HTML with inline or embedded CSS code."},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": temp_load_image(image_path),
                        "format": "image/jpg"
                    }
                },
            ],
        }


        ]

        
    )

    return response

#temp
async def run():
    response= await get_response(image_path="/media/ngotrisi/5CDA32B2DA328872/Ocr/backend/test/ocr_test.jpg")
    rp= response.json()
    with open('result_new.json','w', encoding= "utf8") as file:
        json.dump(rp,file, ensure_ascii=True, indent=4)

if __name__=="__main__":
    asyncio.run(run())