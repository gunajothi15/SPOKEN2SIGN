import os

DEV_VIDEO_DIR = r"C:\Users\Gunajothi\OneDrive\Desktop\Pheonix\dataset\dev"

videos = sorted([
    v.replace(".mp4", "")
    for v in os.listdir(DEV_VIDEO_DIR)
    if v.endswith(".mp4")
])

first_10 = videos[:10]

print("Selected DEV videos:")
for v in first_10:
    print(v)
