from setuptools import setup, find_packages
from flaskavel.metadata import *

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
        "bcrypt>=4.2.0",
        "greenlet>=3.1.0",
        "pyclean>=3.0.0",
        "schedule>=1.2.2",
        "SQLAlchemy>=2.0.35",
        "typing_extensions>=4.12.2",
        "python-dotenv>=1.0.1",
        "cryptography>=43.0.3",
        "Flask>=3.0.3",
        "Flask-Cors>=5.0.0"
    ],
    entry_points={
        "console_scripts": [
            "flaskavel=flaskavel.init:main"
        ]
    }
)
