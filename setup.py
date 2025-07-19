from setuptools import setup, find_packages

#the folders with __init__.py will be considered as package and will be found by find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="document_portal",
    version="0.1",
    author="Deepank Dixit",
    packages=find_packages(),
)