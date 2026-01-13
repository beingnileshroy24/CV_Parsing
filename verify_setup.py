import os
import sys

def verify():
    print("--- CV Parsing Tool Health Check ---")
    
    # 1. Check .env
    if os.path.exists(".env"):
        print("[OK] .env file found.")
    else:
        print("[!!] .env file MISSING.")
        
    # 2. Check template
    template_path = "templates/cv_template.docx"
    if os.path.exists(template_path):
        size = os.path.getsize(template_path)
        print(f"[OK] Default template found ({size} bytes).")
        
        # Check for bad tags
        try:
            from docxtpl import DocxTemplate
            import io
            doc = DocxTemplate(template_path)
            xml = doc.get_docx()._part.blob.decode('utf-8', errors='ignore')
            if "{% tr" in xml or "{%tr" in xml:
                print("[!!] ERROR: The template contains invalid '{% tr %}' tags. Please delete the 'templates' folder and run 'python3 generate_template.py'.")
            else:
                print("[OK] No invalid tags found in template.")
        except Exception as e:
            print(f"[!!] Could not verify template tags: {e}")
    else:
        print("[!!] Default template MISSING. Run 'python3 generate_template.py' first.")

    # 3. Check Python Env
    print(f"[INFO] Running with Python: {sys.version}")
    try:
        import fastapi
        import docxtpl
        import pydantic
        print("[OK] All required libraries are installed.")
    except ImportError as e:
        print(f"[!!] Missing library: {e}")

if __name__ == "__main__":
    verify()
