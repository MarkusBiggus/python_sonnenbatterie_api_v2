#import pathlib
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="sonnenbatterie", # emulates weltmeyer package with same name
    version="0.1.0",
    author="Markus Biggus",
    author_email="author@example.com",
    description="Access Sonnenbatterie REST API V2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/markusbiggus/python_sonnenbatterie_api_v2",
    packages=["sonnenbatterie"],
    package_dir={'sonnenbatterie' : 'sonnenbatterie'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
    ],
    python_requires='>=3.6',
    install_requires=["requests","load-dotenv","setuptools","sonnen_api_v2"],
)
