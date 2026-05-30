A Python-based tool that uses AI face recognition to find photos and videos of a specific person (e.g. your baby) from large media backups.

**Features**
1. Scan thousands of photos & videos recursively
2. Supports nested folder structures
3. Works with Python 3.12+

**Folder Structure**
baby-finder/
├── reference/     # Reference photos of the person to find
├── matches/       # Matched photos/videos
├── find_baby.py
├── find_baby_videos.py

**Update the following paths inside the script:**
1. REFERENCE_FOLDER = r"D:\baby-finder\reference" (Contains 5–10 clear reference photos)
2. SEARCH_FOLDER = r"E:\mobile\data" (Root folder containing photos/videos to scan)
3. MATCH_FOLDER = r"D:\baby-finder\matches" (Destination folder for matched files.)

**Run**
1. Scan photos:python find_baby.py
2. Scan videos:python find_baby_videos.py

**Notes**
1. Use clear reference photos for better accuracy.
2. This script will move the files from source to destination. 

This project is intended for personal media organization and face-matching experiments. Always respect privacy and obtain permission before processing media belonging to others.
