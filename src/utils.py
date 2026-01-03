import json
from pathlib import Path
from typing import Dict

import numpy as np


# OpenPose BODY_25 upper-body joint indices
UPPER_BODY_JOINTS = [1, 2, 3, 4, 5, 6, 7, 8]


def _load_json(json_path: Path) -> Dict:
    with open(json_path, "r") as f:
        return json.load(f)


def _extract_keypoints(frame_data: Dict) -> np.ndarray:
    """
    Extract 50 joints: upper body + left hand + right hand
    Returns shape (50, 3)
    """
    if len(frame_data["people"]) == 0:
        return np.zeros((50, 3), dtype=np.float32)

    person = frame_data["people"][0]

    body = np.array(person["pose_keypoints_2d"]).reshape(-1, 3)
    left_hand = np.array(person["hand_left_keypoints_2d"]).reshape(-1, 3)
    right_hand = np.array(person["hand_right_keypoints_2d"]).reshape(-1, 3)

    selected = []
    selected.extend(body[UPPER_BODY_JOINTS])
    selected.extend(left_hand)
    selected.extend(right_hand)

    return np.asarray(selected, dtype=np.float32)


def _normalize_xy(kps: np.ndarray) -> np.ndarray:
    """
    Normalize x and y coordinates per frame.
    """
    xy = kps[:, :2]
    conf = kps[:, 2]

    mean = xy.mean(axis=0)
    std = xy.std(axis=0) + 1e-6

    xy_norm = (xy - mean) / std
    return np.column_stack([xy_norm, conf])


def json_folder_to_skels(
    json_dir: Path,
    output_path: Path,
    preprocess_cfg: Dict
):
    """
    Convert a folder of OpenPose JSON files into a single .skels file.
    """

    json_files = sorted(json_dir.glob("*.json"))

    if len(json_files) == 0:
        raise RuntimeError(f"No JSON files found in {json_dir}")

    frames = []

    for json_file in json_files:
        frame_data = _load_json(json_file)
        kps = _extract_keypoints(frame_data)

        if preprocess_cfg.get("normalize_xy", True):
            kps = _normalize_xy(kps)

        frame_vec = np.concatenate([
            kps[:, 0],  # x
            kps[:, 1],  # y
            kps[:, 2],  # confidence
        ])

        frames.append(frame_vec)

    frames = np.stack(frames, axis=0)  # (T, 150)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        for frame in frames:
            line = " ".join(f"{v:.5f}" for v in frame)
            f.write(line + "\n")
