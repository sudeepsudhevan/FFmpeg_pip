"""
ffmpeg_tools.downloader
~~~~~~~~~~~~~~~~~~~~~~~

Wrapper for downloading videos using yt-dlp.
"""

import subprocess
import logging
from pathlib import Path
from .media import remove_video_files

# Setup logger
logger = logging.getLogger(__name__)


def download_video(url: str, output_folder: Path, clear_folder: bool = False) -> None:
    """
    Downloads a YouTube video to the specified folder using yt-dlp.
    
    Args:
        url (str): The YouTube URL.
        output_folder (Path): Destination directory.
        clear_folder (bool): If True, deletes existing video files in the folder before download.
    """
    output_folder.mkdir(parents=True, exist_ok=True)

    if clear_folder:
        removed_count = remove_video_files(output_folder)
        logger.info(f"Cleared {removed_count} video files from {output_folder}")

    # Template: Folder/Title.ext
    output_template = str(output_folder / "%(title)s.%(ext)s")

    command = [
        "yt-dlp",
        "-f", "bestvideo+bestaudio/best",
        "-o", output_template,
        url,
    ]

    logger.info(f"Starting download: {url}")
    try:
        subprocess.run(command, check=True)
        logger.info("Download completed successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Download failed: {e}")
        raise
