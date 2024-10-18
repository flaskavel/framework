from setuptools import setup, find_packages

setup(
    name="flaskavel",
    version="0.0.5",
    author="Raul Mauricio Uñate Castro",
    author_email="raulmauriciounate@gmail.com",
    description="Like in Laravel but with Python",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/flaskavel/framework",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
    install_requires=[
        "bcrypt==4.2.0",
        "greenlet==3.1.0",
        "pyclean==3.0.0",
        "schedule==1.2.2",
        "SQLAlchemy==2.0.35",
        "typing_extensions==4.12.2"
    ],
    entry_points={
        "console_scripts": [
            "flaskavel=flaskavel.init:main"
        ]
    }
)
