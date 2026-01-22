"""
Audit logging utility for the Vacation Management System
Tracks all important system activities for admin review
"""

from datetime import datetime
from typing import Optional
import json
import csv
from io import StringIO

def log_activity(supabase, user_id: str, username: str, action_type: str, action_details: str = "", ip_address: str = ""):
    """
    Log an activity to the audit log
    
    Args:
        supabase: Supabase client instance
        user_id: UUID of the user performing the action
        username: Username of the user
        action_type: Type of action (LOGIN, LOGOUT, REQUEST_CREATE, etc.)
        action_details: Additional details about the action
        ip_address: Optional IP address of the user
    """
    try:
        supabase.table("audit_logs").insert({
            "user_id": user_id,
            "username": username,
            "action_type": action_type,
            "action_details": action_details,
            "ip_address": ip_address or "N/A"
        }).execute()
    except Exception as e:
        # Log errors silently - we don't want audit logging to break the app
        print(f"Audit log error: {e}")

def format_log_entry(log: dict) -> str:
    """Format a single log entry for display"""
    timestamp = log.get('timestamp', log.get('created_at', ''))
    username = log.get('username', 'Unknown')
    action = log.get('action_type', 'UNKNOWN')
    details = log.get('action_details', '')
    
    return f"{timestamp} | {username:20s} | {action:20s} | {details}"

def generate_audit_report_txt(supabase, limit: int = 10000) -> str:
    """
    Generate a formatted audit report in TXT format
    
    Args:
        supabase: Supabase client instance
        limit: Maximum number of log entries to include
        
    Returns:
        Formatted audit report as string
    """
    try:
        # Fetch audit logs
        response = supabase.table("audit_logs").select("*").order("timestamp", desc=True).execute()
        
        if not response or not response.data:
            return "No audit logs found."
        
        # Generate report header
        report_lines = [
            "=" * 120,
            "EMPLOYEE VACATION MANAGEMENT SYSTEM - AUDIT LOG",
            "=" * 120,
            f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Total Entries: {len(response.data)}",
            "=" * 120,
            "",
            f"{'TIMESTAMP':<25} | {'USERNAME':<20} | {'ACTION':<20} | {'DETAILS'}",
            "-" * 120,
        ]
        
        # Add log entries
        for log in response.data[:limit]:
            report_lines.append(format_log_entry(log))
        
        report_lines.append("")
        report_lines.append("=" * 120)
        report_lines.append("END OF AUDIT LOG")
        report_lines.append("=" * 120)
        
        return "\n".join(report_lines)
        
    except Exception as e:
        return f"Error generating audit report: {str(e)}"

def generate_audit_report_csv(supabase, limit: int = 10000) -> str:
    """
    Generate audit report in CSV format
    
    Args:
        supabase: Supabase client instance
        limit: Maximum number of log entries to include
        
    Returns:
        CSV formatted audit report as string
    """
    try:
        # Fetch audit logs
        response = supabase.table("audit_logs").select("*").order("timestamp", desc=True).execute()
        
        if not response or not response.data:
            return "Timestamp,Username,Action Type,Action Details,IP Address\n"
        
        # Create CSV in memory
        output = StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['Timestamp', 'Username', 'Action Type', 'Action Details', 'IP Address'])
        
        # Write data rows
        for log in response.data[:limit]:
            timestamp = log.get('timestamp', log.get('created_at', ''))
            username = log.get('username', 'Unknown')
            action_type = log.get('action_type', 'UNKNOWN')
            action_details = log.get('action_details', '')
            ip_address = log.get('ip_address', 'N/A')
            
            writer.writerow([timestamp, username, action_type, action_details, ip_address])
        
        return output.getvalue()
        
    except Exception as e:
        return f"Error generating CSV report: {str(e)}"
