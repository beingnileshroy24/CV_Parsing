from docxtpl import DocxTemplate
import io
import os
from app.schemas import CVData, PersonalDetails, Education, Experience, Project, CustomSection

def test_templates():
    # Create dummy data
    data = CVData(
        personal_details=PersonalDetails(
            name="John Doe",
            email="john@example.com",
            phone="1234567890",
            address="123 Street, City",
            linkedin="linkedin.com/in/johndoe",
            github="github.com/johndoe",
            summary="Experienced developer."
        ),
        education=[
            Education(degree="B.Tech", institution="IIT", year="2020", grade="9.0"),
            Education(degree="12th", institution="KV", year="2016", grade="90%")
        ],
        experience=[
            Experience(role="SDE", company="Google", duration="2 years", description=["Developed features.", "Fixed bugs."]),
            Experience(role="Intern", company="Microsoft", duration="6 months", description=["Learned cloud.", "Built tools."])
        ],
        projects=[
            Project(name="AI Bot", description="An AI chatbot.", technologies=["Python", "Gemini"]),
            Project(name="Web App", description="A React web app.", technologies=["React", "Node"])
        ],
        skills=["Python", "FastAPI", "React"],
        custom_sections=[
            CustomSection(title="Certifications", content=["AWS Certified", "Google Cloud Associate"]),
            CustomSection(title="Languages", content=["English", "Hindi"])
        ]
    )
    context = data.model_dump()

    # Use DocGenerator to test
    from app.services.doc_generator import doc_generator

    # Test Paragraph Template
    try:
        output_stream = doc_generator.generate_docx(data, template_style="paragraph")
        with open("test_para_output.docx", "wb") as f:
            f.write(output_stream.getbuffer())
        print("[OK] Paragraph Template rendered successfully.")
    except Exception as e:
        print(f"[ERROR] Paragraph Template: {e}")

    # Test Tabular Template
    try:
        output_stream = doc_generator.generate_docx(data, template_style="tabular")
        with open("test_table_output.docx", "wb") as f:
            f.write(output_stream.getbuffer())
        print("[OK] Tabular Template rendered successfully.")
    except Exception as e:
        print(f"[ERROR] Tabular Template: {e}")

if __name__ == "__main__":
    test_templates()
