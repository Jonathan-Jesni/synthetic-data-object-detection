import bpy
import random
import os
from bpy_extras.object_utils import world_to_camera_view

# =====================
# PATHS
# =====================
BASE_DIR = bpy.path.abspath("//")
OUTPUT_DIR = os.path.join(BASE_DIR, "renders")
IMAGE_DIR = os.path.join(OUTPUT_DIR, "images")
LABEL_DIR = os.path.join(OUTPUT_DIR, "labels")

os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(LABEL_DIR, exist_ok=True)

# =====================
# OBJECTS
# =====================
OBJECT_NAMES = ["Table", "Bottle", "Ball"]

CLASSES = {
    "Table": 0,
    "Bottle": 1,
    "Ball": 2
}

scene = bpy.context.scene
camera = bpy.data.objects["Camera"]

# =====================
# SAVE ORIGINAL TRANSFORMS
# =====================
original = {}
for name in OBJECT_NAMES:
    obj = bpy.data.objects.get(name)
    original[name] = {
        "loc": obj.location.copy(),
        "rot": obj.rotation_euler.copy(),
        "scale": obj.scale.copy()
    }

# =====================
# SETTINGS
# =====================
NUM_IMAGES = 200
scene.render.image_settings.file_format = "PNG"

# =====================
# YOLO BBOX (CORRECT)
# =====================
def get_yolo_bbox(obj):
    bpy.context.view_layer.update()

    coords = []
    for v in obj.data.vertices:
        world_v = obj.matrix_world @ v.co
        co_ndc = world_to_camera_view(scene, camera, world_v)
        coords.append(co_ndc)

    xs = [c.x for c in coords if 0 <= c.x <= 1 and 0 <= c.y <= 1]
    ys = [c.y for c in coords if 0 <= c.x <= 1 and 0 <= c.y <= 1]

    if not xs or not ys:
        return None  # object not visible

    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)

    x_center = (x_min + x_max) / 2
    y_center = (y_min + y_max) / 2
    width = x_max - x_min
    height = y_max - y_min

    return x_center, y_center, width, height

# =====================
# MAIN LOOP
# =====================
for i in range(NUM_IMAGES):

    # randomize (simple, safe)
    for name in OBJECT_NAMES:
        obj = bpy.data.objects[name]

        obj.location.x = original[name]["loc"].x + random.uniform(-0.3, 0.3)
        obj.location.y = original[name]["loc"].y + random.uniform(-0.3, 0.3)
        obj.rotation_euler.z = original[name]["rot"].z + random.uniform(-0.3, 0.3)

        s = random.uniform(0.9, 1.1)
        obj.scale = original[name]["scale"] * s

    image_path = os.path.join(IMAGE_DIR, f"render_{i}.png")
    label_path = os.path.join(LABEL_DIR, f"render_{i}.txt")

    scene.render.filepath = image_path
    bpy.ops.render.render(write_still=True)

    with open(label_path, "w") as f:
        for name in OBJECT_NAMES:
            obj = bpy.data.objects[name]
            bbox = get_yolo_bbox(obj)

            if bbox is None:
                continue

            x, y, w, h = bbox

            # final safety clamp
            if w <= 0 or h <= 0:
                continue

            cls_id = CLASSES[name]
            f.write(f"{cls_id} {x:.6f} {y:.6f} {w:.6f} {h:.6f}\n")

    print(f"Rendered {i+1}/{NUM_IMAGES}")

print("✅ Rendering complete")
