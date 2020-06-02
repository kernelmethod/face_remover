# face_remover

A simple Python script to remove faces and EXIF metadata from images.

![Barack Obama before/after removing face from image.](assets/results_1.png)

## Usage
After installing the dependencies in `requirements.txt`, you can run the script with

```
$ python3 script.py /path/to/image
```

This will generate a new version of the image with faces obscured by black rectangles in the same directory as the image.

The default options for the script are pretty reliable, but you can fine-tune it a little more with some flags provided by the script.

```
$ python3 script.py --help
Using TensorFlow backend.
usage: script.py [-h] [--box_scale_factor BOX_SCALE_FACTOR] [--confidence CONFIDENCE] image_file

positional arguments:
  image_file            File that the image should be read from.

optional arguments:
  -h, --help            show this help message and exit
  --box_scale_factor BOX_SCALE_FACTOR
                        Scaling factor for boxes placed over faces (default: 1.5)
  --confidence CONFIDENCE
                        Minimum confidence needed to determine that a part of the image is a face (default: 0.8)
```
