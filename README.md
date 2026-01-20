## Simple E‑commerce Store (Django + HTML/CSS/JS)

Features:
- **Product listing** + **product detail page**
- **Shopping cart** (stored in session)
- **Order processing** (creates `Order` + `OrderItem` in SQLite)
- **User registration/login** (Django auth)

### Run locally (Windows / PowerShell)

Install deps:

```powershell
pip install -r requirements.txt
```

Create DB + admin user:

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

Seed demo products:

```powershell
python manage.py seed_demo
```

Start server:

```powershell
python manage.py runserver
```

Open:
- Store: `http://127.0.0.1:8000/`
- Admin: `http://127.0.0.1:8000/admin/` (manage products + orders)

### Deploy on Vercel (important)
Vercel serverless runtime has a **read-only filesystem**, so **SQLite cannot be used in production**.

What this repo does:
- Uses `api/index.py` + `vercel.json` so Vercel can run Django.
- Uses **cookie-based sessions** by default (so requests don’t try to write session rows to SQLite).

For a real deployment with products/orders/users persistence, you must use Postgres (recommended):
- Create a Postgres database (Vercel Postgres / Neon / Supabase)
- Set env var on Vercel:
  - `DATABASE_URL` = your Postgres connection string
  - `SECRET_KEY` = a strong random string
  - (optional) `DEBUG` = `0`

