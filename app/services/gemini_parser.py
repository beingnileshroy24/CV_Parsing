import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from app.schemas import CVData

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

class GeminiParser:
    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def parse_cv(self, cv_text: str) -> CVData:
        prompt = f"""
        You are an expert CV parser. Your goal is to extract structured data from the CV text.
        
        CRITICAL INSTRUCTIONS:
        1. Extract standard fields (Education, Experience, Projects, Skills) as usual.
        2. INTELLIGENT PARSING: Identify ANY other sections present in the CV (e.g., "Certifications", "Awards", "Publications", "Volunteering", "Languages", "Interests", "References").
        3. Place these additional sections into the `custom_sections` list.
        4. Do NOT ignore any information. If it doesn't fit standard fields, make a custom section for it.
        
        CV Text:
        {cv_text}
        
        Output JSON strictly. No markdown formatting.
        Schema:
        {{
            "personal_details": {{
                "name": "string",
                "email": "string",
                "phone": "string",
                "linkedin": "string",
                "summary": "string"
            }},
            "education": [
                {{
                    "degree": "string",
                    "institution": "string",
                    "year": "string",
                    "grade": "string"
                }}
            ],
            "experience": [
                {{
                    "role": "string",
                    "company": "string",
                    "duration": "string",
                    "description": ["string"]
                }}
            ],
            "projects": [
                {{
                    "name": "string",
                    "description": "string",
                    "technologies": ["string"]
                }}
            ],
            "skills": ["string"],
            "custom_sections": [
                {{
                    "title": "string",
                    "content": ["string"]
                }}
            ]
        }}
        """
        
        response = self.model.generate_content(prompt)
        try:
            # Clean up potential markdown code blocks
            cleaned_response = response.text.replace("```json", "").replace("```", "").strip()
            data_dict = json.loads(cleaned_response)
            return CVData(**data_dict)
        except (json.JSONDecodeError, Exception) as e:
            print(f"Error parsing Gemini response: {e}")
            print(f"Raw response: {response.text}")
            raise ValueError("Failed to parse CV data from Gemini response")

parser_service = GeminiParser()
