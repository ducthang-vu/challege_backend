from pathlib import Path

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_upload_correct_file():
    file_path = Path(__file__).parent.parent / 'file_for_test_upload' / 'correct_file.csv'
    with open(file_path, 'rb') as file:
        file_object = file.read()
    response = client.post("/upload-file", files={"file": file_object})
    assert response.status_code == 200


def test_create_upload_wrong_file():
    file_path = Path(__file__).parent.parent / 'file_for_test_upload' / 'wrong_file_column_names.csv'
    with open(file_path, 'rb') as file:
        file_object = file.read()
    response = client.post("/upload-file", files={"file": file_object})
    assert response.status_code == 422


def test_send_form_check_number():
    response = client.get("/check-number/form")
    assert response.status_code == 200


def test_send_form_post_with_number():
    response = client.post("/check-number/form", data={'number': '123456'})
    assert response.status_code == 200


def test_send_form_post_missing_number():
    response = client.post("/check-number/form", data={'number': None})
    assert response.status_code == 422
