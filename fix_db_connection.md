# Quick Fix for 500 Internal Server Error

## The Problem
Your API is showing 500 errors because the database connection is failing. The error is:
```
Access denied for user 'soulnest'@'localhost' (using password: YES)
```

## Solution Steps

### Step 1: Check Your .env File
Open `.env` in your project root and check the `DATABASE_URL`. It should look like:
```
DATABASE_URL=mysql+aiomysql://USERNAME:PASSWORD@localhost:3306/soulnest_db
```

### Step 2: Choose Your Fix

#### Option A: Use Root User (Easiest)
1. Update `.env`:
   ```
   DATABASE_URL=mysql+aiomysql://root:YOUR_ROOT_PASSWORD@localhost:3306/soulnest_db
   ```
2. Replace `YOUR_ROOT_PASSWORD` with your actual MySQL root password
3. Restart the server

#### Option B: Create/Fix the 'soulnest' User
1. Open MySQL Workbench or command line
2. Connect as root
3. Run these SQL commands:
   ```sql
   -- Create the user (if it doesn't exist)
   CREATE USER IF NOT EXISTS 'soulnest'@'localhost' IDENTIFIED BY 'admin';
   
   -- Grant permissions
   GRANT ALL PRIVILEGES ON soulnest_db.* TO 'soulnest'@'localhost';
   
   -- Apply changes
   FLUSH PRIVILEGES;
   ```
4. If user already exists but password is wrong:
   ```sql
   ALTER USER 'soulnest'@'localhost' IDENTIFIED BY 'admin';
   FLUSH PRIVILEGES;
   ```

### Step 3: Test the Connection
Run the test script:
```powershell
.\venv\Scripts\python.exe test_db_connection.py
```

You should see "✓ All tests passed!"

### Step 4: Restart Your Server
```powershell
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8002
```

### Step 5: Test the API
Try these endpoints:
- Health: http://127.0.0.1:8002/api/health
- Products: http://127.0.0.1:8002/api/products
- Featured: http://127.0.0.1:8002/api/products/featured
- Bestsellers: http://127.0.0.1:8002/api/products/bestsellers

## Still Getting Errors?

If you still get 500 errors after fixing the connection:
1. Check the server console output - it will now show the actual error message
2. Make sure the database `soulnest_db` exists
3. Make sure the tables are created (run the seed SQL file)
4. Check that products exist in the database

