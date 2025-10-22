from flask import Flask, render_template, request, redirect, url_for, Response
import os
import pickle
import cv2
import face_recognition
from config import *
from utils.train_faces import train_new_faces
from utils.recognize_faces import recognize_stream
import sqlite3

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists('models'):
    os.makedirs('models')

# Initialize DB
conn = sqlite3.connect(DATABASE, check_same_thread=False)
conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, image TEXT)')
conn.commit()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    name = request.form['name']
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = f"{name}.jpg"
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        conn.execute("INSERT INTO users (name, image) VALUES (?, ?)", (name, filename))
        conn.commit()
        train_new_faces()
        return redirect(url_for('dashboard'))
    return 'Invalid upload!'

@app.route('/dashboard')
def dashboard():
    cur = conn.cursor()
    users = cur.execute("SELECT * FROM users").fetchall()
    return render_template('dashboard.html', users=users)

@app.route('/video_feed')
def video_feed():
    return Response(recognize_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/camera')
def camera():
    return render_template('video.html')

if __name__ == '__main__':
    app.run(debug=True)
