import google.generativeai as genai 
import json
from llm.prompt_builder import PromptBuilder
from dotenv import load_dotenv
import os

class GeminiClient:
    def __init__(self):

        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash")
        self.prompt_builder = PromptBuilder()

    def generate_response(self, content, prompt_type="criminal_news"):
        """Generate a response from the Gemini model."""
        prompt = self.prompt_builder.orcrim_news(content)

        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        return response.text

    def clean_response(self, response):
        """Clean the response text by removing unwanted characters."""
        return response.replace("```", "").replace("´´´", "").replace("json", "").strip()

    def parse_response(self, response):
        """Parse the response as JSON and handle errors."""
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            print("Original response:")
            print(response)
            return None 