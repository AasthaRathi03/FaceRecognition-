import os
import sys
from flask import (
    Flask, render_template, request, jsonify, Response, redirect, url_for
)

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import SECRET_KEY, DEBUG, PORT, CLASSIFIER_PATH, DATA_DIR
from services.db_service import (
    get_all_students, get_student_by_id, add_student,
    update_student, delete_student
)
from services.train_service import train_model
from services.face_service import generate_video_feed, generate_capture_feed

app = Flask(__name__)
app.secret_key = SECRET_KEY


# ==================== PAGE ROUTES ====================

@app.route("/")
def index():
    """Dashboard page."""
    student_count = len(get_all_students()) if _db_available() else 0
    image_count = len(os.listdir(DATA_DIR)) if os.path.exists(DATA_DIR) else 0
    model_exists = os.path.exists(CLASSIFIER_PATH)
    return render_template(
        "index.html",
        student_count=student_count,
        image_count=image_count,
        model_trained=model_exists
    )


@app.route("/students")
def students_page():
    """Student management page."""
    return render_template("students.html")


@app.route("/train")
def train_page():
    """Model training page."""
    image_count = len(os.listdir(DATA_DIR)) if os.path.exists(DATA_DIR) else 0
    model_exists = os.path.exists(CLASSIFIER_PATH)
    return render_template(
        "train.html",
        image_count=image_count,
        model_trained=model_exists
    )


@app.route("/recognize")
def recognize_page():
    """Face recognition page."""
    model_exists = os.path.exists(CLASSIFIER_PATH)
    return render_template("recognize.html", model_trained=model_exists)


# ==================== API ROUTES ====================

@app.route("/api/students", methods=["GET"])
def api_get_students():
    """Get all students as JSON."""
    try:
        students = get_all_students()
        return jsonify({"success": True, "students": students})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/students", methods=["POST"])
def api_add_student():
    """Add a new student."""
    try:
        data = request.json
        required = ["student_id", "name", "department"]
        for field in required:
            if not data.get(field):
                return jsonify({"success": False, "error": f"{field} is required"}), 400

        add_student(data)
        return jsonify({"success": True, "message": "Student added successfully"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/students/<student_id>", methods=["PUT"])
def api_update_student(student_id):
    """Update a student."""
    try:
        data = request.json
        update_student(student_id, data)
        return jsonify({"success": True, "message": "Student updated successfully"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/students/<student_id>", methods=["DELETE"])
def api_delete_student(student_id):
    """Delete a student."""
    try:
        delete_student(student_id)
        return jsonify({"success": True, "message": "Student deleted successfully"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/train", methods=["POST"])
def api_train():
    """Train the face recognition model."""
    try:
        result = train_model()
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/capture_feed/<int:pk_id>")
def capture_feed(pk_id):
    """Stream live video feed for capturing face dataset."""
    return Response(
        generate_capture_feed(pk_id),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/video_feed")
def video_feed():
    """Stream live video feed with face recognition overlays."""
    return Response(
        generate_video_feed(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


# ==================== HELPERS ====================

def _db_available():
    """Check if DB connection is available."""
    try:
        get_all_students()
        return True
    except Exception:
        return False


# ==================== MAIN ====================

if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)
    print(f"\n  [STAR] Face Recognition System running at http://localhost:{PORT}\n")
    app.run(debug=DEBUG, port=PORT, threaded=True)
