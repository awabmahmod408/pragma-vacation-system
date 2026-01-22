"""
Simple Database Setup Script - Opens Supabase SQL Editor with your schema ready to execute
This script automates the database setup by opening your browser and preparing the SQL.
"""

import webbrowser
import pyperclip
import time

# Read the SQL schema
print("📖 Reading database schema...")
with open('database_schema.sql', 'r', encoding='utf-8') as f:
    sql_content = f.read()

print("✅ SQL schema loaded!")
print(f"   - Total SQL length: {len(sql_content)} characters")
print(f"   - Contains {sql_content.count('CREATE TABLE')} tables")
print(f"   - Contains {sql_content.count('INSERT INTO')} data inserts")

# Copy SQL to clipboard
print("\n📋 Copying SQL to clipboard...")
try:
    pyperclip.copy(sql_content)
    print("✅ SQL copied to clipboard successfully!")
    clipboard_success = True
except:
    print("⚠️ Could not copy to clipboard (pyperclip not installed)")
    clipboard_success = False

# Open Supabase dashboard
SUPABASE_PROJECT_REF = "qnetdfiqsqznomdnnjgv"
SQL_EDITOR_URL = f"https://supabase.com/dashboard/project/{SUPABASE_PROJECT_REF}/sql/new"

print(f"\n🌐 Opening Supabase SQL Editor...")
print(f"   URL: {SQL_EDITOR_URL}")

time.sleep(1)
webbrowser.open(SQL_EDITOR_URL)

print("\n" + "="*70)
print("📝 NEXT STEPS:")
print("="*70)

if clipboard_success:
    print("\n✅ The SQL schema is already copied to your clipboard!")
    print("\n1. Your browser should open to the Supabase SQL Editor")
    print("2. Press Ctrl+V to paste the SQL schema")
    print("3. Click the green 'RUN' button (or press Ctrl+Enter)")
    print("4. Wait for 'Success' message (should take ~2-3 seconds)")
else:
    print("\n1. Your browser should open to the Supabase SQL Editor")
    print("2. Open 'database_schema.sql' in a text editor")
    print("3. Copy all the SQL content (Ctrl+A, Ctrl+C)")
    print("4. Paste it in the SQL Editor (Ctrl+V)")
    print("5. Click the green 'RUN' button (or press Ctrl+Enter)")
    print("6. Wait for 'Success' message (~2-3 seconds)")

print("\n" + "="*70)
print("\n✨ What this will create:")
print("   - ✅ 'users' table (employees and admins)")
print("   - ✅ 'requests' table (vacation requests)")
print("   - ✅ Indexes for fast queries")
print("   - ✅ Auto-update triggers")
print("   - ✅ Row Level Security policies")
print("   - ✅ Demo accounts:")
print("       • Admin: admin / admin123")
print("       • Employee: john.doe / password123")

print("\n📋 After execution succeeds, run:")
print("   » streamlit run app.py")

print("\n" + "="*70)
