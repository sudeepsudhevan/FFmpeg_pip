"""
ffmpeg_tools
~~~~~~~~~~~~

A simple Python package for FFmpeg command generation, video downloading, and file management.
"""

from .commands import build_command, get_all_commands, run_command
from .media import clean_filename, has_video_stream, remove_video_files
from .downloader import download_video

__version__ = "0.1.0"
