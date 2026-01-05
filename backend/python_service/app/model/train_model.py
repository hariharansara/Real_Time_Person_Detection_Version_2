import os
import cv2
import numpy as np
import face_recognition
import pickle
from retinaface import RetinaFace

DATA_DIR = "app/data/authorized_people"
EMBED_PATH = "app/model/embeddings.npy"
MODEL_PATH = "app/model/names.pkl"


def enhance(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    L, A, B = cv2.split(img)
    L = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8,8)).apply(L)
    img = cv2.merge((L,A,B))
    img = cv2.cvtColor(img, cv2.COLOR_LAB2BGR)
    img = cv2.GaussianBlur(img,(0,0),1.5)
    img = cv2.addWeighted(img,1.6,img,-0.6,0)
    return img


def extract_face(img):

    # 1. Try face_recognition
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    loc = face_recognition.face_locations(rgb)

    if len(loc)>0:
        t,r,b,l = loc[0]
        return img[t:b,l:r]

    # 2. Try RetinaFace (stronger detection)
    faces = RetinaFace.detect_faces(img)
    if isinstance(faces,dict):
        for key in faces:
            x1,y1,x2,y2 = faces[key]['facial_area']
            return img[y1:y2,x1:x2]

    return None



def train():

    encodings=[]
    names=[]

    print("\n==== TRAINING STARTED ====\n")

    for person in os.listdir(DATA_DIR):
        p_fold = os.path.join(DATA_DIR,person)
        if not os.path.isdir(p_fold): continue

        print(f"\nTraining: {person}")
        total=0; passed=0

        for img_file in os.listdir(p_fold):
            total+=1
            img_path = os.path.join(p_fold,img_file)
            img = cv2.imread(img_path)

            if img is None:
                print(f" ✖ Cannot read → {img_file}")
                continue

            face = extract_face(img)

            if face is None:                     # try enhanced image
                face = extract_face(enhance(img))

            if face is None:
                print(f" ✖ No face detected → {img_file}")
                continue

            face = cv2.resize(face,(256,256))
            enc = face_recognition.face_encodings(face)

            if len(enc)>0:
                encodings.append(enc[0])
                names.append(person)
                passed+=1
                print(f" ✔ Trained → {img_file}")
            else:
                print(f" ✖ Encoding failed → {img_file}")

        print(f"Summary: {passed}/{total} trained")


    np.save(EMBED_PATH,encodings)
    with open(MODEL_PATH,"wb") as f:
        pickle.dump(names,f)

    print("\n==== TRAINING COMPLETE ====")
    print("Encodings:", len(encodings))
    print("Users:",set(names))
    print("Saved:",EMBED_PATH," & ",MODEL_PATH,"\n")


if __name__ == "__main__":
    train()
