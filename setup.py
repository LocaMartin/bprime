from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bprime",
    version="0.1.1",  # Increment version
    author="Loca Martin",
    author_email="locaboyff@gmail.com",
    description="A digital stopwatch with classic green display",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/locamartin/bprime",
    packages=find_packages(),
    package_data={
        'bprime': ['digi7/digital-7.ttf'],  # Fixed package name
    },
    include_package_data=True,  # Important for including data files
    install_requires=[
        'PyQt5>=5.15.4',
    ],
    entry_points={
        'console_scripts': [
            'bprime = bprime.prime.bprime:main',  # Corrected entry point
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)