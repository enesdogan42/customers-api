# Customers API (FastAPI + SQLite)

Deze repo bevat een  **RESTful API** als onderdeel van de KPN Tech Talent Program opdracht.  
De API beheert `Customer` resources met velden: `id`, `full_name`, `address`, `phone`.

Gebouwd met **FastAPI**, **SQLite**, **SQLAlchemy**, **Pydantic** en getest met **Pytest**.

--------------------------

## Functionaliteit
- CRUD op klanten:
  - `POST /customers` → klant aanmaken
  - `GET /customers` → lijst van klanten, incl. zoekfilters
  - `GET /customers/{id}` → klant ophalen
  - `PATCH /customers/{id}` → klant bijwerken
  - `DELETE /customers/{id}` → klant verwijderen
- **Zoeken**:
  - `?phone=` → exact telefoonnummer
  - `?name=` → deel van `full_name` (case-insensitive)
- **Paginatie**:  
  Response structuur:
  ```json
  {
    "items": [...],
    "page": { "total": 23, "limit": 10, "offset": 0 }
  }
  ```
- Health check: `GET /health`

---

## Installatie
```bash
git clone <repo-url>
cd customers-api

python -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## Runnen
```bash
python -m uvicorn app.main:app --reload
```
Open daarna **http://127.0.0.1:8000/docs** voor de Swagger UI.

---

## Testen
- Via **pytest**:
  ```bash
  PYTHONPATH=. pytest -q
  ```
- Via **Swagger UI**:
  1. `POST /customers` → maak een klant
  2. `GET /customers` → check lijst
  3. `GET /customers?name=Ali` → zoek op naam
  4. `PATCH /customers/{id}` → pas adres aan
  5. `DELETE /customers/{id}` → verwijder klant

- Curl voorbeeld:
  ```bash
  curl -X POST "http://127.0.0.1:8000/customers"     -H "Content-Type: application/json"     -d '{"full_name":"Ali Kaya","address":"Dam 1, Amsterdam","phone":"0611111111"}'
  ```

---

## Extra keuzes & toevoegingen
- **Unieke constraint** op telefoonnummer (`phone`).
- **Zoekfunctionaliteit** uitgebreid met `name` (case-insensitive LIKE).
- **Paginatie** toegevoegd (`limit`, `offset`, en `total` in response).
- **Tests** geschreven voor health check, create/get, search.
- Klaar voor uitbreidingen (bv. bulk create of auth).

---

## Projectstructuur
```
app/
 ├── main.py        # API-routes
 ├── db.py          # DB-engine & sessies
 ├── models.py      # SQLAlchemy models
 ├── schemas.py     # Pydantic schemas
 ├── crud.py        # CRUD-functies
 └── deps.py        # Dependencies
tests/
 └── test_customers.py
```


© 2025 Enes Doğan — KPN Tech Talent Program opdracht
