"""
ffmpeg_tools.commands
~~~~~~~~~~~~~~~~~~~~~

High-quality FFmpeg command templates and building utilities.
"""

import json
import logging
import os
from copy import deepcopy


from pathlib import Path

# Setup logger
logger = logging.getLogger(__name__)

# Default path for external commands JSON
DEFAULT_DB_PATH = Path(__file__).parent / "commands.json"

# Hardcoded Baseline Commands
FFMPEG_COMMANDS = {
    # =========================
    # 🎯 BASELINE (GPU ACCELERATED)
    # =========================
    "base_gpu_quality": {
        "command": [
            "ffmpeg", "-y",
            "-hwaccel", "cuda",
            "-i", "{input}",
            "-c:v", "h264_nvenc",
            "-preset", "p6",
            "-rc", "vbr",
            "-cq", "19",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k",
            "{output}"
        ],
        "description": "GPU accelerated H.264 encoding (High Quality)"
    },

    "trim_gpu_reencode": {
        "command": [
            "ffmpeg", "-y",
            "-hwaccel", "cuda",
            "-ss", "{start}", "-to", "{end}",
            "-i", "{input}",
            "-c:v", "h264_nvenc",
            "-preset", "p4",
            "-cq", "19",
            "-c:a", "aac",
            "{output}"
        ],
        "description": "Fast GPU-based frame-accurate trimming"
    },

    "compress_gpu_h265": {
        "command": [
            "ffmpeg", "-y",
            "-hwaccel", "cuda",
            "-i", "{input}",
            "-c:v", "hevc_nvenc",
            "-preset", "p6",
            "-rc", "vbr",
            "-cq", "24",
            "-c:a", "aac",
            "{output}"
        ],
        "description": "Ultra-fast H.265 compression via GPU"
    },

    "resize_gpu": {
        "command": [
            "ffmpeg", "-y",
            "-hwaccel", "cuda",
            "-hwaccel_output_format", "cuda",
            "-i", "{input}",
            "-vf", "scale_cuda={width}:{height}",
            "-c:v", "h264_nvenc",
            "-preset", "p4",
            "-c:a", "aac",
            "{output}"
        ],
        "description": "Resize video entirely on GPU (no CPU bottleneck)"
    },

    # =========================
    # 🎯 BASELINE (CPU BEST QUALITY)
    # =========================
    "base_best_quality": {
        "command": [
            "ffmpeg", "-y",
            "-i", "{input}",
            "-map", "0:v:0",
            "-map", "0:a:0?",
            "-c:v", "libx264",
            "-preset", "slow",
            "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-profile:v", "high",
            "-level", "4.1",
            "-c:a", "aac",
            "-b:a", "192k",
            "-movflags", "+faststart",
            "{output}"
        ],
        "description": "Visually lossless video + high quality AAC audio"
    },

    "trim_reencode": {
        "command": [
            "ffmpeg", "-y",
            "-ss", "{start}",
            "-to", "{end}",
            "-i", "{input}",
            "-c:v", "libx264",
            "-preset", "slow",
            "-crf", "18",
            "-c:a", "aac",
            "-b:a", "192k",
            "-movflags", "+faststart",
            "{output}"
        ],
        "description": "Frame-accurate trimming with re-encoding"
    },

    "trim_copy": {
        "command": [
            "ffmpeg", "-y",
            "-ss", "{start}",
            "-to", "{end}",
            "-i", "{input}",
            "-c", "copy",
            "{output}"
        ],
        "description": "Fast trim without quality loss (keyframe based)"
    },

    "split_segments": {
        "command": [
            "ffmpeg", "-y",
            "-i", "{input}",
            "-map", "0",
            "-c", "copy",
            "-f", "segment",
            "-segment_time", "{duration}",
            "-reset_timestamps", "1",
            "{output_pattern}"
        ],
        "description": "Split video into equal-length segments"
    },

    "compress_high_quality": {
        "command": [
            "ffmpeg", "-y",
            "-i", "{input}",
            "-c:v", "libx264",
            "-preset", "slow",
            "-crf", "23",
            "-c:a", "aac",
            "-b:a", "160k",
            "-movflags", "+faststart",
            "{output}"
        ],
        "description": "Balanced compression (YouTube-grade quality)"
    },

    "compress_ultra": {
        "command": [
            "ffmpeg", "-y",
            "-i", "{input}",
            "-c:v", "libx265",
            "-preset", "slow",
            "-crf", "28",
            "-c:a", "aac",
            "-b:a", "128k",
            "{output}"
        ],
        "description": "Maximum compression using H.265"
    },

    "extract_audio_wav": {
        "command": [
            "ffmpeg", "-y",
            "-i", "{input}",
            "-vn",
            "-c:a", "pcm_s16le",
            "{output}"
        ],
        "description": "Extract lossless WAV audio"
    },

    "extract_audio_aac": {
        "command": [
            "ffmpeg", "-y",
            "-i", "{input}",
            "-vn",
            "-c:a", "aac",
            "-b:a", "192k",
            "{output}"
        ],
        "description": "Extract high-quality AAC audio"
    },

    "extract_video_only": {
        "command": [
            "ffmpeg", "-y",
            "-i", "{input}",
            "-an",
            "-c:v", "libx264",
            "-preset", "slow",
            "-crf", "18",
            "{output}"
        ],
        "description": "Extract video stream only"
    },

    "resize_video": {
        "command": [
            "ffmpeg", "-y",
            "-i", "{input}",
            "-vf", "scale={width}:{height}:flags=lanczos",
            "-c:v", "libx264",
            "-preset", "slow",
            "-crf", "18",
            "-c:a", "aac",
            "-b:a", "192k",
            "{output}"
        ],
        "description": "Resize video using high-quality Lanczos scaling"
    },

    "remux_copy": {
        "command": [
            "ffmpeg", "-y",
            "-i", "{input}",
            "-c", "copy",
            "{output}"
        ],
        "description": "Change container format without re-encoding"
    }
}


