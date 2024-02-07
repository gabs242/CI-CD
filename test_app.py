import pytest
from unittest.mock import patch
from io import BytesIO
from app import app

# Configure your Flask app for testing
@pytest.fixture
def client():
    app.config.update({
        "TESTING": True,
    })
    with app.test_client() as client:
        yield client

# Mock Google Cloud Storage's blob method
@pytest.fixture
def mock_storage(monkeypatch):
    class MockBlob:
        def upload_from_string(self, *args, **kwargs):
            pass

    def mock_blob(*args, **kwargs):
        return MockBlob()

    monkeypatch.setattr('google.cloud.storage.Bucket.blob', mock_blob)

# Test the /klasifikasi route
def test_klasifikasi_route(client, mock_storage):
    data = {
        'image': (BytesIO(b'my image data'), 'image.jpg')
    }
    response = client.post('/klasifikasi', content_type='multipart/form-data', data=data)
    assert response.status_code == 200
    assert response.json == {"message": "Berhasil"}

# Optionally, test other routes as needed
def test_get_posted_data(client):
    response = client.get('/get_data')
    assert response.status_code == 200
    assert response.json == {"message": "No data has been posted yet."}

def test_hello(client):
    response = client.get('/crabify')
    assert response.status_code == 200
    assert response.json == {"message": "Hello, this is a GET request!"}
