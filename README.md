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

