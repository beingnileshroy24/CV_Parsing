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

    def parse_cv(self, cv_text: str, tech6: bool = False) -> CVData:
        if tech6:
            return self._parse_tech6(cv_text)

        prompt = f"""
        You are a highly advanced CV parsing AI. Your goal is to extract EVERY piece of information from the provided CV text without skipping a single detail.
        
        CRITICAL INSTRUCTIONS:
        1. VALIDATE ALL SECTIONS: Carefully scan for:
           - **Personal Details**: Contact info, social links.
           - **Education**: Also known as "Academic Background", "Qualifications", "Scholastic Achievements".
           - **Experience**: Also known as "Work Experience", "Employment History", "Professional Background", "Career Path".
           - **Projects**: Also known as "Key Projects", "Academic Projects", "Personal Projects".
           - **Skills**: Also known as "Technical Skills", "Competencies", "Technologies", "Core Skills".
           - **Languages**: Spoken languages (e.g. English, Spanish).
        2. DYNAMIC EXTRACTION: Identify any non-standard sections (e.g. Certifications ("Credentials", "Licensure"), Awards ("Honors", "Achievements"), volunteering, Interests, Publications, References, Courses, Summary ("Objective", "Profile")).
        3. EXHAUSTIVE CONTENT: For Experience and Projects, extract all bullet points and descriptions. Do not summarize; keep the original detail.
        4. HYPERLINKS: Extract URLs for Projects, Certifications, and Portfolios whenever possible.
        5. CONTACT INFO: Look for Job Title, DOB, Gender, GitHub, Portfolio, and Address in addition to Email/Phone/LinkedIn.
        
        CV Text:
        {cv_text}
        
        Output valid JSON strictly. No markdown formatting.
        Schema:
        {{
            "personal_details": {{
                "name": "string",
                "job_title": "string",
                "date_of_birth": "string",
                "gender": "string",
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
            "languages": [
                {{
                    "language": "string",
                    "proficiency": "string"
                }} 
            ],
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

    def _parse_tech6(self, cv_text: str) -> CVData:
        prompt = f"""
        You are a Proposal Specialist converting a raw CV into the "FORM TECH-6" format.

        **Input CV:**
        {cv_text}

        **Extraction Rules:**
        1. **Header Info:**
           - "Proposed Position": Infer the best title based on their experience (e.g., "Software Developer (Python)").
           - "Name of Firm": Use their *current* or *most recent* employer.
           - "Nationality": Infer from location/context if not explicit (default to "Indian" if context strongly implies, else null).
           - "Personal Details": Extract Name, DOB, Job Title (as extracted above).

        2. **Tables:**
           - **Education**: Extract Degree, College, Date (Year).
           - **Training**: Look for certifications or short courses. If none, return empty list.
           - **Languages**: Extract language name and Proficiency as "Excellent/Good/Fair in speaking, reading, writing".
           - **Employment Record**: List ALL jobs in reverse chronological order (Present to Past). Map to 'experience' list.
           - **Countries of Work**: List strings of countries worked in.

        3. **CRITICAL - Representative Project (Section 13):**
           - Select the **single most significant/recent project** from the CV that demonstrates their core capability.
           - **Client**: Extract the actual client name (e.g., "Country Financial" or "Policy Insurance").
           - **Main Features**: Summarize the project scope into a coherent narrative paragraph (not bullet points).
           - **Activities**: List specific technical tasks performed.
           - **Location**: Infer city/country.

        **Output JSON Schema:**
        {{
            "personal_details": {{ "name": "...", "date_of_birth": "...", "job_title": "...", "email": "...", "phone": "...", "address": "...", "linkedin": "...", "github": "...", "portfolio": "...", "summary": "..." }},
            "firm_name": "...",
            "proposed_position": "...",
            "nationality": "...",
            "memberships": [ {{ "society": "...", "date": "..." }} ],
            "education": [ {{ "degree": "...", "institution": "...", "year": "..." }} ],
            "training": [ {{ "title": "...", "start_date": "...", "end_date": "..." }} ],
            "countries_of_work": ["..."],
            "languages": [ {{ "language": "...", "proficiency": "..." }} ],
            "experience": [
                {{ "role": "...", "company": "...", "duration": "...", "description": ["..."] }}
            ],
            "representative_project": {{
                "name": "...",
                "year": "...",
                "location": "...",
                "client": "...",
                "main_features": "...",
                "positions_held": "...",
                "activities": "..."
            }}
        }}
        """
        response = self.model.generate_content(prompt)
        try:
            cleaned_response = response.text.replace("```json", "").replace("```", "").strip()
            data_dict = json.loads(cleaned_response)
            return CVData(**data_dict)
        except Exception as e:
            print(f"Error parsing Gemini TECH-6 response: {e}")
            raise ValueError(f"Failed to parse TECH-6 data: {e}")

parser_service = GeminiParser()
