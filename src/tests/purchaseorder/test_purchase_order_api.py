import pytest
import requests
import random
import string
import decimal

BASE_URL = "http://localhost:3000"  # Adjust if your serverless-offline runs on a different port

# Helper to generate random PO numbers and data
def random_po_data():
    return {
        "supplierName": random.choice(["Salman", "Ravi", "Sohail", "Uttam"]),
        "deliveryDate": "2024-08-{:02d}".format(random.randint(10, 28)),
        "items": [
            {
                "itemCode": ''.join(random.choices(string.ascii_uppercase, k=5)),
                "itemName": "Item-{}".format(random.randint(1, 100)),
                "category": random.choice(["A", "B", "C"]),
                "unit": "kg",
                "quantity": random.randint(1, 100)
            }
        ],
        "notes": "Test PO",
        "shipTo": "Test Address",
        "paymentTerm": "Net 30"
    }

@pytest.fixture(scope="module")
def po_numbers():
    return []

def test_create_20_purchase_orders(po_numbers):
    for _ in range(20):
        resp = requests.post(f"{BASE_URL}/purchase-orders", json=random_po_data())
        assert resp.status_code == 201
        data = resp.json()
        assert "poNumber" in data
        po_numbers.append(data["poNumber"])


def test_list_purchase_orders(po_numbers):
    resp = requests.get(f"{BASE_URL}/purchase-orders")
    assert resp.status_code == 200
    data = resp.json()
    assert "data" in data
    # There may be more than 20 if table is not empty, but at least 20
    assert len(data["data"]) >= 20


def test_update_some_purchase_orders(po_numbers):
    for po in po_numbers[:3]:
        update_data = {"status": "Confirmed", "notes": "Updated by test"}
        resp = requests.put(f"{BASE_URL}/purchase-orders/{po}", json=update_data)
        assert resp.status_code == 200
        updated = resp.json()
        assert updated.get("status") == "Confirmed"


def test_delete_two_purchase_orders(po_numbers):
    for po in po_numbers[:2]:
        resp = requests.delete(f"{BASE_URL}/purchase-orders/{po}")
        assert resp.status_code == 204


def test_get_deleted_purchase_orders(po_numbers):
    for po in po_numbers[:2]:
        resp = requests.get(f"{BASE_URL}/purchase-orders/{po}")
        assert resp.status_code == 404


def test_get_existing_purchase_orders(po_numbers):
    for po in po_numbers[2:5]:
        resp = requests.get(f"{BASE_URL}/purchase-orders/{po}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["poNumber"] == po

def convert_decimal(obj):
    if isinstance(obj, list):
        return [convert_decimal(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_decimal(v) for k, v in obj.items()}
    elif isinstance(obj, decimal.Decimal):
        if obj % 1 == 0:
            return int(obj)
        else:
            return float(obj)
    else:
        return obj

def api_response(status_code, body):
    import json
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(convert_decimal(body))
    } 