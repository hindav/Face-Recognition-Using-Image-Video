import os

def delete_extra_photos(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Filter out directories with no photos
        photo_files = [file for file in filenames if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]
        if len(photo_files) > 1:
            # Sort photos to ensure the first one is kept
            photo_files.sort()
            # Delete extra photos except for the first one
            for photo in photo_files[1:]:
                os.remove(os.path.join(dirpath, photo))
                print(f"Deleted: {os.path.join(dirpath, photo)}")

# Example usage
root_directory = r"C:\Users\hinda\OneDrive\Desktop\Final Year Project-html\dataset"

delete_extra_photos(root_directory)
