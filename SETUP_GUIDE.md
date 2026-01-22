# 🚀 Quick Setup Guide - Employee Vacation System

## ✅ What's Already Done:

1. **Supabase Connected** ✅
   - URL: `https://qnetdfiqsqznomdnnjgv.supabase.co`
   - API Key: Configured in `.streamlit/secrets.toml`

2. **Email Sender Configured** ✅
   - Sender/Receiver: `awabmhamod88@gmail.com`

3. **Database Schema Ready** ✅
   - All SQL prepared in `database_schema.sql`

---

## 📋 Remaining Steps:

### Step 1: Execute Database Schema (REQUIRED)

**Your browser should have just opened to the Supabase SQL Editor!**

The SQL is already copied to your clipboard. Just:

1. **In the Supabase SQL Editor** (browser window)
2. **Press `Ctrl+V`** to paste the schema
3. **Click the green `RUN` button** (or press Ctrl+Enter)
4. **Wait for "Success"** message (~2-3 seconds)

✅ **This creates:**
- `users` table with demo accounts
- `requests` table for vacation tracking
- All indexes, triggers, and security policies

---

### Step 2: Get Gmail App Password (REQUIRED for email)

To enable email notifications when employees submit requests:

1. **Go to your Google Account:** https://myaccount.google.com/
2. **Navigate to:** Security → 2-Step Verification
3. **Enable 2FA** (if not already enabled)
4. **Go to:** Security → App Passwords
5. **Create new app password:**
   - App: Mail
   - Device: Other (Custom name: "Vacation System")
6. **Copy the 16-character password** (looks like: `xxxx xxxx xxxx xxxx`)

Then update `.streamlit/secrets.toml`:
```toml
EMAIL_APP_PASSWORD = "xxxx xxxx xxxx xxxx"  # Paste your app password here
```

📧 **What this enables:**
- Automatic email to `awabmhamod88@gmail.com` when vacation request is submitted
- Professional HTML-formatted notification emails

---

### Step 3: Run the Application

Once Steps 1 & 2 are complete:

```bash
cd "C:\Users\awabeltarabilly\Downloads\vacation system"
streamlit run app.py
```

The app will open at: `http://localhost:8501`

---

## 🔑 Demo Accounts (Created by SQL Schema)

### Admin Account
- Username: `admin`
- Password: `admin123`
- Can: Approve/reject requests, manage users

### Employee Accounts
- Username: `john.doe` / Password: `password123`
- Username: `jane.smith` / Password: `password123`
- Username: `bob.johnson` / Password: `password123`
- Can: Submit vacation requests, view balance

---

## 🎯 Testing Workflow

1. **Login as employee** (`john.doe` / `password123`)
2. **Submit a vacation request** (e.g., 3 days)
3. **Check email** at `awabmhamod88@gmail.com` (notification should arrive)
4. **Logout** and **login as admin** (`admin` / `admin123`)
5. **Approve the request** (employee balance will decrease)
6. **Login as employee again** (verify balance updated)

---

## ⚠️ Important Notes

**Email will NOT work until you complete Step 2** (Gmail App Password)
- The app will still work for viewing/submitting requests
- Email notifications will fail silently without the app password
- Requests are still saved to database even if email fails

**Change passwords in production!**
- The demo accounts use hardcoded bcrypt hashes
- For production, create new accounts with secure passwords

---

## 🆘 Troubleshooting

### "Connection Error" on startup
→ Database tables not created yet. Complete Step 1 (run SQL in Supabase)

### "Email failed to send"
→ Gmail App Password not configured. Complete Step 2

### "Invalid username or password"
→ Make sure database is set up (Step 1) and using correct demo credentials

---

## 📁 Project Files

```
vacation system/
├── app.py                    # Main application
├── database_schema.sql       # SQL to execute in Supabase
├── setup_database.py         # Helper script (already ran)
├── requirements.txt          # Dependencies
├── .streamlit/secrets.toml   # Your credentials (configured)
├── README.md                 # Full documentation
└── setup.bat                 # Windows setup script
```

---

## ✅ Current Status

| Component | Status |
|-----------|--------|
| Supabase URL | ✅ Configured |
| Supabase API Key | ✅ Configured |
| Email Sender | ✅ Configured (awabmhamod88@gmail.com) |
| Database Tables | ⏳ Needs Step 1 (paste SQL & run) |
| Email App Password | ⏳ Needs Step 2 (get from Google) |

**After completing Steps 1 & 2, you're ready to run the app!**

🚀 Run: `streamlit run app.py`
