import os
import shutil
import cv2
import numpy as np
from insightface.app import FaceAnalysis

# =====================================
# CONFIGURATION
# =====================================

REFERENCE_FOLDER = r"D:\baby-finder\reference"
SEARCH_FOLDER = r"E:\Harsh_phone\backup-Aug2025"
MATCH_FOLDER = r"D:\baby-finder\matches"

SIMILARITY_THRESHOLD = 0.45

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
        print(f"Error: {filename} -> {e}")

print(
    f"\nLoaded {len(reference_embeddings)} reference faces.\n"
)

if len(reference_embeddings) == 0:
    print("No reference faces found.")
    exit()

# =====================================
# SCAN PHOTOS
# =====================================

total_scanned = 0
total_matches = 0

image_extensions = (
    ".jpg",
    ".jpeg",
    ".png",
    ".webp"
)

print("Scanning photos...\n")

for root, dirs, files in os.walk(SEARCH_FOLDER):

    for filename in files:

        if not filename.lower().endswith(image_extensions):
            continue

        image_path = os.path.join(root, filename)

        total_scanned += 1

        try:

            image = cv2.imread(image_path)

            if image is None:
                continue

            faces = app.get(image)

            found_match = False

            for face in faces:

                embedding = face.embedding

                for ref_embedding in reference_embeddings:

                    similarity = np.dot(
                        embedding,
                        ref_embedding
                    ) / (
                        np.linalg.norm(embedding)
                        * np.linalg.norm(ref_embedding)
                    )

                    if similarity >= SIMILARITY_THRESHOLD:
                        found_match = True
                        break

                if found_match:
                    break

            if found_match:

                destination = os.path.join(
                    MATCH_FOLDER,
                    filename
                )

                # avoid overwriting files
                if os.path.exists(destination):

                    base, ext = os.path.splitext(filename)

                    counter = 1

                    while True:

                        new_name = (
                            f"{base}_{counter}{ext}"
                        )

                        destination = os.path.join(
                            MATCH_FOLDER,
                            new_name
                        )

                        if not os.path.exists(destination):
                            break

                        counter += 1

                shutil.move(
                    image_path,
                    destination
                )

                total_matches += 1

                print(
                    f"[MATCH {total_matches}] "
                    f"{image_path}"
                )

        except Exception as e:
            print(
                f"Skipped: {image_path}"
            )

print("\n=================================")
print(f"Photos scanned : {total_scanned}")
print(f"Matches found  : {total_matches}")
print("=================================")
print("Done.")