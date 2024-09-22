import os
import face_recognition
import pickle
import time
from multiprocessing import Pool

# Function to load face encodings from a folder
def load_face_encodings(folder_path):
    face_encodings = []
    face_names = []
    folder_name = os.path.basename(folder_path)

    # Iterate over each image file in the folder
    for filename in os.listdir(folder_path):
        image_path = os.path.join(folder_path, filename)

        # Load the image file
        face_image = face_recognition.load_image_file(image_path)

        # Encode the face
        face_encoding = face_recognition.face_encodings(face_image)

        # Check if a face was found
        if len(face_encoding) > 0:
            # Add the face encoding to the list
            face_encodings.append(face_encoding[0])

            # Add the face name (folder name) to the list
            face_names.append(folder_name)

    return face_encodings, face_names


if __name__ == "__main__":
    # Initialize known face encodings and names
    known_face_encodings = []
    known_face_names = []

    # Define the root folder containing all subfolders with face images
    root_folder = "dataset"

    # Create a pool of workers for multiprocessing
    pool = Pool()

    # Measure the time to load face encodings
    start_time = time.time()

    # Iterate over each subfolder and load face encodings using multiprocessing
    results = pool.map(load_face_encodings,
                       [os.path.join(root_folder, folder_name) for folder_name in os.listdir(root_folder)])

    # Aggregate results
    for face_encodings, face_names in results:
        known_face_encodings.extend(face_encodings)
        known_face_names.extend(face_names)

        # Print the face encodings and names
        for encoding, name in zip(face_encodings, face_names):
            print("Name:", name)
            print("Face Encoding:", encoding)
            print("-" * 30)

    # Close the pool of workers
    pool.close()
    pool.join()

    # Measure the time taken to load face encodings
    end_time = time.time()
    loading_time = end_time - start_time
    print("Time taken to load face encodings:", loading_time, "seconds")

    # Save the face encodings to a pickle file
    with open("encoded_faces.pkl", "wb") as f:
        pickle.dump((known_face_encodings, known_face_names), f)
