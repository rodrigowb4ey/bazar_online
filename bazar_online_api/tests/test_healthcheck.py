from http import HTTPStatus

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_healthcheck() -> None:
    """Test that the healthcheck endpoint returns the expected response."""
    response = client.get('/healthcheck')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'status': 'ok'}
