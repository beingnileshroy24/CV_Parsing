from app.services.doc_generator import doc_generator
from app.schemas import CVData, Project
import io

def test_hyperlinks():
    # 1. Create Data with various links
    data = CVData(
        personal_details={
            "name": "Link Master",
            "email": "link@master.com",
            "linkedin": "linkedin.com/in/linkmaster", # Should be auto-converted to http://...
            "github": "http://github.com/linkmaster",
            "portfolio": "https://linkmaster.dev",
            "summary": "Check out my work at https://mysite.com/work and also www.google.com"
        },
        education=[],
        experience=[
            {
                "role": "Developer",
                "company": "Tech Corp",
                "description": ["Implemented feature X see more at https://docs.techcorp.com/featurex"]
            }
        ],
        projects=[
            Project(
                name="Super Web App", 
                description="A cool app available at https://superwebapp.com", 
                url="https://github.com/linkmaster/superwebapp"
            )
        ],
        skills=["Linking"]
    )
    
    # 2. Generate DOCX
    print("Generating DOCX with hyperlinks...")
    stream = doc_generator.generate_docx(data, template_style="paragraph")
    
    # 3. Save to file for manual inspection (programmatically checking hyperlinks in python-docx is hard without unzipping)
    with open("test_hyperlinks.docx", "wb") as f:
        f.write(stream.getvalue())
        
    print("[SUCCESS] Check 'test_hyperlinks.docx' manually to verify blue clickable links.")

if __name__ == "__main__":
    try:
        test_hyperlinks()
    except Exception as e:
        print(f"[ERROR] {e}")
