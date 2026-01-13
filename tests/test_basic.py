from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the CV Parsing Tool API. Use /docs for Swagger UI."}

def test_imports():
    from app.services.gemini_parser import parser_service
    from app.services.doc_generator import doc_generator
    assert parser_service is not None
    assert doc_generator is not None
