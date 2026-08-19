import base64
import json
import itertools
from google import genai
import os
import mimetypes
from engine.dataAcquisition import dataAcquision
from dotenv import load_dotenv

load_dotenv()

dataAcquire = dataAcquision()

keys = [os.getenv('GEMINI_API_KEY_1'), os.getenv('GEMINI_API_KEY_2'), os.getenv('GEMINI_API_KEY_3')]

key_cycle = itertools.cycle(keys)
class visionModel:

    def engine(self, image, prompt):
        api_key = next(key_cycle)
        client = genai.Client(
            api_key=api_key
        )

        with open(image, "rb") as f:
            image_bytes = f.read()

        image_b64 = base64.b64encode(image_bytes).decode("utf-8")

        mime_type, _ = mimetypes.guess_type(image)

        print(prompt)

        interaction = client.interactions.create(
            model="gemini-3.6-flash",
            input=[
                {
                    "type": "text",
                    "text": prompt
                },
                {
                    "type": "image",
                    "data": image_b64,
                    "mime_type": mime_type,
                }
            ]
        )

        response_text = interaction.output_text

        print(response_text)

        try:
            result = json.loads(response_text)

        except json.JSONDecodeError:
            print("Invalid JSON returned by Gemini.")
            print(response_text)
            return None

        return result