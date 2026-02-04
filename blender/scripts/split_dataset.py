import os
import random
import shutil

# =====================
# PROJECT ROOT
# =====================
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

# =====================
# SOURCE (RENDERS)
# =====================
SRC_IMAGES = os.path.join(PROJECT_ROOT, "blender", "renders", "images")
SRC_LABELS = os.path.join(PROJECT_ROOT, "blender", "renders", "labels")

# =====================
# DESTINATION (DATASET)
# =====================
DST_IMAGES_TRAIN = os.path.join(PROJECT_ROOT, "dataset", "images", "train")
DST_IMAGES_VAL = os.path.join(PROJECT_ROOT, "dataset", "images", "val")
DST_LABELS_TRAIN = os.path.join(PROJECT_ROOT, "dataset", "labels", "train")
DST_LABELS_VAL = os.path.join(PROJECT_ROOT, "dataset", "labels", "val")

os.makedirs(DST_IMAGES_TRAIN, exist_ok=True)
os.makedirs(DST_IMAGES_VAL, exist_ok=True)
os.makedirs(DST_LABELS_TRAIN, exist_ok=True)
os.makedirs(DST_LABELS_VAL, exist_ok=True)

# =====================
# SPLIT
# =====================
images = [f for f in os.listdir(SRC_IMAGES) if f.endswith(".png")]
random.shuffle(images)

split_idx = int(0.8 * len(images))
train_imgs = images[:split_idx]
val_imgs = images[split_idx:]

# =====================
# COPY FILES
# =====================
def copy_files(files, img_dst, lbl_dst):
    for img in files:
        lbl = img.replace(".png", ".txt")

        shutil.copy2(
            os.path.join(SRC_IMAGES, img),
            os.path.join(img_dst, img)
        )

        shutil.copy2(
            os.path.join(SRC_LABELS, lbl),
            os.path.join(lbl_dst, lbl)
        )

copy_files(train_imgs, DST_IMAGES_TRAIN, DST_LABELS_TRAIN)
copy_files(val_imgs, DST_IMAGES_VAL, DST_LABELS_VAL)

print("Dataset split complete (files copied, originals preserved)")
