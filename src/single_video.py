from pathlib import Path
import subprocess

from utils import json_folder_to_skels


def run_single_video(config, video_path):
    video_path = Path(video_path)

    if not video_path.exists():
        raise FileNotFoundError(video_path)

    video_name = video_path.stem

    output_root = Path("outputs/single_videos") / video_name
    json_dir = output_root / "keypoints"
    skels_path = output_root / f"{video_name}.skels"

    json_dir.mkdir(parents=True, exist_ok=True)

    openpose_cmd = [
        "openpose.bin",   # change path if needed
        "--video", str(video_path),
        "--hand",
        "--display", "0",
        "--render_pose", "0",
        "--write_json", str(json_dir)
    ]

    subprocess.run(openpose_cmd, check=True)

    json_folder_to_skels(
        json_dir=json_dir,
        output_path=skels_path,
        preprocess_cfg=config["preprocessing"]
    )
