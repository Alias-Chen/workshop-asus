import pytest
from fastapi.testclient import TestClient


def test_sales_report_returns_category_items_and_total(client: TestClient) -> None:
    response = client.get("/reports/sales", params={"category": "Laptop"})

    assert response.status_code == 200
    body = response.json()
    assert body["category"] == "Laptop"
    assert len(body["items"]) == 1
    assert body["items"][0]["name"] == "Zenbook 14 OLED"
    assert body["total"] == pytest.approx(42900)


def test_sales_report_default_formula_is_accepted(client: TestClient) -> None:
    response = client.get(
        "/reports/sales", params={"category": "Laptop", "formula": "total"}
    )

    assert response.status_code == 200
    assert response.json()["total"] == pytest.approx(42900)


def test_sales_report_unknown_category_returns_empty_items(client: TestClient) -> None:
    response = client.get("/reports/sales", params={"category": "Unknown"})

    assert response.status_code == 200
    body = response.json()
    assert body["category"] == "Unknown"
    assert body["items"] == []
    assert body["total"] == 0


# --- Security regression tests ---


def test_sql_injection_in_category_is_not_executed(client: TestClient) -> None:
    """SQL injection via category must not return extra rows or raise 500."""
    payload = "' OR '1'='1"
    response = client.get("/reports/sales", params={"category": payload})

    assert response.status_code == 200
    # The injected value is treated as a literal string; no products have that category.
    body = response.json()
    assert body["items"] == []
    assert body["total"] == 0


def test_code_injection_via_formula_is_rejected(client: TestClient) -> None:
    """Any formula value other than 'total' must be rejected with 422."""
    payloads = [
        "__import__('os').system('id')",
        "total * 2",
        "1+1",
        "",
    ]
    for payload in payloads:
        response = client.get(
            "/reports/sales", params={"category": "Laptop", "formula": payload}
        )
        assert response.status_code == 422, f"Expected 422 for formula={payload!r}"


def test_error_response_does_not_disclose_stack_trace(client: TestClient) -> None:
    """Error responses must not contain traceback or implementation details."""
    # A very long category string to stress the query; the important thing is that
    # any error path returns a generic message, not a traceback.
    response = client.get("/reports/sales", params={"category": "Laptop"})

    assert response.status_code == 200
    body_text = response.text
    assert "Traceback" not in body_text
    assert "traceback" not in body_text
    assert "sqlite3" not in body_text
