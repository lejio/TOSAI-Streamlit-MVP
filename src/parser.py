from enum import Enum
from pydantic import BaseModel
from openai import OpenAI
from google import genai

import json
from dotenv import load_dotenv
import os

PROMPT = "Extract key information from the privacy agreement. For location and credit card, provide the severity of the data shared on a scale of 1-4."

class Model(Enum):
    OPENAI = "openai"
    GOOGLE = "google"


class PrivacyAgreement(BaseModel):
    email: bool
    username: bool
    password: bool
    dob: bool
    phone: bool
    address: bool
    credit_card: int
    identification_document: bool
    location: int
    administering_website: bool
    communication: bool
    third_party_cookies: bool
    cookies: bool
    web_beacons: bool
    personalization: bool
    advertisement: bool


class Parser:
    def __init__(self, model=Model.GOOGLE, prompt=PROMPT):
        self.model = model
        self.prompt = prompt

        load_dotenv()
        if model == Model.OPENAI:
            self.client = OpenAI(api_key=os.getenv("openai_key"))
        elif model == Model.GOOGLE:
            self.client = genai.Client(api_key=os.getenv("google_key"))

    def parse_text(self, text):
        if self.model == Model.OPENAI:
            return self.openai_parse_text(text)
        elif self.model == Model.GOOGLE:
            return self.google_parse_text(text)
        else:
            raise ValueError("Invalid model")

    def google_parse_text(self, text):
        response = self.client.models.generate_content(
            model='gemini-1.5-flash',
            contents=self.prompt + text,
            config={
                'response_mime_type': 'application/json',
                'response_schema': PrivacyAgreement,
            },
        )
        json_data = json.loads(response.text)
        print(json_data)
        return json_data

    def openai_parse_text(self, text):
        completion = self.client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": self.prompt},
                {"role": "user", "content": text}
            ],
            response_format=PrivacyAgreement,
        )

        json_data = json.loads(completion.choices[0].message.content)
        print(json_data)
        return json_data
