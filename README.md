# Khidmat.net — Vercel-ready Django app

Khidmat.net connects donors with people who need essential goods.

## Local setup (Windows PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Vercel deployment

1. Push this folder to GitHub.
2. Import the repository into Vercel.
3. Add a PostgreSQL database to the Vercel project (or use another managed PostgreSQL provider).
4. Add these environment variables:
   - `DJANGO_SECRET_KEY` — strong random secret
   - `DEBUG` — `False`
   - `ALLOWED_HOSTS` — `.vercel.app,your-domain.com`
   - `CSRF_TRUSTED_ORIGINS` — `https://*.vercel.app,https://your-domain.com`
   - `DATABASE_URL` — PostgreSQL connection string
5. Deploy.

`vercel.json` runs `collectstatic` and `migrate` during deployment.

Do not commit `.env` or production secrets. PostgreSQL is used in production; SQLite remains the local fallback.

Create an admin user locally with `python manage.py createsuperuser`; the admin is at `/admin/`.
