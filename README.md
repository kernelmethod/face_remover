# face_remover

A simple Python script to remove faces and EXIF metadata from images.

![Barack Obama before/after removing face from image.](assets/results_1.png)

## Usage

Install the package in a new virtual environment with

```
$ python3 -m venv venv
$ source ./venv/bin/activate
(venv) $ pip install git+https://github.com/kernelmethod/face_remover.git
```

This will install a new script `face_remover` that will be available to you on
your PATH while the virtual environment is activated. Run

```
(venv) $ face_remover --help
```

for more information on how to use the script.
