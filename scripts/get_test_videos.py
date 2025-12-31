import os

TEST_VIDEO_DIR = r"C:\Users\Gunajothi\OneDrive\Desktop\Pheonix\dataset\test"

videos = sorted([
    v.replace(".mp4", "")
    for v in os.listdir(TEST_VIDEO_DIR)
    if v.endswith(".mp4")
])


first_5 = videos[:5]

print("Selected TEST videos:")
for v in first_5:
    print(v)
