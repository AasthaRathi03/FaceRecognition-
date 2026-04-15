import cv2
import os
import numpy as np
from config import DATA_DIR, CLASSIFIER_PATH, FACE_SAMPLE_COUNT, FACE_RESIZE
from services.db_service import get_student_info


# Load Haar cascade once
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# Global cache for classifier to reduce startup delay
_classifier_cache = None
_classifier_mtime = 0

def get_cached_classifier():
    global _classifier_cache, _classifier_mtime
    if os.path.exists(CLASSIFIER_PATH):
        try:
            mtime = os.path.getmtime(CLASSIFIER_PATH)
            if _classifier_cache is None or mtime > _classifier_mtime:
                clf = cv2.face.LBPHFaceRecognizer_create()
                clf.read(CLASSIFIER_PATH)
                _classifier_cache = clf
                _classifier_mtime = mtime
                print("[INFO] Classifier loaded from disk successfully")
        except Exception as e:
            print(f"[WARNING] Classifier failed to load: {e}")
            _classifier_cache = None
    else:
        _classifier_cache = None
    return _classifier_cache


def crop_face(img):
    """Detect and crop the first face from an image frame."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        return img[y:y+h, x:x+w]
    return None


def generate_capture_feed(student_id):
    """Generator that yields MJPEG frames for capturing face samples from webcam.
    Yields images over HTTP and saves them to the dataset directory.
    Updates the Supabase database automatically when complete.
    """
    os.makedirs(DATA_DIR, exist_ok=True)

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not cap.isOpened():
        err = _make_error_frame("Cannot access webcam")
        if err: yield err
        return

    img_count = 0
    fail_count = 0

    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            fail_count += 1
            if fail_count > 20: break
            continue
            
        fail_count = 0

        face = crop_face(frame)

        if face is not None:
            img_count += 1
            face_resized = cv2.resize(face, FACE_RESIZE)
            face_gray = cv2.cvtColor(face_resized, cv2.COLOR_BGR2GRAY)
            # Equalize lighting histogram for more robust AI training
            face_gray = cv2.equalizeHist(face_gray)

            file_path = os.path.join(DATA_DIR, f"user.{student_id}.{img_count}.jpg")
            cv2.imwrite(file_path, face_gray)

            cv2.putText(
                frame, f"Capturing: {img_count}/{FACE_SAMPLE_COUNT}",
                (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3
            )
            # Draw green box indicating successful capture frame
            cv2.rectangle(frame, (50, 60), (590, 420), (0, 255, 0), 2)
        else:
            cv2.putText(
                frame, "No face detected. Please look at camera.",
                (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2
            )

        ret, buffer = cv2.imencode('.jpg', frame)
        if ret:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

        if img_count >= FACE_SAMPLE_COUNT:
            # End of capture, update DB
            from services.db_service import get_student_by_pk, update_student
            student = get_student_by_pk(student_id)
            if student:
                student["photo_sample"] = "Yes"
                update_student(student.get("student_id"), student)
            
            # Show final completion frame
            success_frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(success_frame, "Capture Complete!", (150, 240), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
            ret, buffer = cv2.imencode('.jpg', success_frame)
            if ret:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
            break

    cap.release()


def _make_error_frame(message):
    """Create a black frame with an error message for the browser."""
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    # Draw error text
    lines = message.split('\n')
    for i, line in enumerate(lines):
        cv2.putText(frame, line, (30, 200 + i * 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    ret, buffer = cv2.imencode('.jpg', frame)
    if ret:
        return (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    return None


def generate_video_feed():
    """Generator that yields MJPEG frames with face recognition overlays.
    
    Used for streaming live video to the browser via /video_feed endpoint.
    """
    # Load classifier
    # Load classifier using cache
    clf = get_cached_classifier()

    if clf is None:
        # Show error frame then stream camera-only (face detection without recognition)
        err = _make_error_frame("Model not loaded.\nShowing detection only.")
        if err:
            yield err

    # Open camera (DirectShow is much faster, retry loop handles empty frames)
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    if not cap.isOpened():
        print("[ERROR] Cannot access webcam")
        import time
        while True:
            err = _make_error_frame("ERROR: Cannot access webcam.\nMake sure camera is connected.")
            if err:
                yield err
            time.sleep(1)

    print("[INFO] Camera opened successfully")

    # Cache student info to avoid DB queries every frame
    student_cache = {}
    fail_count = 0

    while True:
        ret, frame = cap.read()
        
        if not ret or frame is None:
            fail_count += 1
            if fail_count > 20:  # Only break if it fails 20 times in a row
                print("[ERROR] Camera feed lost")
                break
            continue
            
        fail_count = 0  # Reset on success

        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Use 1.3 and 5 for much faster and smoother detection compared to 1.1 and 10
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                if clf is not None:
                    # Extract the face ROI
                    face_roi = gray[y:y+h, x:x+w]
                    
                    # Normalize lighting and resize perfectly to match the trained dataset dimensions
                    face_roi = cv2.equalizeHist(face_roi)
                    face_roi = cv2.resize(face_roi, FACE_RESIZE)

                    face_id, confidence_raw = clf.predict(face_roi)
                    confidence = int(100 * (1 - confidence_raw / 300))

                    if confidence > 75:
                        if face_id not in student_cache:
                            try:
                                student_cache[face_id] = get_student_info(face_id)
                            except Exception:
                                student_cache[face_id] = {"id": str(face_id), "name": "Unknown", "roll": "Unknown"}
                        info = student_cache[face_id]

                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
                        cv2.putText(frame, f"ID: {info['id']}", (x, y-60),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                        cv2.putText(frame, f"Name: {info['name']}", (x, y-35),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                        cv2.putText(frame, f"Roll: {info['roll']}", (x, y-10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                    else:
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 3)
                        cv2.putText(frame, "Unknown", (x, y-10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                else:
                    # No classifier — just show face detection boxes
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 2)
                    cv2.putText(frame, "Face Detected", (x, y-10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        except Exception as e:
            print(f"[WARNING] Frame processing error: {e}")

        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    cap.release()
