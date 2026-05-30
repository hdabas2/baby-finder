import os
import shutil
import cv2
import numpy as np
from insightface.app import FaceAnalysis

# =====================================
# CONFIGURATION
# =====================================

REFERENCE_FOLDER = r"D:\baby-finder\reference"
SEARCH_FOLDER = r"E:\mobile\data"
MATCH_FOLDER = r"D:\baby-finder\matches\videos"

SIMILARITY_THRESHOLD = 0.45

# Check one frame every N seconds
FRAME_INTERVAL_SECONDS = 5

# =====================================
# INITIALIZE MODEL
# =====================================

print("Loading InsightFace model...")

app = FaceAnalysis(
    name="buffalo_l",
    providers=["CPUExecutionProvider"]
)

app.prepare(ctx_id=0)

os.makedirs(MATCH_FOLDER, exist_ok=True)

# =====================================
# LOAD REFERENCE FACES
# =====================================

reference_embeddings = []

print("\nLoading reference photos...\n")

for filename in os.listdir(REFERENCE_FOLDER):

    if not filename.lower().endswith(
        (".jpg", ".jpeg", ".png", ".webp")
    ):
        continue

    path = os.path.join(REFERENCE_FOLDER, filename)

    try:

        image = cv2.imread(path)

        if image is None:
            continue

        faces = app.get(image)

        if len(faces) == 0:
            print(f"No face found: {filename}")
            continue

        reference_embeddings.append(
            faces[0].embedding
        )

        print(f"Loaded: {filename}")

    except Exception as e:
        print(f"Error loading {filename}: {e}")

print(
    f"\nLoaded {len(reference_embeddings)} reference faces.\n"
)

if len(reference_embeddings) == 0:
    print("No reference faces found.")
    exit()

# =====================================
# VIDEO SETTINGS
# =====================================

VIDEO_EXTENSIONS = (
    ".mp4",
    ".mov",
    ".avi",
    ".mkv",
    ".3gp",
    ".m4v"
)

# =====================================
# MATCH FUNCTION
# =====================================

def is_baby_face(face_embedding):

    for ref_embedding in reference_embeddings:

        similarity = np.dot(
            face_embedding,
            ref_embedding
        ) / (
            np.linalg.norm(face_embedding)
            * np.linalg.norm(ref_embedding)
        )

        if similarity >= SIMILARITY_THRESHOLD:
            return True

    return False


# =====================================
# VIDEO SCAN
# =====================================

videos_scanned = 0
videos_matched = 0

for root, dirs, files in os.walk(SEARCH_FOLDER):

    for filename in files:

        if not filename.lower().endswith(
            VIDEO_EXTENSIONS
        ):
            continue

        video_path = os.path.join(root, filename)

        videos_scanned += 1

        print(
            f"\n[{videos_scanned}] Checking: {video_path}"
        )

        try:

            cap = cv2.VideoCapture(video_path)

            if not cap.isOpened():
                print("Cannot open video")
                continue

            fps = cap.get(
                cv2.CAP_PROP_FPS
            )

            if fps <= 0:
                fps = 30

            frame_interval = int(
                fps * FRAME_INTERVAL_SECONDS
            )

            frame_count = 0
            found_match = False

            while True:

                ret, frame = cap.read()

                if not ret:
                    break

                if frame_count % frame_interval == 0:

                    try:

                        faces = app.get(frame)

                        for face in faces:

                            if is_baby_face(
                                face.embedding
                            ):
                                found_match = True
                                break

                        if found_match:
                            break

                    except Exception:
                        pass

                frame_count += 1

            cap.release()

            if found_match:

                destination = os.path.join(
                    MATCH_FOLDER,
                    filename
                )

                if os.path.exists(destination):

                    base, ext = os.path.splitext(
                        filename
                    )

                    counter = 1

                    while True:

                        new_name = (
                            f"{base}_{counter}{ext}"
                        )

                        destination = os.path.join(
                            MATCH_FOLDER,
                            new_name
                        )

                        if not os.path.exists(
                            destination
                        ):
                            break

                        counter += 1

                shutil.move(
                    video_path,
                    destination
                )

                videos_matched += 1

                print(
                    f"VIDEO MATCH FOUND!"
                )

        except Exception as e:

            print(
                f"Error: {video_path}"
            )

print("\n================================")
print(f"Videos scanned : {videos_scanned}")
print(f"Videos matched : {videos_matched}")
print("================================")
print("Done.")
