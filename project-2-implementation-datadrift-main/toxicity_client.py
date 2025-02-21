import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ToxicityClient:
    def _init_(self):
        self.api_url = "https://api.moderatehatespeech.com"
        self.api_key = os.getenv("MODERATE_HATESPEECH_API_KEY")

    def get_toxicity_score(self, text):
        payload = {"text": text}
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.post(f"{self.api_url}/api/v1/moderate/", json=payload, headers=headers, verify=False)
        response.raise_for_status()
        result = response.json()
        return result