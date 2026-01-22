import streamlit as st
import bcrypt
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from supabase_simple import create_client, SupabaseClient
import pandas as pd
from typing import Optional
import numpy as np
from audit_logger import log_activity, generate_audit_report_txt, generate_audit_report_csv

# ===========================
# Configuration & Setup
# ===========================

st.set_page_config(
    page_title="Vacation Management System",
    page_icon="🏖️",
    layout="wide"
)

# Hide Streamlit header/toolbar
st.markdown("""
    <style>
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Initialize Supabase client with caching
@st.cache_resource
def init_supabase() -> SupabaseClient:
    """Initialize and cache Supabase client connection."""
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_supabase()

# ===========================
# Utility Functions
# ===========================

def calculate_workdays(start_date, end_date) -> int:
    """
    Calculate number of working days between two dates.
    Working days: Sunday to Thursday (Middle Eastern work week)
    Weekend: Friday and Saturday
    """
    if start_date > end_date:
        return 0
    
    workdays = 0
    current_date = start_date
    
    while current_date <= end_date:
        # weekday(): Monday=0, Tuesday=1, Wednesday=2, Thursday=3, Friday=4, Saturday=5, Sunday=6
        # Working days: Sunday(6), Monday(0), Tuesday(1), Wednesday(2), Thursday(3)
        # Weekend: Friday(4), Saturday(5)
        if current_date.weekday() not in [4, 5]:  # Exclude Friday and Saturday
            workdays += 1
        current_date += timedelta(days=1)
    
    return workdays

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def send_email_notification(employee_name: str, start_date: str, end_date: str, reason: str, days_taken: int, unbillable_days: int = 0) -> bool:
    """
    Send email notification to multiple admins when a new vacation request is submitted.
    """
    try:
        # Get email credentials from secrets
        sender_email = st.secrets["EMAIL_SENDER_ADDRESS"]
        sender_password = st.secrets["EMAIL_APP_PASSWORD"]
        
        # List of admin emails to notify
        admin_emails = ["awabmahmod88@gmail.com", "yaramahmood1890@gmail.com"]
        
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = f"New Vacation Request from {employee_name}"
        message["From"] = sender_email
        message["To"] = ", ".join(admin_emails)
        
        # Create HTML body
        html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
                    <h2 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px;">
                        🏖️ New Vacation Request
                    </h2>
                    <div style="margin: 20px 0;">
                        <p><strong>Employee:</strong> {employee_name}</p>
                        <p><strong>Start Date:</strong> {start_date}</p>
                        <p><strong>End Date:</strong> {end_date}</p>
                        <p><strong>Total Days:</strong> {days_taken}</p>
                        {"<p style='color: #e74c3c;'><strong>Unbillable Days:</strong> " + str(unbillable_days) + "</p>" if unbillable_days > 0 else ""}
                        <p><strong>Reason:</strong></p>
                        <p style="background-color: #f8f9fa; padding: 10px; border-left: 3px solid #3498db;">
                            {reason}
                        </p>
                    </div>
                    <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
                        <p style="color: #7f8c8d; font-size: 12px;">
                            This is an automated notification from the Employee Vacation Management System.
                            Please log in to the admin dashboard to approve or reject this request.
                        </p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        # Attach HTML content
        part = MIMEText(html, "html")
        message.attach(part)
        
        # Send email using Gmail SMTP
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            # sendmail takes a list of recipients for the envelope
            server.sendmail(sender_email, admin_emails, message.as_string())
        
        return True
    
    except Exception as e:
        st.error(f"Failed to send email notification: {str(e)}")
        return False

def send_status_update_email(employee_email: str, employee_name: str, start_date: str, end_date: str, status: str, unbillable_days: int = 0) -> bool:
    """
    Send email notification to employee when their vacation request is approved or rejected.
    """
    if not employee_email:
        return False
        
    try:
        sender_email = st.secrets["EMAIL_SENDER_ADDRESS"]
        sender_password = st.secrets["EMAIL_APP_PASSWORD"]
        
        message = MIMEMultipart("alternative")
        message["Subject"] = f"Vacation Request {status}: {start_date} to {end_date}"
        message["From"] = sender_email
        message["To"] = employee_email
        
        color = "#27ae60" if status == "Approved" else "#e74c3c"
        icon = "✅" if status == "Approved" else "❌"
        
        html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
                    <h2 style="color: {color}; border-bottom: 2px solid {color}; padding-bottom: 10px;">
                        {icon} Vacation Request {status}
                    </h2>
                    <div style="margin: 20px 0;">
                        <p>Hello {employee_name},</p>
                        <p>Your vacation request for the following period has been <strong>{status.lower()}</strong>:</p>
                        <p style="background-color: #f8f9fa; padding: 10px; border-left: 3px solid {color};">
                            <strong>Dates:</strong> {start_date} to {end_date}
                            {f"<br><strong>Unbillable Days:</strong> {unbillable_days}" if unbillable_days > 0 else ""}
                        </p>
                        <p>Please log in to the system to view your updated balance and history.</p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        part = MIMEText(html, "html")
        message.attach(part)
        
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, employee_email, message.as_string())
            
        return True
    except Exception as e:
        st.error(f"Failed to send status update email: {str(e)}")
        return False

# ===========================
# Authentication Functions
# ===========================

def login_user(username: str, password: str) -> Optional[dict]:
    """
    Authenticate user and return user data if successful.
    
    Args:
        username: Username
        password: Plain text password
    
    Returns:
        User data dict if successful, None otherwise
    """
    try:
        response = supabase.table("users").select("*").eq("username", username).execute()
        
        if response.data and len(response.data) > 0:
            user = response.data[0]
            if verify_password(password, user['password_hash']):
                # Log successful login
                log_activity(supabase, user['id'], username, "LOGIN", f"User logged in successfully")
                return user
        
        return None
    
    except Exception as e:
        st.error(f"Login error: {str(e)}")
        return None

def logout_user():
    """Clear session state to log out user."""
    for key in list(st.session_state.keys()):
        del st.session_state[key]

def recalculate_pending_requests(supabase, user_id, current_balance):
    """
    Recalculate unbillable days for all pending requests of a user
    when their allowance/balance is updated by an admin.
    """
    try:
        # Fetch pending requests
        response = supabase.table("requests").select("*").eq("user_id", user_id).eq("status", "Pending").order("created_at", desc=False).execute()
        
        if response and response.data:
            for request in response.data:
                days_taken = request['days_taken']
                # Recalculate based on the balance at that moment
                new_unbillable = max(0, days_taken - current_balance)
                
                # Update if changed
                if new_unbillable != request.get('unbillable_days', 0):
                    supabase.table("requests").update({"unbillable_days": new_unbillable}).eq("id", request['id']).execute()
    except Exception as e:
        # Silent error in UI but log to session
        print(f"Error recalculating pending requests: {str(e)}")

# ===========================
# Employee Dashboard
# ===========================

def employee_dashboard():
    """Display employee dashboard with vacation balance and request form."""
    user_id = st.session_state.user['id']
    username = st.session_state.user['username']
    
    st.title(f"🏖️ Welcome, {username}!")
    
    # Fetch current balance
    try:
        response = supabase.table("users").select("balance, total_allowance").eq("id", user_id).execute()
        balance = response.data[0]['balance']
        total_allowance = response.data[0]['total_allowance']
    except Exception as e:
        st.error(f"Error fetching balance: {str(e)}")
        return
    
    # Display balance
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Allowance", f"{total_allowance} days")
    with col2:
        st.metric("Current Balance", f"{balance} days", delta=None)
    with col3:
        used_days = total_allowance - balance
        st.metric("Used Days", f"{used_days} days")
    
    st.divider()
    
    # Vacation Request Form
    st.subheader("📝 Submit Vacation Request")
    
    with st.form("vacation_request_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            start_date = st.date_input(
                "Start Date",
                min_value=datetime.now().date(),
                value=datetime.now().date()
            )
        
        with col2:
            end_date = st.date_input(
                "End Date",
                min_value=datetime.now().date(),
                value=datetime.now().date() + timedelta(days=1)
            )
        
        reason = st.text_area("Reason for Leave", placeholder="Please provide a brief reason for your vacation request...")
        
        submitted = st.form_submit_button("Submit Request", type="primary", use_container_width=True)
        
        if submitted:
            if not reason.strip():
                st.error("Please provide a reason for your vacation request.")
            elif start_date > end_date:
                st.error("Start date must be before or equal to end date.")
            else:
                # Calculate workdays
                days_taken = calculate_workdays(start_date, end_date)
                
                # Calculate unbillable days
                unbillable_days = max(0, days_taken - balance)
                
                if days_taken == 0:
                    st.error("The selected date range contains no working days. Please select dates that include at least one working day (Sunday-Thursday).")
                else:
                    if unbillable_days > 0:
                        st.info(f"ℹ️ This request spans {days_taken} days, which exceeds your current balance of {balance} days. **{unbillable_days} days** will be marked as unbillable (unpaid).")
                    
                    # Insert request
                    try:
                        insert_response = supabase.table("requests").insert({
                            "user_id": user_id,
                            "start_date": str(start_date),
                            "end_date": str(end_date),
                            "days_taken": days_taken,
                            "unbillable_days": unbillable_days,
                            "status": "Pending",
                            "reason": reason
                        }).execute()
                        
                        if insert_response.data:
                            # Log vacation request submission
                            unbillable_log = f" ({unbillable_days} unbillable)" if unbillable_days > 0 else ""
                            log_activity(supabase, user_id, username, "REQUEST_CREATE", 
                                       f"Submitted vacation request: {start_date} to {end_date} ({days_taken} days{unbillable_log})")
                            
                            # Send email notification
                            email_sent = send_email_notification(
                                employee_name=username,
                                start_date=str(start_date),
                                end_date=str(end_date),
                                reason=reason,
                                days_taken=days_taken,
                                unbillable_days=unbillable_days
                            )
                            
                            if email_sent:
                                st.success(f"✅ Request submitted successfully! ({days_taken} working days requested)")
                            else:
                                st.warning(f"✅ Request submitted successfully! ({days_taken} working days) - But email notification failed.")
                            
                            st.rerun()
                        else:
                            st.error("Failed to submit request. Please try again.")
                    
                    except Exception as e:
                        st.error(f"Error submitting request: {str(e)}")
    
    st.divider()
    
    # Display request history
    st.subheader("📋 My Request History")
    
    try:
        requests_response = supabase.table("requests").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
        
        if requests_response.data:
            df = pd.DataFrame(requests_response.data)
            
            # Format dataframe for display
            df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M')
            # Handle potential missing unbillable_days in older records
            if 'unbillable_days' not in df.columns:
                df['unbillable_days'] = 0
            
            display_df = df[['start_date', 'end_date', 'days_taken', 'unbillable_days', 'status', 'reason', 'created_at']]
            display_df.columns = ['Start Date', 'End Date', 'Days', 'Unbillable', 'Status', 'Reason', 'Submitted At']
            
            # Color code status
            def highlight_status(row):
                if row['Status'] == 'Approved':
                    return ['background-color: #155724; color: #d4edda'] * len(row)  # Dark green background, light text
                elif row['Status'] == 'Rejected':
                    return ['background-color: #721c24; color: #f8d7da'] * len(row)  # Dark red background, light text
                else:
                    return ['background-color: #856404; color: #fff3cd'] * len(row)  # Dark yellow/orange background, light text
            
            st.dataframe(display_df.style.apply(highlight_status, axis=1), use_container_width=True, hide_index=True)
        else:
            st.info("No requests found. Submit your first vacation request above!")
    
    except Exception as e:
        st.error(f"Error fetching requests: {str(e)}")

# ===========================
# Admin Dashboard
# ===========================

def admin_dashboard():
    """Display admin dashboard with pending requests and user management."""
    st.title("👔 Admin Dashboard")
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["📥 Pending Requests", "👥 User Management", "📋 Audit Logs"])
    
    # Tab 1: Pending Requests
    with tab1:
        st.subheader("Pending Vacation Requests")
        
        try:
            # Fetch pending requests with user info
            requests_response = supabase.table("requests").select("*, users(username, email)").eq("status", "Pending").order("created_at", desc=False).execute()
            
            if requests_response.data:
                for request in requests_response.data:
                    with st.container():
                        col1, col2, col3 = st.columns([3, 1, 1])
                        
                        with col1:
                            st.markdown(f"**Employee:** {request['users']['username']}")
                            unbillable_str = f" ({request.get('unbillable_days', 0)} unbillable)" if request.get('unbillable_days', 0) > 0 else ""
                            st.markdown(f"**Dates:** {request['start_date']} to {request['end_date']} ({request['days_taken']} days{unbillable_str})")
                            st.markdown(f"**Reason:** {request['reason']}")
                            st.caption(f"Submitted: {pd.to_datetime(request['created_at']).strftime('%Y-%m-%d %H:%M')}")
                        
                        with col2:
                            if st.button("✅ Approve", key=f"approve_{request['id']}", use_container_width=True):
                                try:
                                    # Update request status
                                    supabase.table("requests").update({"status": "Approved"}).eq("id", request['id']).execute()
                                    
                                    # Deduct days from user balance
                                    user_response = supabase.table("users").select("balance").eq("id", request['user_id']).execute()
                                    current_balance = user_response.data[0]['balance']
                                    new_balance = current_balance - request['days_taken']
                                    
                                    supabase.table("users").update({"balance": new_balance}).eq("id", request['user_id']).execute()
                                    
                                    # Log approval
                                    admin_user = st.session_state.user
                                    unbillable_days_val = request.get('unbillable_days', 0)
                                    unbillable_log = f" ({unbillable_days_val} unbillable)" if unbillable_days_val > 0 else ""
                                    log_activity(supabase, admin_user['id'], admin_user['username'], "REQUEST_APPROVE",
                                               f"Approved {request['users']['username']}'s request for {request['days_taken']} days ({request['start_date']} to {request['end_date']}{unbillable_log})")
                                    
                                    # Send status update email to employee
                                    employee_email = request['users'].get('email')
                                    if employee_email:
                                        send_status_update_email(
                                            employee_email=employee_email,
                                            employee_name=request['users']['username'],
                                            start_date=request['start_date'],
                                            end_date=request['end_date'],
                                            status="Approved",
                                            unbillable_days=request.get('unbillable_days', 0)
                                        )
                                    
                                    st.success(f"Request approved! Balance updated: {current_balance} → {new_balance} days")
                                    st.rerun()
                                
                                except Exception as e:
                                    st.error(f"Error approving request: {str(e)}")
                        
                        with col3:
                            if st.button("❌ Reject", key=f"reject_{request['id']}", use_container_width=True):
                                try:
                                    supabase.table("requests").update({"status": "Rejected"}).eq("id", request['id']).execute()
                                    
                                    # Log rejection
                                    admin_user = st.session_state.user
                                    unbillable_days_val = request.get('unbillable_days', 0)
                                    unbillable_log = f" ({unbillable_days_val} unbillable)" if unbillable_days_val > 0 else ""
                                    log_activity(supabase, admin_user['id'], admin_user['username'], "REQUEST_REJECT",
                                               f"Rejected {request['users']['username']}'s request for {request['days_taken']} days ({request['start_date']} to {request['end_date']}{unbillable_log})")
                                    
                                    # Send status update email to employee
                                    employee_email = request['users'].get('email')
                                    if employee_email:
                                        send_status_update_email(
                                            employee_email=employee_email,
                                            employee_name=request['users']['username'],
                                            start_date=request['start_date'],
                                            end_date=request['end_date'],
                                            status="Rejected",
                                            unbillable_days=request.get('unbillable_days', 0)
                                        )
                                    
                                    st.success("Request rejected!")
                                    st.rerun()
                                
                                except Exception as e:
                                    st.error(f"Error rejecting request: {str(e)}")
                        
                        st.divider()
            else:
                st.info("No pending requests at this time.")
        
        except Exception as e:
            st.error(f"Error fetching pending requests: {str(e)}")
    
    # Tab 2: User Management
    with tab2:
        st.subheader("👥 User Management")
        
        # Create tabs for different management functions
        mgmt_tab1, mgmt_tab2 = st.tabs(["📋 All Users", "➕ Create New User"])
        
        # Tab: All Users (View, Edit, Delete)
        with mgmt_tab1:
            try:
                users_response = supabase.table("users").select("*").order("role, username").execute()
                
                if users_response.data:
                    for user in users_response.data:
                        # Different icon based on role
                        icon = "👔" if user['role'] == 'admin' else "👤"
                        
                        with st.expander(f"{icon} {user['username']} ({user['role'].title()})", expanded=False):
                            # Only show vacation metrics for employees
                            if user['role'] == 'employee':
                                col1, col2, col3 = st.columns(3)
                                
                                with col1:
                                    st.metric("Total Allowance", f"{user['total_allowance']} days")
                                with col2:
                                    st.metric("Current Balance", f"{user['balance']} days")
                                with col3:
                                    st.metric("Used", f"{user['total_allowance'] - user['balance']} days")
                                
                                st.markdown("---")
                            
                            # Edit User Form
                            with st.form(f"edit_user_{user['id']}"):
                                st.markdown("### Edit User")
                                
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    new_username = st.text_input(
                                        "Username",
                                        value=user['username'],
                                        key=f"username_{user['id']}"
                                    )
                                    
                                    new_role = st.selectbox(
                                        "Role",
                                        options=["employee", "admin"],
                                        index=0 if user['role'] == 'employee' else 1,
                                        key=f"role_{user['id']}"
                                    )
                                    
                                    new_email = st.text_input(
                                        "Email Address",
                                        value=user.get('email', ''),
                                        key=f"email_{user['id']}"
                                    )
                                
                                with col2:
                                    new_allowance = st.number_input(
                                        "Total Allowance (days)",
                                        min_value=0,
                                        max_value=365,
                                        value=user['total_allowance'],
                                        step=1,
                                        key=f"allowance_{user['id']}"
                                    )
                                
                                # Password change section - separate for visibility
                                st.markdown("#### Change Password (Optional)")
                                change_password = st.checkbox(
                                    "Update password for this user",
                                    key=f"change_pwd_{user['id']}"
                                )
                                
                                new_password = ""
                                confirm_password = ""
                                if change_password:
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        new_password = st.text_input(
                                            "New Password",
                                            type="password",
                                            key=f"new_pwd_{user['id']}",
                                            placeholder="Minimum 6 characters"
                                        )
                                    with col2:
                                        confirm_password = st.text_input(
                                            "Confirm Password",
                                            type="password",
                                            key=f"confirm_pwd_{user['id']}",
                                            placeholder="Re-enter password"
                                        )
                                
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    update_button = st.form_submit_button("💾 Update User", type="primary", use_container_width=True)
                                
                                with col2:
                                    delete_button = st.form_submit_button("🗑️ Delete User", use_container_width=True)
                                
                                if update_button:
                                    try:
                                        # Validate password change
                                        if change_password:
                                            if not new_password:
                                                st.error("Please enter a new password.")
                                            elif new_password != confirm_password:
                                                st.error("Passwords do not match!")
                                            elif len(new_password) < 6:
                                                st.error("Password must be at least 6 characters.")
                                            else:
                                                # Update with password
                                                password_hash = hash_password(new_password)
                                                
                                                # Calculate new balance
                                                used_days = user['total_allowance'] - user['balance']
                                                new_balance = new_allowance - used_days
                                                
                                                if new_balance < 0:
                                                    st.error(f"Cannot set allowance to {new_allowance} days. User has already used {used_days} days.")
                                                else:
                                                    supabase.table("users").update({
                                                        "username": new_username,
                                                        "email": new_email,
                                                        "password_hash": password_hash,
                                                        "role": new_role,
                                                        "total_allowance": new_allowance,
                                                        "balance": new_balance
                                                    }).eq("id", user['id']).execute()
                                                    
                                                    # Log password change
                                                    admin_user = st.session_state.user
                                                    log_activity(supabase, admin_user['id'], admin_user['username'], "USER_UPDATE",
                                                               f"Updated user {new_username} (role: {new_role}, allowance: {new_allowance}, password changed)")
                                                    
                                                    # Recalculate pending requests
                                                    recalculate_pending_requests(supabase, user_id=user['id'], current_balance=new_balance)
                                                    
                                                    st.success(f"✅ User '{new_username}' updated successfully (including password and pending requests)!")
                                                    st.rerun()
                                        else:
                                            # Update without password
                                            used_days = user['total_allowance'] - user['balance']
                                            new_balance = new_allowance - used_days
                                            
                                            if new_balance < 0:
                                                st.error(f"Cannot set allowance to {new_allowance} days. User has already used {used_days} days.")
                                            else:
                                                supabase.table("users").update({
                                                    "username": new_username,
                                                    "email": new_email,
                                                    "role": new_role,
                                                    "total_allowance": new_allowance,
                                                    "balance": new_balance
                                                }).eq("id", user['id']).execute()
                                                
                                                # Log update
                                                admin_user = st.session_state.user
                                                log_activity(supabase, admin_user['id'], admin_user['username'], "USER_UPDATE",
                                                           f"Updated user {new_username} (role: {new_role}, allowance: {new_allowance})")
                                                
                                                # Recalculate pending requests
                                                recalculate_pending_requests(supabase, user_id=user['id'], current_balance=new_balance)
                                                
                                                st.success(f"✅ User '{new_username}' updated successfully (including pending requests)!")
                                                st.rerun()
                                    
                                    except Exception as e:
                                        st.error(f"Error updating user: {str(e)}")
                                
                                if delete_button:
                                    # Prevent deleting yourself
                                    if user['id'] == st.session_state.user['id']:
                                        st.error("❌ You cannot delete your own account!")
                                    else:
                                        try:
                                            supabase.table("users").delete().eq("id", user['id']).execute()
                                            
                                            # Log deletion
                                            admin_user = st.session_state.user
                                            log_activity(supabase, admin_user['id'], admin_user['username'], "USER_DELETE",
                                                       f"Deleted user {user['username']} (role: {user['role']})")
                                            
                                            st.success(f"✅ User '{user['username']}' deleted successfully!")
                                            st.rerun()
                                        except Exception as e:
                                            st.error(f"Error deleting user: {str(e)}")
                else:
                    st.info("No users found in the system.")
            
            except Exception as e:
                st.error(f"Error fetching users: {str(e)}")
        
        # Tab: Create New User
        with mgmt_tab2:
            st.markdown("### Create New User Account")
            
            with st.form("create_user_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    create_username = st.text_input("Username", placeholder="e.g., john.smith")
                    create_role = st.selectbox("Role", options=["employee", "admin"])
                    create_allowance = st.number_input(
                        "Total Allowance (days)",
                        min_value=0,
                        max_value=365,
                        value=21,
                        step=1
                    )
                
                with col2:
                    create_email = st.text_input("Email Address", placeholder="e.g., john.smith@example.com")
                    create_password = st.text_input("Password", type="password", placeholder="Minimum 6 characters")
                    create_confirm_password = st.text_input("Confirm Password", type="password")
                
                create_button = st.form_submit_button("➕ Create User", type="primary", use_container_width=True)
                
                if create_button:
                    # Validation
                    if not create_username:
                        st.error("Please enter a username.")
                    elif not create_password:
                        st.error("Please enter a password.")
                    elif create_password != create_confirm_password:
                        st.error("Passwords do not match!")
                    elif len(create_password) < 6:
                        st.error("Password must be at least 6 characters.")
                    else:
                        try:
                            # Hash password
                            password_hash = hash_password(create_password)
                            
                            # Insert new user
                            insert_response = supabase.table("users").insert({
                                "username": create_username,
                                "email": create_email,
                                "password_hash": password_hash,
                                "role": create_role,
                                "total_allowance": create_allowance,
                                "balance": create_allowance
                            }).execute()
                            
                            # Log user creation
                            admin_user = st.session_state.user
                            log_activity(supabase, admin_user['id'], admin_user['username'], "USER_CREATE",
                                       f"Created new user: {create_username} (role: {create_role}, allowance: {create_allowance} days)")
                            
                            st.success(f"✅ User '{create_username}' created successfully!")
                            st.info(f"**Login Credentials:**\n- Username: `{create_username}`\n- Password: `{create_password}`")
                            st.rerun()
                        
                        except Exception as e:
                            if "duplicate key" in str(e).lower() or "unique" in str(e).lower():
                                st.error(f"❌ Username '{create_username}' already exists!")
                            else:
                                st.error(f"Error creating user: {str(e)}")
    
    # Tab 3: Audit Logs
    with tab3:
        st.subheader("📋 System Audit Logs")
        st.markdown("Track all user activities and administrative operations for security and compliance.")
        
        try:
            # Fetch audit logs
            logs_response = supabase.table("audit_logs").select("*").order("timestamp", desc=True).execute()
            
            if logs_response and logs_response.data:
                # Display statistics
                total_logs = len(logs_response.data)
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Entries", total_logs)
                
                with col2:
                    login_count = len([log for log in logs_response.data if log['action_type'] == 'LOGIN'])
                    st.metric("Logins", login_count)
                
                with col3:
                    request_count = len([log for log in logs_response.data if 'REQUEST' in log['action_type']])
                    st.metric("Request Actions", request_count)
                
                with col4:
                    user_crud_count = len([log for log in logs_response.data if log['action_type'].startswith('USER_')])
                    st.metric("User CRUD", user_crud_count)
                
                st.markdown("---")
                
                # Download section
                st.markdown("### 📥 Download Audit Logs")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # TXT Download
                    if st.button("📄 Download as TXT", use_container_width=True, type="primary"):
                        txt_content = generate_audit_report_txt(supabase)
                        st.download_button(
                            label="💾 Save TXT File",
                            data=txt_content,
                            file_name=f"audit_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                
                with col2:
                    # CSV Download
                    if st.button("📊 Download as CSV", use_container_width=True, type="secondary"):
                        csv_content = generate_audit_report_csv(supabase)
                        st.download_button(
                            label="💾 Save CSV File",
                            data=csv_content,
                            file_name=f"audit_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                
                st.markdown("---")
                
                # Display recent logs
                st.markdown("### 🔍 Recent Activity (Last 20 entries)")
                
                # Create DataFrame for display
                recent_logs = logs_response.data[:20]
                df = pd.DataFrame(recent_logs)
                
                if len(df) > 0:
                    # Format for display
                    df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
                    display_df = df[['timestamp', 'username', 'action_type', 'action_details']]
                    display_df.columns = ['Timestamp', 'User', 'Action', 'Details']
                    
                    st.dataframe(display_df, use_container_width=True, hide_index=True)
                else:
                    st.info("No recent logs to display.")
                
            else:
                st.info("📝 No audit logs yet. Logs will appear here as users perform actions.")
                st.markdown("""
                **Tracked Activities:**
                - User logins
                - Vacation request submissions
                - Request approvals/rejections
                - User creation, updates, and deletion
                """)
        
        except Exception as e:
            st.error(f"Error fetching audit logs: {str(e)}")
            st.info("💡 Make sure the `audit_logs` table is created in your Supabase database. Run `audit_log_schema.sql` in the SQL Editor.")

# ===========================
# Main Application
# ===========================

def main():
    """Main application entry point."""
    
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    # Login page
    if not st.session_state.authenticated:
        st.title("🏖️ Employee Vacation Management System")
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.subheader("🔐 Login")
            
            with st.form("login_form"):
                username = st.text_input("Username", placeholder="Enter your username")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                login_button = st.form_submit_button("Login", use_container_width=True, type="primary")
                
                if login_button:
                    if not username or not password:
                        st.error("Please enter both username and password.")
                    else:
                        user = login_user(username, password)
                        
                        if user:
                            st.session_state.authenticated = True
                            st.session_state.user = user
                            st.success(f"Welcome, {user['username']}!")
                            st.rerun()
                        else:
                            st.error("Invalid username or password.")
            
            # st.markdown("---")
            # Removed demo credentials section
    
    # Authenticated user interface
    else:
        user = st.session_state.user
        
        # Sidebar
        with st.sidebar:
            st.title("🏖️ Vacation System")
            st.markdown(f"**Logged in as:** {user['username']}")
            st.markdown(f"**Role:** {user['role'].title()}")
            st.markdown("---")
            
            if st.button("🚪 Logout", use_container_width=True):
                logout_user()
                st.rerun()
        
        # Route to appropriate dashboard
        if user['role'] == 'admin':
            admin_dashboard()
        else:
            employee_dashboard()

if __name__ == "__main__":
    main()
