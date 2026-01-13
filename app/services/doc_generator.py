from docxtpl import DocxTemplate
from app.schemas import CVData
import io

class DocGenerator:
    def __init__(self, template_path: str = "templates/cv_template.docx"):
        self.template_path = template_path

    def generate_docx(self, data: CVData) -> io.BytesIO:
        try:
            doc = DocxTemplate(self.template_path)
            
            # Convert Pydantic model to dict
            context = data.model_dump()
            
            doc.render(context)
            
            file_stream = io.BytesIO()
            doc.save(file_stream)
            file_stream.seek(0)
            return file_stream
        except Exception as e:
            raise RuntimeError(f"Error generating DOCX: {e}")

doc_generator = DocGenerator()
