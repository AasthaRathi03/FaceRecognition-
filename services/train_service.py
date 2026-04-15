import cv2
import os
import numpy as np
from PIL import Image
from config import DATA_DIR, CLASSIFIER_PATH


def train_model():
    """Train the LBPH face recognizer on all images in the data directory.
    
    Returns:
        dict with training status, face count, and unique IDs
    """
    if not os.path.exists(DATA_DIR) or len(os.listdir(DATA_DIR)) == 0:
        return {"success": False, "error": "No training images found in data folder"}

    faces = []
    ids = []
    image_paths = [
        os.path.join(DATA_DIR, f)
        for f in os.listdir(DATA_DIR)
        if f.endswith('.jpg')
    ]

    if not image_paths:
        return {"success": False, "error": "No .jpg images found in data folder"}

    for image_path in image_paths:
        try:
            img = Image.open(image_path).convert('L')
            img_np = np.array(img, 'uint8')
            
            # Enforce histogram equalization for old datasets that weren't captured with normalization
            img_np = cv2.equalizeHist(img_np)
            
            # Extract student ID from filename: user.<id>.<count>.jpg
            student_id = int(os.path.split(image_path)[1].split('.')[1])
            faces.append(img_np)
            ids.append(student_id)
        except Exception as e:
            print(f"Skipping {image_path}: {e}")
            continue

    if len(faces) == 0:
        return {"success": False, "error": "Could not process any training images"}

    ids_np = np.array(ids)

    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.train(faces, ids_np)
    clf.write(CLASSIFIER_PATH)

    unique_ids = len(set(ids))
    return {
        "success": True,
        "total_images": len(faces),
        "unique_students": unique_ids,
        "message": f"Training complete! Processed {len(faces)} images for {unique_ids} students."
    }
