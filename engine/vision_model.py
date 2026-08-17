import base64
from google import genai
import os
from engine.dataAcquisition import dataAcquision
import mimetypes
from dotenv import load_dotenv
load_dotenv()

dataAcquire = dataAcquision()

class visionModel:
    def engine(self, image, prompt):
        client = genai.Client(api_key = os.getenv('GEMINI_API_KEY'))

        with open(image, "rb") as f:
            image_bytes = f.read()
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")

        mime_type, _ = mimetypes.guess_type(image)
        # dataAcquire.allFields()
        print(prompt)

        interaction = client.interactions.create(
            model="gemini-3.6-flash",
            input=[
                {"type": "text", "text": prompt},
                {
                    "type": "image",
                    "data": image_b64,
                    "mime_type": mime_type,
                },
            ]
        )
        # print(interaction.output_text)
        return interaction.output_text
        # with open("output.text", "w", encoding="utf-8") as file:
        #     file.write(interaction.output_text)