"""
ffmpeg_tools.media
~~~~~~~~~~~~~~~~~~

Utilities for file handling, cleaning, and validation of media files.
"""

import re
import mimetypes
import logging
import subprocess
from pathlib import Path
from typing import Optional, List

# Setup logger
logger = logging.getLogger(__name__)


def has_video_stream(file_path: Path) -> bool:
    """
    Checks if a file contains a video stream using ffprobe.
    """
    if not file_path.exists():
        return False

    cmd = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=codec_type",
        "-of", "csv=p=0",
        str(file_path)
    ]
    
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.returncode == 0 and result.stdout.strip() == "video"
    except Exception as e:
        logger.error(f"Error checking video stream for '{file_path}': {e}")
        return False


def clean_filename(file_path: Path) -> Path:
    """
    Renames a file to be 'clean' (no spaces, special chars).
    Returns the new Path object.
    
    Example: "My Video (2024).mp4" -> "My_Video_2024.mp4"
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    original_stem = file_path.stem
    # Remove wrappers like [] () and replace spaces with underscores
    clean_stem = re.sub(r"[_\[\]\(\)]", "", original_stem).replace(" ", "_")
    
    # Ensure it's not empty, fallback to 'video' if everything was stripped
    if not clean_stem:
        clean_stem = "video"
        
    new_name = f"{clean_stem}{file_path.suffix}"
    new_path = file_path.parent / new_name
    
    if new_path != file_path:
        try:
            file_path.rename(new_path)
            logger.info(f"Renamed '{file_path.name}' -> '{new_name}'")
        except OSError as e:
            logger.error(f"Failed to rename '{file_path}': {e}")
            raise
            
    return new_path


def remove_video_files(folder: Path) -> int:
    """
    Removes all video files from the specified folder.
    Returns the count of removed files.
    """
    if not folder.exists():
        return 0
        
    count = 0
    for file in folder.iterdir():
        if file.is_file():
            mime, _ = mimetypes.guess_type(file)
            # Basic mime check, can be expanded or use has_video_stream for strictness
            if mime and mime.startswith("video"):
                try:
                    file.unlink()
                    count += 1
                    logger.debug(f"Deleted: {file.name}")
                except OSError as e:
                    logger.error(f"Failed to delete '{file}': {e}")
    return count
