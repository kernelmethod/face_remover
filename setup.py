#!/usr/bin/env python

from distutils.core import setup
from pathlib import Path

BASE = Path(__file__).parent

with open("requirements.txt", "r") as f:
    install_requires = f.readlines()

setup(
    name='face_remover',
    version='0.1.0',
    description='Face and EXIF metadata removal utility',
    author='kernelmethod',
    author_email='17100608+kernelmethod@users.noreply.github.com',
    url='https://github.com/kernelmethod/face_remover',
    packages=["face_remover"],
    install_requires=install_requires,
    scripts=[str(BASE / "scripts" / "face_remover")],
)
