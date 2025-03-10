from pydantic import BaseModel
from openai import OpenAI
import json
from dotenv import load_dotenv
import os

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
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("api_key"))

    def parse_text(self, text):
        completion = self.client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": "Extract key information from the privacy agreement. For location and credit card, provide the severity of the data shared on a scale of 1-4."},
                {"role": "user", "content": text}
            ],
            response_format=PrivacyAgreement,
        )
        
        json_data = json.loads(completion.choices[0].message.content)
        return json_data


