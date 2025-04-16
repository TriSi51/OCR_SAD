from PIL import Image
import google.generativeai as genai
import json
import os

# Configure API key
genai.configure(api_key='AIzaSyDRv2LdAEwquUwP2CqIfXSdjwIh1CVlVy4')

# Load the image
image = Image.open('/media/ngotrisi/5CDA32B2DA328872/Ocr/backend/test/ocr_test.jpg')

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-1.5-pro-001')

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
json_path='result.json'
html_path='output.html'
for filename in [json_path,html_path]:
    if os.path.exists(filename):
        os.remove(filename)
        print(f"done removing file: {filename}")

with open(json_path, 'w',encoding='utf8') as json_file:
    json.dump(rp, json_file, ensure_ascii=False,indent= 4)

# Save the HTML output
with open(html_path, 'w', encoding='utf-8') as f:   
    f.write(response.text)
