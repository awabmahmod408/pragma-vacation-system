# 🏖️ Employee Vacation Management System

A production-ready vacation management system built with **Streamlit** and **Supabase** (PostgreSQL). Features include employee vacation requests, admin approval workflows, email notifications, and secure authentication.

## ✨ Features

### For Employees
- 📊 **Real-time Vacation Balance** - View available, used, and total vacation days
- 📝 **Submit Vacation Requests** - Easy-to-use form with date selection and reason
- ⚡ **Automatic Workday Calculation** - System calculates working days excluding weekends (Sun-Thu)
- 📋 **Request History** - Track all past and current vacation requests with color-coded status

### For Administrators
- 📥 **Pending Request Management** - Review and process all pending vacation requests
- ✅ **Approve/Reject Requests** - One-click approval or rejection with automatic balance updates
- 👥 **User Management** - Full CRUD for creating, editing, and deleting users (admins & employees)
- 📋 **Audit Logs** - Track all system activities with downloadable TXT and CSV reports
- 📧 **Email Notifications** - Automatic email alerts for new vacation requests

### Security & Performance
- 🔒 **Secure Authentication** - Password hashing with bcrypt
- 🔐 **Session Management** - Secure user sessions with Streamlit session state
- ⚡ **Database Connection Caching** - Optimized Supabase connection pooling
- 🛡️ **Row Level Security (RLS)** - Additional database-level security

---

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8 or higher
- A Supabase account
- Gmail account (for email notifications)

### Step 1: Supabase Database Setup

1. **Create a Supabase Project**
   - Go to [supabase.com](https://supabase.com)
   - Click "New Project"

2. **Run Database Schema**
   - Copy the contents of `database_schema.sql` into the Supabase SQL Editor and run it.
   - Run `audit_log_schema.sql` to enable the audit logging system.

3. **Get Your Credentials**
   - Copy your **Project URL** and **anon/public key** from Project Settings.

### Step 2: Local Installation

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Secrets**
   - Create `.streamlit/secrets.toml` with your credentials:
   
   ```toml
   SUPABASE_URL = "https://your-project.supabase.co"
   SUPABASE_KEY = "your-anon-key"
   EMAIL_SENDER_ADDRESS = "your-email@gmail.com"
   EMAIL_APP_PASSWORD = "xxxx xxxx xxxx xxxx"
   ```

### Step 3: Run the Application

```bash
streamlit run app.py
```

---

## 👤 Demo Accounts
- **Admin:** `admin` / `admin123`
- **Employee:** `john.doe` / `password123`

---

## 📄 License
This project is provided as-is for educational and commercial use.

**Built with ❤️ using Streamlit and Supabase**
