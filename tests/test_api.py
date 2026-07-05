from fastapi.testclient import TestClient

from app import app

client = TestClient(app)

def test_get_history():
    response = client.get("/history")
    assert response.status_code == 200
    assert isinstance(response.json(), list) #Converts the JSON response into Python.