import cv2
import numpy as np
import face_recognition
from collections import defaultdict

class FaceRecognizer:
    """
    Optimized frame processing, match confidence metrics, and dynamic HUD overlays.
    """
    def __init__(self, tolerance=0.55, resize_factor=0.25, min_consecutive_frames=2):
        self.tolerance = tolerance
        self.resize_factor = resize_factor
        self.min_consecutive_frames = min_consecutive_frames
        self.detection_history = defaultdict(int)

    def process_frame(self, frame, known_encodings, known_names):
        if not known_encodings:
            return [], [], [], []

        small_frame = cv2.resize(frame, (0, 0), fx=self.resize_factor, fy=self.resize_factor)
        rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small)
        face_encodings = face_recognition.face_encodings(rgb_small, face_locations)

        face_names = []
        confidences = []
        logging_names = []
        current_detected = set()

        for encoding in face_encodings:
            matches = face_recognition.compare_faces(known_encodings, encoding, tolerance=self.tolerance)
            name = "Unknown"
            confidence = 0

            distances = face_recognition.face_distance(known_encodings, encoding)
            if len(distances) > 0:
                best_idx = np.argmin(distances)
                best_dist = distances[best_idx]
                confidence = max(0, min(100, int((1.0 - (best_dist / 1.1)) * 100)))

                if matches[best_idx]:
                    name = known_names[best_idx]
                    current_detected.add(name)
                    self.detection_history[name] += 1
                    if self.detection_history[name] >= self.min_consecutive_frames:
                        logging_names.append(name)

            face_names.append(name)
            confidences.append(confidence)

        for k in list(self.detection_history.keys()):
            if k not in current_detected:
                self.detection_history[k] = max(0, self.detection_history[k] - 1)

        scale = int(1 / self.resize_factor)
        full_locations = [
            (top * scale, right * scale, bottom * scale, left * scale)
            for (top, right, bottom, left) in face_locations
        ]

        return full_locations, face_names, confidences, logging_names

    def draw_overlays(self, frame, face_locations, face_names, confidences, summary_stats):
        for (top, right, bottom, left), name, conf in zip(face_locations, face_names, confidences):
            is_known = (name != "Unknown")
            color = (46, 204, 113) if is_known else (52, 73, 94)

            line_len = int(min(right - left, bottom - top) * 0.2)
            thick = 3
            cv2.rectangle(frame, (left, top), (right, bottom), color, 1)
            cv2.line(frame, (left, top), (left + line_len, top), color, thick)
            cv2.line(frame, (left, top), (left, top + line_len), color, thick)
            cv2.line(frame, (right, top), (right - line_len, top), color, thick)
            cv2.line(frame, (right, top), (right, top + line_len), color, thick)
            cv2.line(frame, (left, bottom), (left + line_len, bottom), color, thick)
            cv2.line(frame, (left, bottom), (left, bottom - line_len), color, thick)
            cv2.line(frame, (right, bottom), (right - line_len, bottom), color, thick)
            cv2.line(frame, (right, bottom), (right, bottom - line_len), color, thick)

            label = f"{name} ({conf}%)" if is_known else "Unknown"
            font = cv2.FONT_HERSHEY_SIMPLEX
            (tw, th), _ = cv2.getTextSize(label, font, 0.55, 1)
            cv2.rectangle(frame, (left, bottom - th - 12), (left + tw + 12, bottom), color, cv2.FILLED)
            cv2.putText(frame, label, (left + 6, bottom - 6), font, 0.55, (255, 255, 255), 1, cv2.LINE_AA)

        h, w, _ = frame.shape
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (w, 45), (20, 24, 33), cv2.FILLED)
        cv2.addWeighted(overlay, 0.85, frame, 0.15, 0, frame)

        reg = summary_stats.get("total_registered", 0)
        pres = summary_stats.get("present_count", 0)
        late = summary_stats.get("late_count", 0)

        status_text = f"Live Feed  |  Enrolled: {reg}  |  Present: {pres}  |  Late: {late}"
        cv2.putText(frame, status_text, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (236, 240, 241), 2, cv2.LINE_AA)
        return frame
