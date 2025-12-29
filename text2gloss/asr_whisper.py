import whisper
import os
import json

MODEL_SIZE = "small"
LANGUAGE = "de"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
OUTPUT_DIR = os.path.join(BASE_DIR, "text2gloss", "asr_text")

SPLITS = ["train", "dev", "test"]

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Loading Whisper model...")
model = whisper.load_model(MODEL_SIZE)

for split in SPLITS:
    print(f"\nProcessing {split} split...")
    
    video_dir = os.path.join(DATASET_DIR, split)
    out_dir = os.path.join(OUTPUT_DIR, split)
    os.makedirs(out_dir, exist_ok=True)

    for video in sorted(os.listdir(video_dir)):
        if not video.endswith(".mp4"):
            continue

        video_path = os.path.join(video_dir, video)
        video_id = video.replace(".mp4", "")

        print(f"Transcribing: {video}")

        result = model.transcribe(video_path, language=LANGUAGE)

        with open(
            os.path.join(out_dir, video_id + ".json"),
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(
                {
                    "video": video,
                    "text": result["text"].strip()
                },
                f,
                indent=2,
                ensure_ascii=False
            )
print("\nTranscription completed.")