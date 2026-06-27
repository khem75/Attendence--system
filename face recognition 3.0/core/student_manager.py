import os
import cv2
import pickle
import face_recognition

class StudentManager:
    """
    Manages loading student images dynamically with smart disk caching acceleration.
    """
    def __init__(self, folder_path="students", cache_file="encodings_cache.pkl"):
        self.folder_path = folder_path
        self.cache_file = os.path.join(self.folder_path, cache_file)
        self.known_face_encodings = []
        self.known_face_names = []

    def load_students(self):
        """Scans folder_path and encodes student images with cache acceleration."""
        self.known_face_encodings.clear()
        self.known_face_names.clear()

        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)
            return

        supported_exts = ('.jpg', '.jpeg', '.png', '.bmp')
        files = sorted([f for f in os.listdir(self.folder_path) if f.lower().endswith(supported_exts)])

        current_meta = {}
        for f in files:
            full_path = os.path.join(self.folder_path, f)
            current_meta[f] = os.path.getmtime(full_path)

        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "rb") as cf:
                    cache_data = pickle.load(cf)
                if cache_data.get("files_meta") == current_meta:
                    self.known_face_encodings = cache_data.get("encodings", [])
                    self.known_face_names = cache_data.get("names", [])
                    print(f"[INFO] Loaded {len(self.known_face_names)} student encodings instantly from cache.")
                    return
            except Exception as e:
                pass

        print(f"[INFO] Encoding {len(files)} student faces...")
        for filename in files:
            name = os.path.splitext(filename)[0].capitalize()
            image_path = os.path.join(self.folder_path, filename)
            try:
                image = face_recognition.load_image_file(image_path)
                encodings = face_recognition.face_encodings(image)
                if encodings:
                    self.known_face_encodings.append(encodings[0])
                    self.known_face_names.append(name)
            except Exception as e:
                pass

        try:
            cache_data = {
                "files_meta": current_meta,
                "encodings": self.known_face_encodings,
                "names": self.known_face_names
            }
            with open(self.cache_file, "wb") as cf:
                pickle.dump(cache_data, cf)
        except Exception as e:
            pass

    def get_known_data(self):
        return self.known_face_encodings, self.known_face_names

    def get_student_names(self):
        return list(self.known_face_names)
