#!/usr/bin/env python3

import argparse
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

from mtcnn import MTCNN
from PIL import Image

"""
CLI arguments
"""

parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)

parser.add_argument(
    "image_file", type=str, help="File that the image should be read from."
)

parser.add_argument(
    "--box_scale_factor",
    type=float,
    help="Scaling factor for boxes placed over faces",
    default=1.5,
)

parser.add_argument(
    "--confidence",
    type=float,
    help="Minimum confidence needed to determine that a part of the image is a face",
    default=0.80,
)

"""
Function definitions
"""


def expand_box(x1, y1, x2, y2, scale_factor):
    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2
    width = (x2 - x1) * scale_factor
    height = (y2 - y1) * scale_factor
    x1 = round(center_x - width / 2)
    x2 = round(center_x + width / 2)
    y1 = round(center_y - height / 2)
    y2 = round(center_y + height / 2)
    return x1, y1, x2, y2


def blackout_faces(filename, box_scale_factor=1, min_confidence=0.95):
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


def save_image(img, outfile):
    img = Image.fromarray(img)
    img.save(outfile)


"""
Script
"""

if __name__ == "__main__":
    args = parser.parse_args()
    filename = args.image_file
    scale_factor = args.box_scale_factor
    min_confidence = args.confidence

    orig, img = blackout_faces(
        filename, box_scale_factor=args.box_scale_factor, min_confidence=min_confidence
    )

    # Save file
    filename, ext = os.path.splitext(filename)
    outfile = f"{filename}.blacked_out{ext}"
    save_image(img, outfile)

    print()
    print(f"Image saved to {outfile}")

    # Display image to user
    fig, axes = plt.subplots(1, 2, figsize=(20, 10))
    axes[0].imshow(orig)
    axes[1].imshow(img)
    for ax in axes:
        ax.set_xticks([])
        ax.set_yticks([])

    plt.show()
