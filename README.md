🎯 Face Detection Attendance System
An AI-powered attendance system that marks user presence through real-time facial recognition. Built with Python, OpenCV, and Flask, it supports deployment on Jetson Nano and standard webcams like Logitech C270.

📌 Project Overview
This system captures and identifies faces to securely and efficiently record attendance. It offers a user-friendly web interface and is ideal for use in classrooms, offices, or labs.

🚀 Features
🧠 Real-Time Face Detection: Utilizes Haarcascade classifiers to detect faces live via webcam.

🪞 Face Recognition: Implements the LBPH (Local Binary Pattern Histogram) algorithm for accurate recognition.

🕒 Auto Attendance Logging: Logs user presence along with date and time in a local CSV or database.

🌐 Web Interface: Clean Flask-based frontend built with HTML/CSS.

🎥 Camera Support: Compatible with webcams like Logitech C270.

🖥️ Edge Deployment: Can be deployed on low-cost hardware like NVIDIA Jetson Nano.

🧰 Technology Stack
Languages: Python, HTML, CSS

Libraries: OpenCV, NumPy, Flask

Machine Learning Model: LBPH (Local Binary Pattern Histogram)

Hardware: Logitech webcam / Jetson Nano

⚙️ Getting Started
✅ Prerequisites
Python 3.x

pip (Python package installer)

A compatible webcam (e.g., Logitech C270)

Haarcascade file (haarcascade_frontalface_default.xml)

🔧 Installation
bash
Copy
Edit
git clone https://github.com/khem75/face-attendance-system.git
cd face-attendance-system
pip install -r requirements.txt
python app.py
🧠 How It Works
The camera captures the user’s face.

Haarcascade detects the face in the frame.

LBPH compares the detected face with trained data.

If matched, attendance is logged with name, date, and time.

The Flask web app displays status and history.

📂 Project Structure
graphql
Copy
Edit
face-attendance-system/
│
├── app.py                 # Flask app entry point
├── dataset/               # Collected training images
├── trainer/               # Trained model (.yml file)
├── static/                # CSS & frontend assets
├── templates/             # HTML templates for Flask
├── haarcascade/           # Haarcascade XML files
├── attendance.csv         # Auto-generated attendance log
├── requirements.txt       # Python dependencies
💡 Deployment on Jetson Nano
Ensure OpenCV and Flask are installed (pip3 install opencv-python flask)

Use lightweight image resizing for better performance

Optimize face detection 

👤 Developer
Developed by Khem Raj Joshi
Connect on: Facebook | LinkedIn
