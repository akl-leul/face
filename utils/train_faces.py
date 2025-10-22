import os
import cv2
import face_recognition
import pickle
from config import UPLOAD_FOLDER, ENCODINGS_PATH

def train_new_faces():
    known_encodings = []
    known_names = []
    for img_name in os.listdir(UPLOAD_FOLDER):
        path = os.path.join(UPLOAD_FOLDER, img_name)
        image = face_recognition.load_image_file(path)
        encodings = face_recognition.face_encodings(image)
        if len(encodings) > 0:
            known_encodings.append(encodings[0])
            known_names.append(img_name.split(".")[0])

    data = {"encodings": known_encodings, "names": known_names}
    with open(ENCODINGS_PATH, "wb") as f:
        pickle.dump(data, f)
    print("Training completed!")
