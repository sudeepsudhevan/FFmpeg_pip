# Publishing Guide

This document explains how to release new versions of `ffmpeg-tools` to PyPI.

## Prerequisites

Ensure you have the build tools installed:

```bash
pip install build twine
```

## Steps to Release a New Version

### 1. Update Version
Open `setup.py` and increment the `version` number (e.g., change `0.1.2` to `0.1.3`).

```python
setup(
    name="ffmpeg_tools",
    version="0.1.3",  # <--- Update this
    ...
)
```

### 2. Clean Previous Builds (Optional)
To avoid confusion, remove the old `dist/` folder if it exists.

```powershell
Remove-Item -Recurse -Force dist
```

### 3. Build the Package
Run the following command to generate the distribution files:

```bash
python -m build
```
This will create a new `dist/` folder containing your `.whl` and `.tar.gz` files.

### 4. Upload to PyPI
Use `twine` to upload the new files. Since we configured `.pypirc`, you can use the config flag:

```bash
python -m twine upload --config-file .pypirc dist/*
```

## Troubleshooting

- **403 Forbidden**: This usually means the version number you are trying to upload already exists on PyPI. You **must** bump the version number in `setup.py` for every new upload.
- **Invalid Auth**: Check if your token in `.pypirc` has expired or is incorrect.
