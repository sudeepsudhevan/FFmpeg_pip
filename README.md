# FFmpeg Tools

A Python package for simplified FFmpeg command generation, video downloading, and file management.

## Installation

```bash
pip install ffmpeg-tools
```

## Usage

### 1. Generating & Running FFmpeg Commands

```python
from ffmpeg_tools import build_command, run_command

# 1. Build the command
cmd = build_command("compress_high_quality", input="video.mp4", output="compressed.mp4")

# 2. Run the command (returns True if successful)
success = run_command(cmd)

# Optional: Dry run to just print the command
run_command(cmd, dry_run=True)
```

### 2. Downloading Videos

```python
from pathlib import Path
from ffmpeg_tools import download_video

# Download a video from YouTube
download_video(
    url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    output_folder=Path("downloads"),
    clear_folder=False
)
```

### 3. Cleaning Filenames

```python
from pathlib import Path
from ffmpeg_tools import clean_filename

file_path = Path("downloads/My Video (2024).mp4")
new_path = clean_filename(file_path)
print(new_path)
# Output: downloads/My_Video_2024.mp4
```

## License

MIT
