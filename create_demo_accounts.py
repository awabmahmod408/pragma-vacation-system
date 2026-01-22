"""
Create fresh demo accounts with correct password hashes
"""

from supabase_simple import create_client
import bcrypt

# Supabase credentials
SUPABASE_URL = "https://qnetdfiqsqznomdnnjgv.supabase.co"
SUPABASE_KEY = "sb_publishable_Iuw4Rf4vg-XYO0-kI8Ickg_x8gqy947"

print("=" * 70)
print("CREATING FRESH DEMO ACCOUNTS")
print("=" * 70)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

print("\n1. Deleting old demo accounts...")
try:
    # Delete existing demo users
    for username in ["admin", "john.doe", "jane.smith", "bob.johnson"]:
        supabase.table("users").delete().eq("username", username).execute()
    print("   ✅ Old accounts deleted")
except Exception as e:
    print(f"   ⚠️ Error deleting (might not exist): {e}")

print("\n2. Creating fresh password hashes...")
admin_password = "admin123"
employee_password = "password123"

admin_hash = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
employee_hash = bcrypt.hashpw(employee_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

print(f"   Admin hash: {admin_hash[:50]}...")
print(f"   Employee hash: {employee_hash[:50]}...")

# Verify hashes work
admin_verify = bcrypt.checkpw(admin_password.encode('utf-8'), admin_hash.encode('utf-8'))
employee_verify = bcrypt.checkpw(employee_password.encode('utf-8'), employee_hash.encode('utf-8'))

print(f"\n3. Testing hashes before inserting...")
print(f"   Admin hash verifies: {admin_verify}")
print(f"   Employee hash verifies: {employee_verify}")

if not (admin_verify and employee_verify):
    print("\n❌ HASH VERIFICATION FAILED! Stopping.")
    exit(1)

print("\n4. Inserting new demo accounts...")

# Insert admin
try:
    supabase.table("users").insert({
        "username": "admin",
        "password_hash": admin_hash,
        "role": "admin",
        "total_allowance": 0,
        "balance": 0
    }).execute()
    print("   ✅ Admin account created")
except Exception as e:
    print(f"   ❌ Error creating admin: {e}")

# Insert employees
for username in ["john.doe", "jane.smith", "bob.johnson"]:
    try:
        supabase.table("users").insert({
            "username": username,
            "password_hash": employee_hash,
            "role": "employee",
            "total_allowance": 21,
            "balance": 21
        }).execute()
        print(f"   ✅ {username} created")
    except Exception as e:
        print(f"   ❌ Error creating {username}: {e}")

print("\n" + "=" * 70)
print("✅ DEMO ACCOUNTS READY!")
print("=" * 70)
print("\n🔑 Login Credentials:")
print("   Admin:    admin / admin123")
print("   Employee: john.doe / password123")
print("\n🌐 Try logging in at: http://localhost:8502")
print("=" * 70)
