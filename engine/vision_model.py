import base64
from google import genai
import os
from dotenv import load_dotenv
load_dotenv()

client = genai.Client(api_key = os.getenv('GEMINI_API_KEY'))

with open("engine/tomato.jpg", "rb") as f:
    image_bytes = f.read()
image_b64 = base64.b64encode(image_bytes).decode("utf-8")

interaction = client.interactions.create(
    model="gemini-3.6-flash",
    input=[
        {"type": "text", "text": "Identify the leaf from the image and tell me what happened to it."},
        {
            "type": "image",
            "data": image_b64,
            "mime_type": "image/jpeg"
        },
    ]
)
print(interaction.output_text)