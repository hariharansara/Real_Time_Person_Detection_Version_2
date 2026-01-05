import face_recognition
import numpy as np
import pickle
import cv2

EMBED_PATH = "app/model/embeddings.npy"
NAMES_PATH = "app/model/names.pkl"   

encodings = np.load(EMBED_PATH, allow_pickle=True)

with open(NAMES_PATH, "rb") as f:
    names = pickle.load(f)


def recognize_face(frame):

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    if len(face_encodings) == 0:
        return "No Face"

    for encoding in face_encodings:
        distances = face_recognition.face_distance(encodings, encoding)
        idx = np.argmin(distances)

        if distances[idx] < 0.60:   
            return names[idx]

    return "Unauthorized"

