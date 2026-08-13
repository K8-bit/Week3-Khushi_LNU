from uuid import uuid4

from fastapi.testclient import TestClient


USERS_URL = "/api/users"
REGISTER_USER_URL = f"{USERS_URL}/register"


def create_user_payload() -> dict[str, str]:
    unique_value = uuid4().hex[:8]

    return {
        "name": f"Test User {unique_value}",
        "email": f"test_{unique_value}@example.com",
        "mobile": f"9{uuid4().int % 1_000_000_000:09d}",
        "password": "TestPassword123!",
    }


def test_create_user_returns_created_user(
    client: TestClient,
) -> None:
    payload = create_user_payload()

    response = client.post(
        REGISTER_USER_URL,
        json=payload,
    )

    assert response.status_code == 201, response.text

    response_data = response.json()

    assert response_data["name"] == payload["name"]
    assert response_data["email"] == payload["email"]
    assert response_data["mobile"] == payload["mobile"]
    assert "password" not in response_data


def test_get_missing_user_returns_not_found(
    client: TestClient,
) -> None:
    response = client.get(f"{USERS_URL}/999999999")

    assert response.status_code == 404, response.text
    assert response.json()["detail"] == "User not found"

