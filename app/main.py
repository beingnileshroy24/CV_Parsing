from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse, FileResponse
from app.schemas import CVData
from app.services.gemini_parser import parser_service
from app.services.doc_generator import doc_generator
from app.utils import extract_text_from_upload_file
import uvicorn
import os

app = FastAPI(title="CV Parsing & Generation API")

@app.get("/")
def read_root():
    return {"message": "Welcome to the CV Parsing Tool API. Use /docs for Swagger UI."}

@app.get("/download-template")
def download_template():
    """
    Downloads the default sample DOCX template.
    """
    template_path = "templates/cv_template.docx"
    if not os.path.exists(template_path):
        raise HTTPException(status_code=404, detail="Template not found. Please run generate_template.py first.")
    return FileResponse(
        template_path, 
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename="sample_cv_template.docx"
    )

@app.post("/parse", response_model=CVData)
async def parse_cv(file: UploadFile = File(...)):
    """
    Parses an uploaded CV (PDF/DOCX) and returns structured JSON data.
    """
    try:
        text = await extract_text_from_upload_file(file)
        parsed_data = parser_service.parse_cv(text)
        return parsed_data
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

@app.post("/generate")
async def generate_cv(data: CVData, template_file: UploadFile = File(None)):
    """
    Generates a formatted DOCX CV based on the provided JSON data.
    Optionally accepts a customized DOCX template.
    """
    try:
        template_bytes = await template_file.read() if template_file else None
        file_stream = doc_generator.generate_docx(data, template_bytes=template_bytes)
        return StreamingResponse(
            file_stream, 
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": "attachment; filename=parsed_cv.docx"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process")
async def process_full_flow(file: UploadFile = File(...), template_file: UploadFile = File(None)):
    """
    End-to-end flow: Upload raw CV + Optional Template -> Parse -> Generate DOCX.
    """
    try:
        # 1. Extract Text from CV
        text = await extract_text_from_upload_file(file)
        
        # 2. Parse with Gemini
        parsed_data = parser_service.parse_cv(text)
        
        # 3. Read Template if provided
        template_bytes = await template_file.read() if template_file else None
        
        # 4. Generate DOCX
        file_stream = doc_generator.generate_docx(parsed_data, template_bytes=template_bytes)
        
        return StreamingResponse(
            file_stream, 
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": "attachment; filename=generated_cv.docx"}
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
