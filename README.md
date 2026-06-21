# ModaCol Django App

This project is a Django application prepared for deployment on Railway.

## Deploying to Railway

1. Push your repository to GitHub or another git host.
2. Create a new Railway project and connect the repository.
3. Add environment variables:
   - `DJANGO_SECRET_KEY`: a secret value.
   - `DJANGO_DEBUG`: `False`.
   - `DJANGO_ALLOWED_HOSTS`: your Railway host, for example `yourapp.up.railway.app`.
   - `DATABASE_URL`: provided by Railway Postgres addon.
   - `EMAIL_BACKEND` (optional)
   - `EMAIL_HOST` (optional)
   - `EMAIL_PORT` (optional)
   - `EMAIL_USE_TLS` (optional)
   - `EMAIL_HOST_USER` (optional)
   - `EMAIL_HOST_PASSWORD` (optional)
   - `DEFAULT_FROM_EMAIL` (optional)

4. Railway will use the existing `Procfile`:
   - `web: gunicorn ModaCol.wsgi:application`

5. Verify build and run commands:
   - Build: `pip install -r requirements.txt`
   - Migrate: `python manage.py migrate`
   - Collect static: `python manage.py collectstatic --noinput`

## Local setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver
```

## Notes

- This project uses `WhiteNoise` for static files.
- `DATABASE_URL` support is enabled in `ModaCol/settings.py`.
- Do not commit `.venv`, `db.sqlite3`, or `staticfiles/`.
