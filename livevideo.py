from flask import Flask, render_template, Response
from flask_socketio import SocketIO
import cv2
import numpy as np
import face_recognition
import os

app = Flask(__name__)
socketio = SocketIO(app)

# Read images and names from the specified directory
PATH = "faceImages"
images = []
image_names = []
for file_name in os.listdir(PATH):
    image = cv2.imread(f"{PATH}/{file_name}")
    images.append(image)
    image_names.append(os.path.splitext(file_name)[0])

#Encode images
encode_list = []
for image in images:
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    encoding = face_recognition.face_encodings(rgb_image)[0]
    encode_list.append(encoding)

# Video capture
cap = cv2.VideoCapture(0)

def generate_frames():
    frame_counter = 0
    while True:
        success, img = cap.read()
        if not success:
            continue

        # Only run detection and recognition on every other frame
        if frame_counter % 2 == 0:
            img_small = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            img_small = cv2.cvtColor(img_small, cv2.COLOR_BGR2RGB)

            face_locations = face_recognition.face_locations(img_small)
            encodings = face_recognition.face_encodings(img_small, face_locations)

            for encoding, location in zip(encodings, face_locations):
                matches = face_recognition.compare_faces(encode_list,encoding)
                distances = face_recognition.face_distance(encode_list,encoding)
                min_distance_idx=np.argmin(distances)

                if matches[min_distance_idx]:
                    name=image_names[min_distance_idx].upper()
                    #match_perc= round(calculate_confidence(distances[min_distance_idx])*100)
                    match_perc = round((1 - distances[min_distance_idx]) * 100)
                else:
                    name = "Unknown"
                    match_perc = "???"

                top, right, bottom, left = [4 * n for n in location]
                cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(img, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                cv2.putText(img, f"{name} {match_perc}%", (left + 6, bottom - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

        ret, buffer = cv2.imencode('.jpg', img)
        img_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + img_bytes + b'\r\n')

        frame_counter += 1

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

@app.route('/video_feed')
def video_feed():
    #Video streaming route.
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    #Video streaming Home Page
    return render_template('index.html')

def run():
    socketio.run(app)