# SoulNest Backend (FastAPI)

FastAPI backend for the SoulNest wellness e-commerce platform. Async SQLAlchemy with MySQL (aiomysql), JWT auth, and comprehensive REST endpoints.

## Quickstart

1. Create and activate a virtual environment (recommended)
2. Install dependencies:

```
pip install -r requirements.txt
```

3. Create the database and seed (MySQL):

```
# Update credentials in the SQL or use env vars
mysql -u <user> -p < seeds/mysql_seed.sql
```

4. Set environment variables and run:

```
set DATABASE_URL=mysql+aiomysql://username:password@localhost:3306/soulnest_db
set JWT_SECRET_KEY=your-secret-key-change-in-production
set JWT_ALGORITHM=HS256
set JWT_EXPIRATION_HOURS=24
set CORS_ORIGINS=http://localhost:3000,http://localhost:3001

uvicorn app.main:app --reload
```

On Linux/macOS, replace `set` with `export`.

## Project Structure

```
app/
  core/
    config.py
  db/
    session.py
  models/
    __init__.py
  schemas/
    __init__.py
  routers/
    __init__.py
  utils/
    security.py
  main.py
seeds/
  mysql_seed.sql
requirements.txt
README.md
```

## Notes
- Uses async SQLAlchemy with `aiomysql` driver.
- JWT tokens (24h expiry) via `python-jose` and `passlib[bcrypt]`.
- CORS configured via env `CORS_ORIGINS` (comma-separated).
- All endpoints are under `/api/*` and a health check at `/api/health`.

