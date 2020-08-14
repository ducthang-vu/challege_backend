import json
from pathlib import Path

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_upload_correct_file():
    """Test endpoint "/upload-file" (POST): returns 200 when uploaded file is correct"""
    file_path = Path(__file__).parent.parent / 'file_for_test_upload' / 'correct_file.csv'
    with open(file_path, 'rb') as file:
        file_object = file.read()
    response = client.post("/upload-file", files={"file": file_object})
    assert response.status_code == 200


def test_create_upload_correct_file_small():
    """Test endpoint "/upload-file" (POST)"""
    file_path = Path(__file__).parent.parent / 'file_for_test_upload' / 'correct_file_small.csv'
    with open(file_path, 'rb') as file_csv:
        file_object = file_csv.read()
    json_path = Path(__file__).parent.parent / 'file_for_test_upload' / 'small.json'
    with open(json_path, 'rb') as file_json:
        json_content = json.load(file_json)
    response = client.post("/upload-file", files={"file": file_object})
    assert response.status_code == 200
    assert response.json() == json_content


def test_create_upload_wrong_file():
    """Test endpoint "/upload-file" (POST): returns 422 when csv file is invalid"""
    file_path = Path(__file__).parent.parent / 'file_for_test_upload' / 'wrong_file_column_names.csv'
    with open(file_path, 'rb') as file:
        file_object = file.read()
    response = client.post("/upload-file", files={"file": file_object})
    assert response.status_code == 422


def test_send_form_check_number():
    response = client.get("/")
    assert response.status_code == 200


def test_send_form_post_with_number():
    """Test endpoint "/" (POST), return 200 when parameter is correct"""
    response = client.post("/", data={'number': '123456'})
    assert response.status_code == 200


def test_send_form_post_missing_number():
    """Test endpoint "/" (POST), return 422 when missing parameter"""
    response = client.post("/", data={'number': None})
    assert response.status_code == 422
