from setuptools import setup, find_packages

#the folders with __init__.py will be considered as package and will be found by find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="document_portal",
    version="0.1",
    author="Deepank Dixit",
    packages=find_packages(), # auto-discovers packages
    install_requires = requirements #won't have to install requirements.txt separately. Only need to run pip install -e .
)

"""
1. About find_packages() in setup.py

The find_packages() function (from setuptools) automatically discovers all packages and sub-packages in your project directory.
It does this by looking for directories that contain an __init__.py file (which marks them as Python packages).
This saves you from manually listing each package in the packages argument of setup().
"""