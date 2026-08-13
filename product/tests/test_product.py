from uuid import uuid4

from fastapi.testclient import TestClient
from unittest.mock import Mock

from fastapi.testclient import TestClient

from product.services import product_service

PRODUCTS_URL = "/api/products"
ADMIN_PRODUCTS_URL = "/api/admin/products"


def test_get_products_returns_success(
    client: TestClient,
    monkeypatch,
) -> None:
    mock_service = Mock(return_value=[])

    monkeypatch.setattr(
        product_service,
        "get_all_products",
        mock_service,
    )

    response = client.get(PRODUCTS_URL)

    assert response.status_code == 200
    assert response.json() == []
    mock_service.assert_called_once()


def test_search_products_passes_filters(
    client: TestClient,
    monkeypatch,
) -> None:
    mock_service = Mock(return_value=[])

    monkeypatch.setattr(
        product_service,
        "search_products",
        mock_service,
    )

    response = client.get(
        f"{PRODUCTS_URL}/search",
        params={"name": "keyboard", "category": 1},
    )

    assert response.status_code == 200
    assert response.json() == []

    call_kwargs = mock_service.call_args.kwargs
    assert call_kwargs["name"] == "keyboard"
    assert call_kwargs["category_id"] == 1


def test_get_missing_product_returns_not_found(
    client: TestClient,
    monkeypatch,
) -> None:
    mock_service = Mock(return_value=None)

    monkeypatch.setattr(
        product_service,
        "get_product_by_id",
        mock_service,
    )

    response = client.get(f"{PRODUCTS_URL}/999999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"
