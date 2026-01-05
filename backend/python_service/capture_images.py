import cv2
import os
import time

name = "Hariharan"  
save_dir = f"backend/python-service/app/data/authorized_people/{name}"

os.makedirs(save_dir, exist_ok=True)

cam = cv2.VideoCapture(0)
if not cam.isOpened():
    print("\nCamera not detected. Try:")
    print("1. Close all apps using camera")
    print("2. Change camera index to 1 or 2")
    exit()

print("\nLook at camera. Capture starts in 3 seconds...")
time.sleep(3)

count = 0
while count < 50:                     # increase dataset count
    ret, frame = cam.read()
    if not ret:
        print("Frame read failed")
        break

    cv2.imshow("Capturing - press 'q' to stop", frame)
    img_path = f"{save_dir}/img_{count}.jpg"
    cv2.imwrite(img_path, frame)
    count += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
print(f"\nSaved {count} images to: {save_dir}")
print("Now run → python app/model/train_model.py")

