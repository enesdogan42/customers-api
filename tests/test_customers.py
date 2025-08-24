from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_create_and_get_customer():
    payload = {
        "full_name": "Ali Kaya",
        "address": "Langestraat 12, Amsterdam",
        "phone": "0612345678",
    }
    r = client.post("/customers", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["full_name"] == payload["full_name"]
    cid = data["id"]

    r2 = client.get(f"/customers/{cid}")
    assert r2.status_code == 200
    assert r2.json()["phone"] == payload["phone"]

def test_list_and_search():
    r = client.get("/customers")
    assert r.status_code == 200
    assert isinstance(r.json()["items"], list)


    r2 = client.get("/customers", params={"phone": "0612345678"})
    assert r2.status_code == 200
    items = r2.json()["items"]
    assert any(x["phone"] == "0612345678" for x in items)

    r3 = client.get("/customers", params={"name": "Ali"})
    assert r3.status_code == 200
    assert any("Ali" in x["full_name"] for x in r3.json()["items"])
