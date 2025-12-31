import os

TRAIN_VIDEO_DIR = r"C:\Users\Gunajothi\OneDrive\Desktop\Pheonix\dataset\train"

videos = sorted([
    v.replace(".mp4", "")
    for v in os.listdir(TRAIN_VIDEO_DIR)
    if v.endswith(".mp4")
])

first_5 = videos[:5]

print("Selected TRAIN videos:")
for v in first_5:
    print(v)
