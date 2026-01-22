# 🏖️ Employee Vacation Management System

A production-ready vacation management system built with **Streamlit** and **Supabase** (PostgreSQL). Features include employee vacation requests, admin approval workflows, email notifications, and secure authentication.

## ✨ Features

### For Employees
- 📊 **Real-time Vacation Balance** - View available, used, and total vacation days
- 📝 **Submit Vacation Requests** - Easy-to-use form with date selection and reason
- ⚡ **Automatic Workday Calculation** - System calculates working days excluding weekends
- 📋 **Request History** - Track all past and current vacation requests with color-coded status

### For Administrators
- 📥 **Pending Request Management** - Review and process all pending vacation requests
- ✅ **Approve/Reject Requests** - One-click approval or rejection with automatic balance updates
- 👥 **User Management** - Update employee vacation allowances
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
- A Supabase account (free tier works fine)
- Gmail account (for email notifications)

### Step 1: Supabase Database Setup

1. **Create a Supabase Project**
   - Go to [supabase.com](https://supabase.com)
   - Click "New Project"
   - Note your project URL and API keys

2. **Run Database Schema**
   - Open your Supabase dashboard
   - Navigate to **SQL Editor**
   - Copy the entire contents of `database_schema.sql`
   - Paste and click "Run"
   - This will create:
     - `users` table
     - `requests` table
     - Indexes and triggers
     - Sample admin and employee accounts

3. **Get Your Credentials**
   - Go to **Project Settings** → **API**
   - Copy your **Project URL** (e.g., `https://xxxxx.supabase.co`)
   - Copy your **anon/public key** (starts with `eyJ...`)

### Step 2: Gmail App Password Setup

For security, Gmail requires an "App Password" instead of your regular password for application access.

1. **Enable 2-Factor Authentication**
   - Go to your Google Account settings
   - Navigate to **Security** → **2-Step Verification**
   - Follow the setup process if not already enabled

2. **Create App Password**
   - Still in Security settings, find **App passwords**
   - Select app: **Mail**
   - Select device: **Other** (enter "Vacation System")
   - Google will generate a 16-character password
   - **IMPORTANT:** Copy this password immediately (you won't see it again)

### Step 3: Local Installation

1. **Clone/Download the Project**
   ```bash
   cd "C:\Users\awabeltarabilly\Downloads\vacation system"
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Secrets**
   - Open `.streamlit/secrets.toml`
   - Replace the placeholder values:
   
   ```toml
   # Supabase Configuration
   SUPABASE_URL = "https://your-project-id.supabase.co"  # Your Supabase project URL
   SUPABASE_KEY = "eyJhbGc..."  # Your Supabase anon key
   
   # Email Configuration (Gmail)
   EMAIL_SENDER_ADDRESS = "your-email@gmail.com"  # Your Gmail address
   EMAIL_APP_PASSWORD = "xxxx xxxx xxxx xxxx"  # Your 16-char app password (with spaces)
   ```

### Step 4: Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

---

## 👤 Demo Accounts

After running the database schema, the following test accounts are available:

### Admin Account
- **Username:** `admin`
- **Password:** `admin123`
- **Permissions:** View/approve requests, manage users

### Employee Accounts
- **Username:** `john.doe` | **Password:** `password123`
- **Username:** `jane.smith` | **Password:** `password123`
- **Username:** `bob.johnson` | **Password:** `password123`

> ⚠️ **IMPORTANT:** Change these default passwords in production! The SQL schema includes bcrypt hashes for these demo accounts.

---

## 📋 How It Works

### Employee Workflow
1. **Login** with employee credentials
2. **View Balance** - See total allowance, used days, and remaining balance
3. **Submit Request** - Select dates and provide a reason
4. **System Calculates** - Automatically counts working days (excluding weekends)
5. **Email Sent** - Admin receives notification at `awabmahmod88@gmail.com`
6. **Track Status** - View request history with color-coded status

### Admin Workflow
1. **Login** with admin credentials
2. **View Pending Requests** - See all employee vacation requests
3. **Review Details** - Check employee, dates, days, and reason
4. **Approve** - Updates request status and deducts days from employee balance
5. **Reject** - Updates request status (no balance change)
6. **Manage Users** - Update employee vacation allowances as needed

### Email Notification
When an employee submits a request:
- Email automatically sent to: `awabmahmod88@gmail.com`
- Subject: `"New Vacation Request from [Employee Name]"`
- Body: Includes employee name, dates, days, and reason
- Styled HTML format for professional appearance

---

## 🗄️ Database Schema

### `users` Table
```sql
- id (UUID, Primary Key)
- username (VARCHAR, Unique)
- password_hash (TEXT)
- role (VARCHAR: 'admin' or 'employee')
- total_allowance (INTEGER)
- balance (INTEGER)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
```

### `requests` Table
```sql
- id (UUID, Primary Key)
- user_id (UUID, Foreign Key to users)
- start_date (DATE)
- end_date (DATE)
- days_taken (INTEGER)
- status (VARCHAR: 'Pending', 'Approved', 'Rejected')
- reason (TEXT)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
```

---

## 🔧 Configuration Details

### Secrets Configuration
All sensitive credentials are stored in `.streamlit/secrets.toml`:

| Key | Description | Example |
|-----|-------------|---------|
| `SUPABASE_URL` | Your Supabase project URL | `https://abc123.supabase.co` |
| `SUPABASE_KEY` | Supabase anonymous/public key | `eyJhbGciOiJIUzI1NiIsInR5cCI6...` |
| `EMAIL_SENDER_ADDRESS` | Gmail address for sending notifications | `yourapp@gmail.com` |
| `EMAIL_APP_PASSWORD` | Gmail App Password (16 characters) | `abcd efgh ijkl mnop` |

### Performance Optimization
- **Connection Caching:** Supabase client is cached using `@st.cache_resource`
- **Efficient Queries:** Indexed database queries for fast retrieval
- **Session Management:** Minimal database calls by caching user data in session

---

## 🚢 Deployment Options

### Streamlit Cloud (Recommended)

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Select `app.py` as the main file
   - Add secrets in the dashboard:
     - Click "Advanced settings"
     - Paste your `secrets.toml` content

3. **Your app is live!** 🎉

### Other Deployment Options
- **Heroku:** Use the provided `requirements.txt`
- **AWS/GCP/Azure:** Deploy as a containerized application
- **On-Premise:** Run on internal servers with VPN access

---

## 🔒 Security Best Practices

1. **Change Default Passwords**
   - Immediately update demo account passwords
   - Use strong, unique passwords for all users

2. **Environment Variables**
   - Never commit `secrets.toml` to version control
   - Add `.streamlit/secrets.toml` to `.gitignore`

3. **Supabase RLS**
   - The schema includes Row Level Security policies
   - Additional authorization is handled in the application layer

4. **Email Security**
   - Use Gmail App Passwords (never your actual password)
   - Consider using a dedicated service account

5. **HTTPS in Production**
   - Always use HTTPS for deployed applications
   - Streamlit Cloud provides this automatically

---

## 📧 Email Notification Details

### Gmail SMTP Configuration
- **Server:** `smtp.gmail.com`
- **Port:** `465` (SSL)
- **Authentication:** App Password required

### Email Template
The system sends professional HTML emails with:
- Clear subject line with employee name
- Formatted employee details
- Request dates and reason
- Professional styling with colors and layout

### Troubleshooting Email Issues
If emails aren't sending:
1. Verify Gmail App Password is correct (16 characters)
2. Ensure 2-Factor Authentication is enabled on Gmail
3. Check that the sender email exists in secrets
4. Review Streamlit error messages for SMTP errors

---

## 🛠️ Troubleshooting

### "Connection Error" on Startup
- Verify `SUPABASE_URL` and `SUPABASE_KEY` in secrets.toml
- Check that your Supabase project is active

### "Email Failed to Send"
- Confirm Gmail App Password is correct
- Ensure 2FA is enabled on your Google account
- Check that `EMAIL_SENDER_ADDRESS` matches your Gmail

### "Insufficient Balance" Error
- Employees can only request up to their available balance
- Admins can update allowances in User Management tab

### Database Queries Not Working
- Ensure all SQL schema commands ran successfully
- Check Supabase logs for error messages
- Verify RLS policies are enabled

---

## 📝 Customization

### Change Admin Email
Edit line 52 in `app.py`:
```python
admin_email = "your-new-admin@email.com"
```

### Modify Vacation Allowance Defaults
Edit database_schema.sql line 12:
```sql
total_allowance INTEGER NOT NULL DEFAULT 21,  -- Change 21 to desired default
```

### Customize Email Template
Edit the HTML in the `send_email_notification()` function (lines 72-103 in app.py)

### Add More Employee Fields
- Update database schema to add columns
- Modify `employee_dashboard()` to display new fields
- Update forms to collect additional information

---

## 📊 Future Enhancements

Potential features to add:
- 📱 **Mobile Responsive UI** - Optimize for mobile devices
- 📅 **Calendar View** - Visual calendar of approved vacations
- 📈 **Analytics Dashboard** - Vacation usage statistics
- 🔔 **In-App Notifications** - Real-time notification system
- 📤 **Export Reports** - Download vacation reports as PDF/Excel
- 👥 **Team View** - See team members' vacation schedules
- 🌐 **Multi-language Support** - Internationalization
- 📨 **Email to Employee** - Notify employee when request is approved/rejected

---

## 📄 License

This project is provided as-is for educational and commercial use.

---

## 🤝 Support

For questions or issues:
- Check the troubleshooting section above
- Review Supabase and Streamlit documentation
- Verify all configuration steps were completed

---

**Built with ❤️ using Streamlit and Supabase**
