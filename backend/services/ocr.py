import json
import asyncio
import litellm
import os
from typing import List
from litellm import acompletion,batch_completion
from litellm.utils import ModelResponse
from config.model_config import load_api_key
from .utils.code_utils import extract_code_html, image_to_base64,build_message_template_for_ocr
from dotenv import load_dotenv
load_dotenv()

os.environ['LITELLM_LOG'] = 'DEBUG'
os.environ['GEMINI_API_KEY'] = "AIzaSyDRv2LdAEwquUwP2CqIfXSdjwIh1CVlVy4"
litellm._turn_on_debug()

ListGeminiModel=[
    'gemini/gemini-1.5-pro-001',
    'gemini/gemini-1.5-pro-002',
    'gemini/gemini-2.5-pro-exp-03-25',
    'gemini/gemini-2.5-pro-preview-03-25' #paid
]

def load_model():
    model = ListGeminiModel[0]
    return model

def temp_load_image(image_path:str) -> str:
    
    return image_to_base64(image_path=image_path) 


async def get_ocr_response_for_image(image_path: str) -> ModelResponse:
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
                        "url": "data:image/jpeg;base64," + temp_load_image(image_path="/home/ngotrisi/OCR_SAD/backend/test/ocr_test.jpg")
                    }
                },
            ],
        }
        ]
    )

    
    return extract_code_html(response['choices'][0]['message']['content'])


async def get_ocr_response_for_list_images(images: List[str]) -> List[ModelResponse]:
    messages_template= build_message_template_for_ocr(images)
    try:
        responses = batch_completion(
            model= load_model(),
            messages = messages_template
        )
    except Exception  as e:
        print(f"Error processing : {e}")
    
    # responses=[]
    # for image in images:
    #     response = litellm.completion(
    #     model=load_model(),
    #     messages=[
    #         {
    #             "role": "user",
    #             "content": [
    #                 {"type": "text", "text": "OCR text for me"},
    #                 {
    #                     "type": "image_url",
    #                     "image_url": {
    #                         "url": f"data:image/jpeg;base64,{image}",
    #                         "detail": "high"
    #                     },
    #                 },
    #             ],
    #         }
    #     ],
    #     )
    #     responses.append(response)

    with open("output/result_batch.json", "w", encoding="utf8") as file:
        json.dump([response.to_dict() for response in responses if hasattr(response, "to_dict")], file,ensure_ascii=True, indent= 4)
    return responses





# #temp
# async def run():
#     response= await get_ocr_response_for_image(image_path="/home/ngotrisi/OCR_SAD/backend/test/ocr_test.jpg")
    
#     rp= response.json()
    
#     with open('output/result_new.json','w', encoding= "utf8") as file:
#         json.dump(rp,file, ensure_ascii=True, indent=4)

#     print('Done')

# if __name__=="__main__":
#     asyncio.run(run())