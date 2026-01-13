from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import StreamingResponse, FileResponse
from app.schemas import CVData
from app.services.gemini_parser import parser_service
from app.services.doc_generator import doc_generator
from app.utils import extract_text_from_upload_file
import uvicorn
import os
from typing import Optional

app = FastAPI(title="CV Parsing & Generation API")

@app.get("/")
def read_root():
    return {"message": "Welcome to the CV Parsing Tool API. Use /docs for Swagger UI."}

@app.get("/download-template")
def download_template(style: str = "paragraph"):
    """
    Downloads the default sample DOCX template.
    Options for style: 'paragraph' or 'tabular'.
    """
    if style == "tabular":
        template_path = "templates/tabular_template.docx"
    else:
        template_path = "templates/paragraph_template.docx"
        
    if not os.path.exists(template_path):
        raise HTTPException(status_code=404, detail=f"Template {style} not found. Please run generate_template.py first.")
    
    return FileResponse(
        template_path, 
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=f"sample_cv_{style}_template.docx"
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
async def generate_cv(data: CVData, style: str = "paragraph", template_file: Optional[UploadFile] = None, masking: bool = False):
    """
    Generates a formatted DOCX CV based on the provided JSON data.
    Optionally accepts a customized DOCX template or a default style ('paragraph' or 'tabular').
    If masking=True, contact details (email, phone, address, linkedin, etc.) will be hidden.
    """
    try:
        # Scrub data if masking is enabled
        if masking:
            data.personal_details.email = None
            data.personal_details.phone = None
            data.personal_details.address = None
            data.personal_details.linkedin = None
            data.personal_details.github = None
            data.personal_details.portfolio = None
        
        template_bytes = None
        if template_file and template_file.filename:
            template_bytes = await template_file.read()
            
        file_stream = doc_generator.generate_docx(data, template_bytes=template_bytes, template_style=style)
        return StreamingResponse(
            file_stream, 
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": "attachment; filename=parsed_cv.docx"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process")
async def process_full_flow(
    file: UploadFile = File(...), 
    style: str = Form("paragraph"), 
    template_file: Optional[UploadFile] = None,
    masking: bool = Form(False)
):
    """
    End-to-end flow: Upload raw CV + Optional Template -> Parse -> Generate DOCX.
    If masking=True, contact details will be removed from the final DOCX.
    """
    try:
        # 1. Extract Text from CV
        text = await extract_text_from_upload_file(file)
        
        # 2. Parse with Gemini
        parsed_data = parser_service.parse_cv(text)
        
        # 2.5 Masking
        if masking:
            parsed_data.personal_details.email = None
            parsed_data.personal_details.phone = None
            parsed_data.personal_details.address = None
            parsed_data.personal_details.linkedin = None
            parsed_data.personal_details.github = None
            parsed_data.personal_details.portfolio = None
        
        # 3. Read Template if provided correctly
        template_bytes = None
        if template_file and template_file.filename and not template_file.filename.strip() == "":
            content = await template_file.read()
            if len(content) > 0:
                print(f"Received custom template: {template_file.filename} ({len(content)} bytes)")
                template_bytes = content
        
        if not template_bytes:
            print(f"No custom template detected. Using system default style: {style}.")
        
        # 4. Generate DOCX
        file_stream = doc_generator.generate_docx(parsed_data, template_bytes=template_bytes, template_style=style)
        
        return StreamingResponse(
            file_stream, 
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f"attachment; filename=generated_cv.docx"}
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"FULL ERROR STACK:\n{error_detail}")
        
        # Determine if it's a Jinja error
        if "unknown tag 'tr'" in str(e).lower():
            msg = "Jinja Error: The template contains an invalid '{% tr %}' tag. "
            if template_bytes:
                msg += "Please check your UPLOADED custom template."
            else:
                msg += "Please delete the 'templates/' folder on your machine and run 'python3 generate_template.py' to reset the default template."
            raise HTTPException(status_code=500, detail=msg)
            
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
