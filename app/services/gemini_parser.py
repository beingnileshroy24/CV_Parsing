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
        You are a highly advanced CV parsing AI. Your goal is to extract EVERY piece of information from the provided CV text without skipping a single detail.
        
        CRITICAL INSTRUCTIONS:
        1. VALIDATE ALL SECTIONS: Carefully scan for Personal Details, Education, Experience, Projects, and Skills.
        2. DYNAMIC EXTRACTION: Identify any non-standard sections (e.g. Certifications, Awards, volunteering, Languages, Interests, Publications, References, Courses, Summary).
        3. EXHAUSTIVE CONTENT: For Experience and Projects, extract all bullet points and descriptions. Do not summarize; keep the original detail.
        4. HYPERLINKS: Extract URLs for Projects, Certifications, and Portfolios whenever possible.
        5. CUSTOM SECTIONS: If ANY info remains that doesn't fit standard fields, create a new entry in `custom_sections` with a descriptive title and all relevant text as a list of strings in `content`.
        6. CONTACT INFO: Look for GitHub, Portfolio, and Address in addition to Email/Phone/LinkedIn.
        
        CV Text:
        {cv_text}
        
        Output valid JSON strictly. No markdown formatting.
        Schema:
        {{
            "personal_details": {{
                "name": "string",
                "email": "string",
                "phone": "string",
                "address": "string",
                "linkedin": "string",
                "github": "string",
                "portfolio": "string",
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
                    "technologies": ["string"],
                    "url": "string"
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
