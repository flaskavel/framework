from setuptools import setup, find_packages
from orionis.framework import *

setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url=FRAMEWORK,
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=PYTHON_REQUIRES,
    install_requires=[
        "apscheduler>=3.11.0",
        "python-dotenv>=1.0.1"
    ],
    entry_points={
        "console_scripts": [
            "orionis=orionis.cli_manager:main"
        ]
    },
    test_suite="tests"
)
