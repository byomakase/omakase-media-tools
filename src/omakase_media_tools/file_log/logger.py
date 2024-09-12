#!/usr/bin/env python3

import logging
from pathlib import Path
import tempfile

def setup_ffmpeg_logger(name, level=logging.INFO):
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    log_dir = Path(tempfile.gettempdir()) / 'omakase_logs'
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        print(f"Permission denied when creating log directory: {log_dir}")
        # Fallback to user's home directory
        log_dir = Path.home() / '.omakase_logs'
        log_dir.mkdir(parents=True, exist_ok=True)

    ffmpeg_logger = logging.getLogger(f"{name}.ffmpeg")
    ffmpeg_logger.setLevel(level)

    # Create log file in the determined directory
    log_file_path = log_dir / f"{name}_ffmpeg.log"
    try:
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setFormatter(formatter)
        ffmpeg_logger.addHandler(file_handler)
    except PermissionError:
        print(f"Permission denied when creating log file: {log_file_path}")
        # Fallback to console logging
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        ffmpeg_logger.addHandler(console_handler)
        
    ffmpeg_logger.propagate = False

    return ffmpeg_logger

def ffmpeg_error(ffmpeg_logger: logging.Logger, message):
        out_message = f"FFmpeg error: {message}\nFFmpeg must be installed separately\nFor installation instructions, visit: https://ffmpeg.org"
        ffmpeg_logger.error(out_message)
        print(out_message)