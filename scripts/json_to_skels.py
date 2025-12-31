import os
import json
import numpy as np

# ---------------- CONFIG ----------------
JSON_DIR = r"C:\Users\Gunajothi\OneDrive\Desktop\Pheonix\keypoints\train\01April_2010_Thursday_heute-6701"
OUT_DIR  = r"C:\Users\Gunajothi\OneDrive\Desktop\Pheonix\skels\train"
VIDEO_ID = "01April_2010_Thursday_heute-6701"

os.makedirs(OUT_DIR, exist_ok=True)
OUT_FILE = os.path.join(OUT_DIR, VIDEO_ID + ".skels")

# Upper body joints (OpenPose BODY_25 indices)
UPPER_BODY = [1, 2, 3, 4, 5, 6, 7, 8]  # neck, shoulders, arms

# ----------------------------------------

def extract_joints(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)

    if len(data["people"]) == 0:
        return np.zeros((50, 3))

    p = data["people"][0]

    pose = np.array(p["pose_keypoints_2d"]).reshape(-1, 3)
    lh   = np.array(p["hand_left_keypoints_2d"]).reshape(-1, 3)
    rh   = np.array(p["hand_right_keypoints_2d"]).reshape(-1, 3)

    selected = []
    selected.extend(pose[UPPER_BODY])
    selected.extend(lh)
    selected.extend(rh)

    return np.array(selected)  # (50, 3)


# ----------- PROCESS ALL FRAMES ----------
frames = sorted([f for f in os.listdir(JSON_DIR) if f.endswith(".json")])

with open(OUT_FILE, "w") as out:
    for jf in frames:
        kp = extract_joints(os.path.join(JSON_DIR, jf))

        # Normalize x, y per frame
        xy = kp[:, :2]
        conf = kp[:, 2]

        mean = xy.mean(axis=0)
        std = xy.std(axis=0) + 1e-6
        xy_norm = (xy - mean) / std

        frame_vec = np.concatenate([
            xy_norm[:, 0],   # x1..x50
            xy_norm[:, 1],   # y1..y50
            conf             # z1..z50 (confidence)
        ])

        out.write(" ".join(f"{v:.5f}" for v in frame_vec) + "\n")

print("✅ Saved:", OUT_FILE)
