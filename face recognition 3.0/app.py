import os
import cv2
import time
from flask import Flask, render_template, Response, jsonify
from core.student_manager import StudentManager
from core.attendance_logger import AttendanceLogger
from core.face_recognizer import FaceRecognizer

app = Flask(__name__)

# Initialize Core Managers
student_mgr = StudentManager(folder_path="students")
student_mgr.load_students()

logger = AttendanceLogger(logs_dir=".", cutoff_time="09:00:00")
recognizer = FaceRecognizer(tolerance=0.55, resize_factor=0.25, min_consecutive_frames=2)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/summary")
def get_summary():
    known_names = student_mgr.get_student_names()
    summary = logger.get_today_summary(known_names)
    return jsonify(summary)

@app.route("/api/records")
def get_records():
    records = logger.get_today_records()
    return jsonify(records)

@app.route("/api/students")
def get_students():
    names = student_mgr.get_student_names()
    return jsonify(names)

def generate_frames():
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not camera.isOpened():
        camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("[WARNING] Webcam unavailable.")
        return

    process_this_frame = True
    locations, names, confidences = [], [], []

    try:
        while True:
            success, frame = camera.read()
            if not success or frame is None:
                continue

            known_encodings, known_names = student_mgr.get_known_data()

            if process_this_frame:
                locations, names, confidences, logging_names = recognizer.process_frame(frame, known_encodings, known_names)
                for name in logging_names:
                    logger.mark_attendance(name)

            process_this_frame = not process_this_frame

            summary_stats = logger.get_today_summary(known_names)
            frame = recognizer.draw_overlays(frame, locations, names, confidences, summary_stats)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            
            time.sleep(0.03)
    finally:
        camera.release()

@app.route("/video_feed")
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    print("[INFO] Launching Professional Attendance Web Server on http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
