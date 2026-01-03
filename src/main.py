import argparse

from config import load_config
from preprocess import run_preprocessing
from single_video import run_single_video


def parse_args():
    parser = argparse.ArgumentParser(
        description="Spoken2Sign preprocessing pipeline"
    )

    parser.add_argument(
        "--config",
        type=str,
        required=True,
        help="Path to pipeline.yaml"
    )

    parser.add_argument(
        "--split",
        type=str,
        choices=["train", "dev", "test"],
        help="Dataset split to process"
    )

    parser.add_argument(
        "--video",
        type=str,
        help="Path to a single video"
    )

    args = parser.parse_args()

    if args.split is None and args.video is None:
        raise ValueError("Either --split or --video must be provided")

    if args.split is not None and args.video is not None:
        raise ValueError("Provide only one of --split or --video")

    return args


def main():
    args = parse_args()
    config = load_config(args.config)

    if args.split:
        run_preprocessing(config, args.split)

    elif args.video:
        run_single_video(config, args.video)


if __name__ == "__main__":
    main()
