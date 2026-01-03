from pathlib import Path
from typing import Dict

from utils import json_folder_to_skels


def run_preprocessing(config: Dict, split: str):
    """
    Run preprocessing for a given split.
    Converts OpenPose JSON folders into .skels files.
    """

    dataset_root = Path(config["paths"]["dataset_root"])
    keypoints_root = Path(config["paths"]["keypoints_root"])
    skels_root = Path(config["paths"]["skels_root"])

    split_cfg = config["splits"][split]

    json_split_dir = keypoints_root / split_cfg["json_dir"]
    skels_split_dir = skels_root / split_cfg["output_dir"]

    if not json_split_dir.exists():
        raise FileNotFoundError(f"JSON directory not found: {json_split_dir}")

    skels_split_dir.mkdir(parents=True, exist_ok=True)

    video_folders = sorted([
        p for p in json_split_dir.iterdir()
        if p.is_dir()
    ])

    print(f"[INFO] Found {len(video_folders)} videos in split '{split}'")

    for video_dir in video_folders:
        video_id = video_dir.name
        output_skels = skels_split_dir / f"{video_id}.skels"

        print(f"[INFO] Processing video: {video_id}")

        json_folder_to_skels(
            json_dir=video_dir,
            output_path=output_skels,
            preprocess_cfg=config["preprocessing"]
        )
