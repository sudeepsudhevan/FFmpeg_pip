from setuptools import setup, find_packages

setup(
    name="ffmpeg_tools",
    version="0.1.1",
    description="A Python package for high-quality FFmpeg command generation and video utilities.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Sudeep Sudhevan",
    author_email="sudeepsudhevan66@gmail.com",
    url="https://github.com/sudeepsudhevan/FFmpeg_pip",
    packages=find_packages(),
    install_requires=[
        "yt-dlp",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
