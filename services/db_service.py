from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

# Initialize Supabase client (single instance, reused everywhere)
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

TABLE = "student"


def get_all_students():
    """Fetch all student records."""
    result = supabase.table(TABLE).select("*").execute()
    return result.data


def get_student_by_id(student_id):
    """Fetch a single student by ID."""
    result = supabase.table(TABLE).select("*").eq("student_id", student_id).execute()
    if result.data:
        return result.data[0]
    return None


def get_student_by_pk(pk_id):
    """Fetch a single student by primary key id (used for OpenCV)."""
    result = supabase.table(TABLE).select("*").eq("id", pk_id).execute()
    if result.data:
        return result.data[0]
    return None


def add_student(data):
    """Insert a new student record."""
    row = {
        "department": data.get("department", ""),
        "course": data.get("course", ""),
        "year": data.get("year", ""),
        "semester": data.get("semester", ""),
        "student_id": data["student_id"],
        "name": data["name"],
        "division": data.get("division", ""),
        "roll": data.get("roll", ""),
        "gender": data.get("gender", ""),
        "dob": data.get("dob", ""),
        "email": data.get("email", ""),
        "phone": data.get("phone", ""),
        "address": data.get("address", ""),
        "teacher": data.get("teacher", ""),
        "photo_sample": data.get("photo_sample", "No"),
    }
    result = supabase.table(TABLE).insert(row).execute()
    return result.data


def update_student(student_id, data):
    """Update an existing student record."""
    row = {
        "department": data.get("department", ""),
        "course": data.get("course", ""),
        "year": data.get("year", ""),
        "semester": data.get("semester", ""),
        "name": data.get("name", ""),
        "division": data.get("division", ""),
        "roll": data.get("roll", ""),
        "gender": data.get("gender", ""),
        "dob": data.get("dob", ""),
        "email": data.get("email", ""),
        "phone": data.get("phone", ""),
        "address": data.get("address", ""),
        "teacher": data.get("teacher", ""),
        "photo_sample": data.get("photo_sample", "No"),
    }
    result = supabase.table(TABLE).update(row).eq("student_id", student_id).execute()
    return result.data


def delete_student(student_id):
    """Delete a student record by ID."""
    result = supabase.table(TABLE).delete().eq("student_id", student_id).execute()
    return result.data


def get_student_info(pk_id):
    """Get student name, roll, and ID for face recognition overlay."""
    student = get_student_by_pk(pk_id)
    if student:
        return {
            "id": str(student.get("student_id", "Unknown")),
            "name": str(student.get("name", "Unknown")),
            "roll": str(student.get("roll", "Unknown")),
        }
    return {"id": "Unknown", "name": "Unknown", "roll": "Unknown"}
