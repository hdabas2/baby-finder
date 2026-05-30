A Python-based tool that uses AI face recognition to find photos and videos of a specific person (e.g. your baby) from large media backups.

**Features**
Scan thousands of photos recursively
Scan videos by extracting frames at intervals
Match faces using InsightFace embeddings
Automatically move or copy matched files
Supports nested folder structures
Works on Windows with Python 3.12+

**Folder Structure**
baby-finder/
├── reference/     # Reference photos of the person to find
├── matches/       # Matched photos/videos
├── find_baby.py
├── find_baby_videos.py
Configuration

**Update the following paths inside the script:**
REFERENCE_FOLDER = r"D:\baby-finder\reference"
SEARCH_FOLDER = r"E:\mobile\data"
MATCH_FOLDER = r"D:\baby-finder\matches\videos"

REFERENCE_FOLDER → Contains 5–10 clear reference photos.
SEARCH_FOLDER → Root folder containing photos/videos to scan.
MATCH_FOLDER → Destination folder for matched files.


**Run**
Scan photos:python find_baby.py
Scan videos:python find_baby_videos.py

**Notes**
Use clear reference photos for better accuracy.
This script will move the files from source to destination. 
Disclaimer

This project is intended for personal media organization and face-matching experiments. Always respect privacy and obtain permission before processing media belonging to others.
