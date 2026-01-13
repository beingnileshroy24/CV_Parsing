import unittest
from unittest.mock import MagicMock, patch
import json
import os
from app.services.gemini_parser import GeminiParser
from app.services.doc_generator import DocGenerator
from app.schemas import CVData

# Sample TECH-6 JSON Response
MOCK_TECH6_RESPONSE = """
{
    "personal_details": {
        "name": "Jane Doe",
        "date_of_birth": "1990-01-01",
        "job_title": "Senior Urban Planner",
        "email": "jane@example.com",
        "phone": "+1234567890",
        "address": "123 City St",
        "nationality": "Indian",
        "linkedin": "linkedin.com/in/janedoe",
        "summary": "Experienced planner."
    },
    "firm_name": "Urban Solutions Ltd",
    "proposed_position": "Team Leader",
    "nationality": "Indian",
    "memberships": [
        { "society": "Institute of Urban Planners", "date": "2015" }
    ],
    "education": [
        { "degree": "M.Sc. Urban Planning", "institution": "City University", "year": "2014" }
    ],
    "training": [
        { "title": "GIS Advanced Course", "start_date": "Jan 2016", "end_date": "Mar 2016" }
    ],
    "countries_of_work": ["India", "Vietnam"],
    "languages": [
        { "language": "English", "proficiency": "Excellent in speaking, reading, writing" }
    ],
    "experience": [
        { 
            "role": "Planner", 
            "company": "Prev Co", 
            "duration": "2015-2020", 
            "description": ["Managed city projects", "Led team of 5"] 
        }
    ],
    "representative_project": {
        "name": "Smart City Development",
        "year": "2020-2022",
        "location": "Pune, India",
        "client": "Pune Municipal Corp",
        "main_features": "Development of smart traffic systems.",
        "positions_held": "Lead Consultant",
        "activities": "Designed traffic flow, managed stakeholder meetings."
    }
}
"""

class TestTech6Flow(unittest.TestCase):
    
    @patch('app.services.gemini_parser.genai')
    def test_end_to_end_tech6(self, mock_genai):
        # 1. Setup Mock
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = MOCK_TECH6_RESPONSE
        mock_model.generate_content.return_value = mock_response
        
        # Mock the GenerativeModel constructor to return our mock_model
        mock_genai.GenerativeModel.return_value = mock_model
        
        # Initialize Parser (API Key check happens in init, so we might need to mock os.getenv if strict)
        # Assuming .env has a key or we mock it.
        with patch.dict(os.environ, {"GEMINI_API_KEY": "fake_key"}):
            parser = GeminiParser()
            
            # 2. Test Parsing
            print("Testing Parser logic...")
            cv_data = parser.parse_cv("dummy text", tech6=True)
            
            self.assertIsInstance(cv_data, CVData)
            self.assertEqual(cv_data.firm_name, "Urban Solutions Ltd")
            self.assertEqual(cv_data.representative_project.client, "Pune Municipal Corp")
            print("Parser logic verified: Successfully mapped JSON to CVData schema.")
            
            # 3. Test Generation
            print("Testing Doc Generation...")
            generator = DocGenerator()
            # Ensure template exists (should have been created by generate_tech6_template.py)
            if not os.path.exists("templates/tech6_template.docx"):
                print("template not found, creating it...")
                from generate_tech6_template import create_tech6_template
                create_tech6_template()
                
            stream = generator.generate_docx(cv_data, template_style="tech6")
            
            self.assertIsNotNone(stream)
            content = stream.read()
            self.assertGreater(len(content), 0)
            print(f"Doc Generation verified: Created {len(content)} bytes DOCX.")
            
            # Optional: Save to inspect manually if needed
            with open("test_output_tech6.docx", "wb") as f:
                f.write(content)
            print("Saved test_output_tech6.docx for inspection.")

if __name__ == '__main__':
    unittest.main()
