import cv2
import numpy as np
from PIL import Image


def expand_box(x1: int, y1: int, x2: int, y2: int, scale_factor: float):
    """Expand a rectangular box by some scaling factor. Used to rescale the
    boxes placed around faces."""
    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2
    width = (x2 - x1) * scale_factor
    height = (y2 - y1) * scale_factor
    x1 = round(center_x - width / 2)
    x2 = round(center_x + width / 2)
    y1 = round(center_y - height / 2)
    y2 = round(center_y + height / 2)
    return x1, y1, x2, y2


def blackout_faces(
    filename: str, box_scale_factor: float = 1, min_confidence: float = 0.95
):
    """Find all of the faces in an image and obscure them with black boxes."""
    # This import automatically launches some code to check for attached GPUs, the
    # presence of libcuda.so, etc. This can generate a decent amount of output as
    # well as slow down the script quite a bit.
    #
    # For that reason, we delay this import until this function so that if for
    # whatever reason this function doesn't get called (e.g. if the user just wants
    # to get usage information) we don't run the checker script.
    from mtcnn import MTCNN

    img = cv2.cvtColor(cv2.imread(filename), cv2.COLOR_BGR2RGB)
    detector = MTCNN()
    results = detector.detect_faces(img)

    # Make a copy of the original image to return alongside the
    # modified image
    orig = img.copy()

    n_thrown_out = 0
    for res in results:
        if res["confidence"] < min_confidence:
            n_thrown_out += 1
            continue
        box = res["box"]

        x1, y1, width, height = box
        x2, y2 = x1 + width, y1 + height
        x1, y1, x2, y2 = expand_box(x1, y1, x2, y2, box_scale_factor)
        x1 = max(x1, 0)
        x2 = min(x2, img.shape[1])
        y1 = max(y1, 0)
        y2 = min(y2, img.shape[0])

        img[y1:y2, x1:x2] = 0

    print(f"Found {len(results)} faces (skipped {n_thrown_out})")
    return orig, img


def save_image(img: np.ndarray, outfile: str):
    """Save a numpy array as an image to an output file."""
    img = Image.fromarray(img)
    img.save(outfile)
