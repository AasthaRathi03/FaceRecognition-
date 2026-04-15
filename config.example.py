import os

# Supabase Configuration
SUPABASE_URL = os.environ.get("SUPABASE_URL", "YOUR_SUPABASE_URL_HERE")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "YOUR_SUPABASE_KEY_HERE")

# Application paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
CLASSIFIER_PATH = os.path.join(BASE_DIR, "classifier.xml")
STATIC_DIR = os.path.join(BASE_DIR, "static")
IMAGES_DIR = os.path.join(STATIC_DIR, "images")

# Face capture settings
FACE_SAMPLE_COUNT = 100
FACE_RESIZE = (450, 450)

# Flask settings
SECRET_KEY = os.environ.get("SECRET_KEY", "replace-with-a-secure-secret-key")
DEBUG = os.environ.get("FLASK_DEBUG", "True").lower() == "true"
PORT = int(os.environ.get("PORT", 5000))
