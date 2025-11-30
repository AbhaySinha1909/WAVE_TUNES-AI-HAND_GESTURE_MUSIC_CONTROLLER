🎵 Wave Tunes

    A real-time ML-powered, webcam-based gesture control system for music playback.

    Wave Tunes lets users control music using hand gestures, powered by MediaPipe, TensorFlow, and Django.

    ✨ No buttons. No clicks. Just gestures.
    Perfect for accessibility, contactless control, smart systems, and futuristic UI designs.

🚀 Features
🎯 Hand Gesture Recognition

    Control your music with 11 gestures:

    Gesture	Action
    ✋ Palm	Play / Pause
    ✊ Fist	Pause
    ☝️ Index Finger	Next Track
    ✌️ Two Fingers	Previous Track
    👍 Thumbs Up	Volume Up
    👎 Thumbs Down	Volume Down
    👌 OK	Mute / Unmute
    👉 Swipe Right	Next Track
    👈 Swipe Left	Previous Track
    👆 Swipe Up	Volume Up
    👇 Swipe Down	Volume Down
🎥 Real-Time ML Detection

    MediaPipe Hands (21-keypoint tracking)

    Custom TensorFlow model for gesture classification

    Live webcam inference

    Gesture stabilization & smoothing

🎶 Music Player Features

    Dynamic playlist

    “Now Playing” metadata

    Smooth UI animations

    Volume, mute, seekbar

    Custom Songs support

    Gesture + keyboard control

🌐 Backend Features (Django)

    Django REST Framework API

    Secure user authentication

    Modular apps:

    users/

    gestures/

    music_control/

    Real-time gesture endpoint

🧠 Machine Learning

    Trained using:

    TensorFlow

    NumPy

    OpenCV

    MediaPipe

    Custom dataset

    Includes:

    keras_model.h5

    labels.txt

📦 Tech Stack
🎯 Frontend

    HTML5, CSS3

    JavaScript

    MediaPipe

    Webcam API

⚙ Backend

    Python 3.11+

    Django 5+

    Django REST Framework

🧠 ML

    TensorFlow

    OpenCV

    NumPy

🖥 Deployment Ready For

    Render

    Railway

    Heroku

    GitHub Actions

📁 Project Structure
AI-Hand-Music-Controller/
│
├── backend/
│   ├── backend_project/
│   ├── devices/
│   ├── gestures/
│   │     └── ml/
│   │          ├── keras_model.h5
│   │          ├── labels.txt
│   │          └── real_time_teachable.py
│   ├── music_control/
│   ├── static/
│   │     ├── css/
│   │     ├── js/
│   │     └── media/
│   ├── templates/
│   ├── users/
│   └── manage.py
│
├── requirements.txt
├── runtime.txt
├── .gitignore
└── README.md

🛠 Installation & Setup
1️⃣ Clone the Repository
    git clone https://github.com/AbhaySinha1909/WAVETUNES.git
    cd Wave_Tunes/backend

2️⃣ Create Virtual Environment
    python -m venv venv


Activate it:

Windows

    .\venv\Scripts\activate


Linux/Mac

    source venv/bin/activate

3️⃣ Install Requirements
    pip install -r requirements.txt

4️⃣ Run Migrations
    python manage.py migrate

5️⃣ Start Server
    python manage.py runserver

6️⃣ Open in Browser

👉 http://127.0.0.1:8000

🎬 How to Use

    Allow webcam access

    Login → Go to /music

    Show your hand in camera

    Use gestures to control songs

    Enjoy the futuristic experience 🎧

🚀 Deployment (Render)
Build Command:
pip install -r requirements.txt

Start Command:
gunicorn backend_project.wsgi

🤝 Contributing

Pull requests are welcome!
For major changes, open an issue to discuss.

📄 License

Licensed under the MIT License — free to use & modify.

👤 Author

Abhay Sinha
AI/ML Engineer & Full-Stack Developer
GitHub — AbhaySinha1909