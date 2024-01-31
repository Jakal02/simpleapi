"""
Pytest file for testing the API.
"""
from fastapi import status
from fastapi.testclient import TestClient
from my_api import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == status.HTTP_200_OK
