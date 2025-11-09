# Quick Fix for 500 Internal Server Error

## What's Wrong?
Your backend server is running ✅, MySQL is running ✅, but the **database doesn't exist or isn't seeded** with tables. That's why you're getting 500 errors when the API tries to query the database.

## The Fix (Choose One Method)

### Method 1: Using the Batch Script (Easiest for Windows)

1. Open Command Prompt or PowerShell
2. Navigate to the backend directory:
   ```bash
   cd "C:\moi\SoulNest Backend"
   ```
3. Run the setup script:
   ```bash
   setup_db.bat
   ```
4. Enter your MySQL root password when prompted
5. Done! The database will be created and seeded

### Method 2: Manual MySQL Command

1. Find your MySQL installation (usually at `C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe`)
2. Open Command Prompt
3. Run:
   ```bash
   "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p < seeds\mysql_seed.sql
   ```
   (Replace the path with your actual MySQL path)
4. Enter your MySQL root password

### Method 3: Using MySQL Workbench

1. Open MySQL Workbench
2. Connect to your MySQL server
3. Go to File → Open SQL Script
4. Open `seeds/mysql_seed.sql`
5. Click the Execute button (⚡)
6. Done!

### Method 4: Using phpMyAdmin (if you have XAMPP/WAMP)

1. Open phpMyAdmin in your browser (usually http://localhost/phpmyadmin)
2. Click on "SQL" tab
3. Copy and paste the contents of `seeds/mysql_seed.sql`
4. Click "Go"
5. Done!

## After Setup

1. **Verify your .env file** has the correct database URL:
   ```env
   DATABASE_URL=mysql+aiomysql://root:YOUR_PASSWORD@localhost:3306/soulnest_db
   ```
   (Replace `YOUR_PASSWORD` with your actual MySQL root password)

2. **Restart your backend server** (if it's running):
   - Stop it (Ctrl+C)
   - Start it again: `uvicorn app.main:app --reload`

3. **Test the API**:
   ```bash
   curl http://127.0.0.1:8000/api/health
   curl http://127.0.0.1:8000/api/products/bestsellers
   ```

## Still Having Issues?

### Error: "Access denied for user"
- Check your MySQL username and password in the `.env` file
- Make sure the user has permission to create databases

### Error: "Can't connect to MySQL server"
- Make sure MySQL is running
- Check the port (default is 3306)
- Verify the host is `localhost` or `127.0.0.1`

### Error: "Unknown database"
- The database name in your `.env` file doesn't match
- Default database name should be: `soulnest_db`

## Summary

**Yes, you need to make MySQL "live" by:**
1. ✅ Making sure MySQL service is running (already done!)
2. ⚠️ Creating the database (you need to do this)
3. ⚠️ Seeding it with tables and data (you need to do this)

Once you run the seed script, your 500 errors should be fixed!