def get_all_commands(db_path: str = None) -> dict:
    """
    Returns the complete dictionary of available FFmpeg commands.
    Merges hardcoded commands with an optional external JSON file.
    """
    all_cmds = deepcopy(FFMPEG_COMMANDS)
    
    target_path = db_path if db_path else DEFAULT_DB_PATH
    
    if os.path.exists(target_path):
        try:
            with open(target_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    external_cmds = json.loads(content)
                    all_cmds.update(external_cmds)
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Failed to load external commands from {target_path}: {e}")
            
    return all_cmds


def add_command(name: str, command: list[str], description: str, db_path: str = None) -> None:
    """
    Adds a new command to the external JSON file.
    
    Args:
        name (str): Unique name for the command profile.
        command (list[str]): The FFmpeg command list.
        description (str): Description of what the command does.
        db_path (str, optional): Path to external JSON command DB.
    """
    target_path = db_path if db_path else DEFAULT_DB_PATH
    
    # Load existing external commands
    external_cmds = {}
    if os.path.exists(target_path):
        try:
            with open(target_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    external_cmds = json.loads(content)
        except (json.JSONDecodeError, IOError):
            logger.warning(f"Could not read existing commands from {target_path}, starting fresh.")
    
    # Add/Update the command
    external_cmds[name] = {
        "command": command,
        "description": description
    }
    
    # Save back to JSON
    try:
        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(external_cmds, f, indent=4)
        logger.info(f"Command '{name}' added successfully to {target_path}")
    except IOError as e:
        logger.error(f"Failed to save command '{name}' to {target_path}: {e}")
        raise


def build_command(profile: str, db_path: str = None, **kwargs) -> list[str]:
    """
    Builds the FFmpeg command list for a given profile.
    
    Args:
        profile (str): The key/name of the command profile.
        db_path (str, optional): Path to external JSON command DB.
        **kwargs: Arguments to format the command template (e.g., input, output, start, end).
        
    Returns:
        list[str]: The formatted command list ready for subprocess.
        
    Raises:
        KeyError: If profile is not found or required arguments are missing.
    """
    commands = get_all_commands(db_path)
    
    if profile not in commands:
        raise KeyError(f"Profile '{profile}' not found.")

    template = commands[profile]["command"]
    
    try:
        # Format each argument in the command list
        return [arg.format(**kwargs) for arg in template]
    except KeyError as e:
        missing_key = e.args[0]
        raise KeyError(f"Missing required parameter '{missing_key}' for profile '{profile}'.")


def run_command(command: list[str], dry_run: bool = False) -> bool:
    """
    Executes the given FFmpeg command list using subprocess.
    
    Args:
        command (list[str]): The command list (e.g., from build_command).
        dry_run (bool): If True, prints the command without executing.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    if dry_run:
        print(f"Dry run: {' '.join(command)}")
        return True

    try:
        import subprocess
        logger.info(f"Running command: {' '.join(command)}")
        subprocess.run(command, check=True)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"FFmpeg execution failed: {e}")
        return False
    except FileNotFoundError:
        logger.error("FFmpeg not found. Please ensure ffmpeg is in your system PATH.")
        return False

