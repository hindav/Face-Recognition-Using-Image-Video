from flask import Flask, render_template, Response, request
import cv2
import numpy as np
import pickle
import face_recognition

app = Flask(__name__)

# Load the face encodings from the pickle file
with open("encoded_faces.pkl", "rb") as f:
    known_face_encodings, known_face_names = pickle.load(f)

def detect_faces(frame):
    # Increase the resolution of the frame
    frame = cv2.resize(frame, (0, 0), fx=2.0, fy=2.0)

    # Convert the image from BGR color to RGB color
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Find all the faces and face encodings in the current frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # See if the face matches any known faces
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)  # Adjust tolerance as needed
        name = "Unknown"

        # If a match is found, use the known name
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        face_names.append(name)

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with the name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    return frame
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index.html')
def home():
    return render_template('index.html')

@app.route('/team.html')
def team():
    return render_template('team.html')

@app.route('/service.html')
def service():
    return render_template('service.html')

@app.route('/image_recognition.html')
def image_recognition():
    return render_template('image_recognition.html')

@app.route('/live_recognition.html')
def live_recognition():
    return render_template('live_recognition.html')

@app.route('/video_recognition.html')
def video_recognition():
    return render_template('video_recognition.html')

@app.route('/image', methods=['POST'])
def image():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        image = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)
        frame = detect_faces(image)
        _, buffer = cv2.imencode('.jpg', frame)
        return Response(buffer.tobytes(), mimetype='image/jpeg')
    return "No file selected!"

def generate_frames(video_path):
    video_capture = cv2.VideoCapture(video_path)
    while video_capture.isOpened():
        ret, frame = video_capture.read()
        if not ret:
            break
        frame = detect_faces(frame)
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    video_capture.release()

@app.route('/video', methods=['POST'])
def video():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        video_path = 'temp_video.mp4'
        uploaded_file.save(video_path)
        return Response(generate_frames(video_path), mimetype='multipart/x-mixed-replace; boundary=frame')
    return "No file selected!"


def live_face_recognition():
    video_capture = cv2.VideoCapture(0)
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        frame = detect_faces(frame)
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    video_capture.release()

@app.route('/live')
def live():
    return Response(live_face_recognition(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
