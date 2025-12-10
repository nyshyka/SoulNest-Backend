# SoulNest Backend Setup Guide

## Issues Found

1. **500 Internal Server Error**: The backend is running, but the database is either:
   - Not created yet
   - Not seeded with tables and data
   - Connection string is misconfigured

2. **MySQL Status**: MySQL is running (confirmed), but you need to:
   - Create the database
   - Seed it with the schema and initial data

## Step-by-Step Fix

### Step 1: Verify MySQL is Running
MySQL is already running (process ID found). Good! ✅

### Step 2: Check Your .env File
Make sure your `.env` file in the backend directory has the correct database connection string:

```env
DATABASE_URL=mysql+aiomysql://username:password@localhost:3306/soulnest_db
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

**Important**: Replace `username` and `password` with your actual MySQL credentials (usually `root` and your MySQL root password).

### Step 3: Create and Seed the Database

You have several options:

#### Option A: Using MySQL Command Line (if mysql is in your PATH)

1. Find where MySQL is installed (usually `C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe`)
2. Run:
```bash
mysql -u root -p < seeds/mysql_seed.sql
```

#### Option B: Using MySQL Workbench or phpMyAdmin

1. Open MySQL Workbench or phpMyAdmin
2. Connect to your MySQL server
3. Open the file `seeds/mysql_seed.sql`
4. Execute it

#### Option C: Using Python Script (Easiest)

I've created a script that will do this for you - see the next steps.

### Step 4: Verify the Backend is Running

Make sure your backend server is running:
```bash
cd "SoulNest Backend"
.\venv\Scripts\activate
uvicorn app.main:app --reload
```

### Step 5: Test the API

After setting up the database, test the endpoint:
```bash
curl http://127.0.0.1:8000/api/health
curl http://127.0.0.1:8000/api/products/bestsellers
```

## Quick Troubleshooting

### If you get "Access denied" error:
- Check your MySQL username and password in the `.env` file
- Make sure MySQL root user has the correct permissions

### If you get "Database does not exist" error:
- Run the seed script to create the database

### If you get "Table does not exist" error:
- The database exists but isn't seeded. Run the seed script again.

### Finding MySQL Installation

On Windows, MySQL is usually installed at:
- `C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe`
- Or check: `C:\ProgramData\MySQL\MySQL Server 8.0\`

You can add it to your PATH or use the full path to the mysql.exe file.





