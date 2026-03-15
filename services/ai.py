import os
from google import genai


def call_ai(system: str, user: str) -> str:
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is not set. Add it to your .env file or Streamlit secrets."
        )
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=user,
        config={"system_instruction": system},
    )
    return response.text
