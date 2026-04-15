"""
Run this script ONCE to create the 'student' table in Supabase.

Usage:  python setup_supabase.py
"""
import requests
from config import SUPABASE_URL, SUPABASE_KEY

# Supabase REST API to run SQL via the SQL editor isn't available via anon key,
# so we create the table using the PostgREST RPC or we guide the user.

SQL = """
CREATE TABLE IF NOT EXISTS student (
    id BIGSERIAL PRIMARY KEY,
    department TEXT DEFAULT '',
    course TEXT DEFAULT '',
    year TEXT DEFAULT '',
    semester TEXT DEFAULT '',
    student_id TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    division TEXT DEFAULT '',
    roll TEXT DEFAULT '',
    gender TEXT DEFAULT '',
    dob TEXT DEFAULT '',
    email TEXT DEFAULT '',
    phone TEXT DEFAULT '',
    address TEXT DEFAULT '',
    teacher TEXT DEFAULT '',
    photo_sample TEXT DEFAULT 'No',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Disable RLS so the anon key can access the table
ALTER TABLE student ENABLE ROW LEVEL SECURITY;

-- Create a policy that allows all operations via anon key
CREATE POLICY "Allow all access" ON student
    FOR ALL
    USING (true)
    WITH CHECK (true);
"""

print("=" * 60)
print("  SUPABASE TABLE SETUP")
print("=" * 60)
print()
print("Please create the 'student' table in Supabase:")
print()
print("1. Go to your Supabase Dashboard")
print("2. Click 'SQL Editor' in the left sidebar")
print("3. Click 'New Query'")
print("4. Paste the following SQL and click 'Run':")
print()
print("-" * 60)
print(SQL)
print("-" * 60)
print()
print("After running the SQL, your app will be ready to use!")
print()

# Also copy to clipboard-friendly file
with open("setup_table.sql", "w") as f:
    f.write(SQL)
print("SQL also saved to: setup_table.sql")
print("=" * 60)
