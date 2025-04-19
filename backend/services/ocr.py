import json
import asyncio
import litellm
import os
from typing import List
from litellm import acompletion,batch_completion
from litellm.utils import ModelResponse
from config.model_config import load_api_key
from .utils.code_utils import extract_code_html, image_to_base64,build_message_template_for_ocr,PROMPT_TEXT


from dotenv import load_dotenv
load_dotenv(override=True)

os.environ['LITELLM_LOG'] = 'DEBUG'
litellm._turn_on_debug()

ListGeminiModel=[
    'gemini/gemini-1.5-pro-001',
    'gemini/gemini-1.5-pro-002',
    'gemini/gemini-2.5-pro-exp-03-25',
    'gemini/gemini-2.5-pro-preview-03-25' #paid
]




def my_custom_logging_fn(model_call_dict):
    print(f"model call details: {model_call_dict}")

def load_model():
    model = ListGeminiModel[3]
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
                {"type": "text", "text": PROMPT_TEXT},
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
            messages = messages_template,
            logger_fn= my_custom_logging_fn
        )
    except Exception  as e:
        print(f"Error processing : {e}")

    with open("output/result_batch.json", "w", encoding="utf8") as file:
        json.dump([response.to_dict() for response in responses if hasattr(response, "to_dict")], file,ensure_ascii=False, indent= 4)
    return responses
