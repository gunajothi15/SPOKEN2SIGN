import gzip
import os

# -------- PATHS --------
ANNO_FILE = r"C:\Users\Gunajothi\OneDrive\Desktop\Pheonix\annotations\phoenix14t.pami0.train.annotations_only.gzip"
TRAIN_VIDEO_DIR = r"C:\Users\Gunajothi\OneDrive\Desktop\Pheonix\dataset\train"
OUT_FILE = "train_selected_annotations.txt"
# ----------------------

# Step 1: collect selected video names
selected_videos = sorted([
    v.replace(".mp4", "")
    for v in os.listdir(TRAIN_VIDEO_DIR)
    if v.endswith(".mp4")
])[:40]

selected_set = set(selected_videos)

print("Filtering annotations for:")
for v in selected_videos:
    print(" ", v)

print("\nExtracted annotations:\n")

count = 0

with gzip.open(ANNO_FILE, "rt", encoding="utf-8", errors="ignore") as f, \
     open(OUT_FILE, "w", encoding="utf-8") as out:

    for block in f.read().split("u}"):
        for vid in selected_set:
            if f"train/{vid}" in block:
                out.write(block + "\n\n")
                print("✔ Found:", vid)
                count += 1
                break

print(f"\nTotal matched annotations: {count}")
print(f"Saved to: {OUT_FILE}")
