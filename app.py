from flask import Flask, render_template, Response, request
import cv2
import numpy as np
import pickle
import face_recognition

app = Flask(__name__)

# Load the face encodings from the pickle file
with open("encoded_faces.pkl", "rb") as f:
    known_face_encodings, known_face_names = pickle.load(f)

def detect_faces(frame: np.ndarray) -> np.ndarray:
    try:
        print(f"Frame shape: {frame.shape}, dtype: {frame.dtype}")  # Debugging info

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
    except Exception as e:
        print(f"Error in detect_faces: {str(e)}")
        return frame  # Return the original frame if any error occurs

@app.route('/')
def index() -> str:
    return render_template('index.html')

# ... (rest of the code remains the same)

if __name__ == "__main__":
    app.run(debug=True)
