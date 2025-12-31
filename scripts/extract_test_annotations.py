import os
import gzip
import pickle

# --------------------------------------------------
# PATHS (FIX THIS PATH)
# --------------------------------------------------
TEST_VIDEO_DIR = "../dataset/test"
ANNOTATION_FILE = "../annotations/phoenix14t.pami0.test.annotations_only.gzip"
OUTPUT_FILE = "test_selected_annotations.txt"

# --------------------------------------------------
# 0. Check annotation file EXISTS FIRST
# --------------------------------------------------
if not os.path.exists(ANNOTATION_FILE):
    raise FileNotFoundError(f"❌ Annotation file not found: {ANNOTATION_FILE}")

# --------------------------------------------------
# 1. Get DEV video order
# --------------------------------------------------
selected_order = sorted([
    f.replace(".mp4", "")
    for f in os.listdir(TEST_VIDEO_DIR)
    if f.endswith(".mp4")
])

print("Selected TEST videos:")
for v in selected_order:
    print(" ", v)

# --------------------------------------------------
# 2. Load annotation file
# --------------------------------------------------
with gzip.open(ANNOTATION_FILE, "rb") as f:
    data = pickle.load(f)

# --------------------------------------------------
# 3. Build lookup dictionary
# --------------------------------------------------
anno_dict = {}
for sample in data:
    vid = sample["name"].replace("test/", "")
    anno_dict[vid] = sample

# --------------------------------------------------
# 4. Write annotations in VIDEO ORDER
# --------------------------------------------------
found = 0
with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
    for vid in selected_order:
        if vid in anno_dict:
            s = anno_dict[vid]
            out.write(f"{vid}\n")
            out.write(f"GLOSS: {s['gloss']}\n")
            out.write(f"TEXT: {s['text']}\n")
            out.write(f"SIGNER: {s['signer']}\n\n")
            print("✔ Found:", vid)
            found += 1
        else:
            print("✘ Missing:", vid)

print(f"\nTotal matched annotations: {found}")
print("Saved to:", OUTPUT_FILE)
