#!/usr/bin/env python3

import json
import os
import subprocess
import sys
from argparse import Namespace
from pathlib import Path

from omakase_media_tools.file_log.logger import setup_ffmpeg_logger, ffmpeg_error

try:
    import ffmpeg
except ImportError:
    print("Error: ffmpeg package not found. Please install it separately.")
    print("For installation instructions, visit: https://https://ffmpeg.org")
    ffmpeg = None

ffmpeg_logger = setup_ffmpeg_logger("create__audio_waveforms")


def create_wav_from_aac(source_audio_file_path) -> str:
    """
    Convert an AAC audio file to a WAV file using ffmpeg
    :param source_audio_file_path:Should be a path to an AAC audio file
    :return: Path to BWAV file created
    """

    # If ffmpeg is none, import above failed skip generation
    if ffmpeg is None:
        print("Error: ffmpeg package not available. Skipping WAV conversion.")
        return source_audio_file_path
    try:
        output_wav_file_path = Path(source_audio_file_path).with_suffix('.wav').name
        stream = (
            ffmpeg
            .input(source_audio_file_path)
            .output(output_wav_file_path)
        )

        stdout, stderr = stream.run(capture_stdout=True, capture_stderr=True)
        ffmpeg_logger.info(f"FFmpeg output: {stdout.decode('utf-8')}")

        print("Audio waveform generated successfully")

    except ffmpeg.Error as e:
        error_message = e.stderr.decode('utf-8') if e.stderr else str(e)
        ffmpeg_error(ffmpeg_logger, error_message)
    except Exception as e:
        err_msg = str(e)
        if "ffmpeg" in err_msg.lower():
            ffmpeg_error(ffmpeg_logger, err_msg)
            return
        print(f"An unexpected error occurred: {str(e)}", file=sys.stderr)

    return output_wav_file_path


def generate_audio_waveform(source_audio_file_path, vtt_file_path='', samples_per_second=1):
    """
    Generate an audio waveform form using the BBC audiowaveform Open Source project that can be found here:
      https://github.com/bbc/audiowaveform

    Post-process the JSON file output from the audiowaveform tool into a VTT file with the presentation time
      of each 'subtitle' corresponding to the sample interval and the subtitle in the format -MIN,MAX values.

      Sample values are normalized before being written to the VTT file as (MIN / 32768) and (MAX / 32767). Where
        the sample value is a signed 16-bit integer.
    """
    # Ensure output directory exists
    if vtt_file_path:
        try:
            os.makedirs(vtt_file_path, exist_ok=True)
        except PermissionError:
            print(f"Error: OMT does not have permissions to create vtt file path {vtt_file_path}")
            print("Change folder permissions or target folder and try again!")
            return
        except Exception as e:    
            print(f"An unexpected error occurred creating vtt file path {vtt_file_path} :: {str(e)}")
            return

    if source_audio_file_path.endswith('.aac') | source_audio_file_path.endswith('.mp4'):
        wav_audio_file_path = create_wav_from_aac(source_audio_file_path)
    else:
        wav_audio_file_path = source_audio_file_path

    # The audiowaveform tool outputs a JSON formatted file.
    temp_json_file_path = Path(source_audio_file_path).with_suffix(".json")

    #  audiowaveform \
    #       -i source_audio_file.wav \
    #       -o ./vtt_file_path/out.json \
    #       --pixels-per-second samples_per_second \
    #       --bits 16
    try:
        subprocess.run(
            [
                "audiowaveform",
                "-i", wav_audio_file_path,
                "-o", str(temp_json_file_path),
                "--pixels-per-second", str(samples_per_second),
                "--bits", "16"
            ],
            check=True,
            capture_output=True,
            text=True
        )
    except Exception as e:
        print(f"audio wave form error: {e}")
        print(
            "Make sure the audiowaveform package is installed on your system and properly configured: https://github.com/bbc/audiowaveform")
        return

    # Convert the audiowaveform JSON output to an OMP VTT file
    convert_json_to_vtt(
        temp_json_file_path,
        Path(vtt_file_path) / (Path(source_audio_file_path).stem + ".vtt"),
        samples_per_second
    )

    # Clean up temporary JSON file
    try:
        os.remove(temp_json_file_path)
    except PermissionError:
        print(f"Error: OMT does not have permissions to remove temp json file directory {temp_json_file_path}")
        print("Folder will remain in place and must be removed manually.")
    except Exception as e:    
        print(f"An unexpected error occurred removing temp json file directory {temp_json_file_path} :: {str(e)}")
        print("Folder will remain in place and must be removed manually.")

    # Remove the temporary wav file if needed
    try:
        if source_audio_file_path.endswith('.aac'):
            os.remove(wav_audio_file_path)
    except PermissionError:
        print(f"Error: OMT does not have permissions to remove temp json file directory {wav_audio_file_path}")
        print("Folder will remain in place and must be removed manually.")
    except Exception as e:    
        print(f"An unexpected error occurred removing temp json file directory {wav_audio_file_path} :: {str(e)}")
        print("Folder will remain in place and must be removed manually.")


def format_timestamp(seconds):
    # Create a VTT compliant timestamp
    # Format time in HH:MM:SS.mmm
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}.{milliseconds:03}"


def convert_json_to_vtt(input_file, output_file, samples_per_second=1):
    # Load the JSON data from the input file
    with open(input_file, 'r') as file:
        json_data = json.load(file)

    # Calculate the time per sample period
    time_per_sample = 1 / samples_per_second

    # Open the output file for writing
    with open(output_file, 'w') as vtt_file:
        vtt_file.write("WEBVTT\n\n")

        # Loop through the data array in steps of 2 (MIN, MAX pairs)
        for i in range(0, len(json_data["data"]), 2):
            # Calculate the start and end times for this subtitle
            start_time = i // 2 * time_per_sample
            # Calculate an end_time that doesn't overlap with the next sample interval start_time.
            end_time = (i // 2 + 1) * time_per_sample - 0.000999

            # Format the times as VTT timestamps
            start_time_str = format_timestamp(start_time)
            end_time_str = format_timestamp(end_time)

            # Normalize the samples to a fractional value
            min_sample = float(json_data["data"][i]) / 32768
            max_sample = float(json_data["data"][i + 1]) / 32767

            # Write the VTT entry with sample values formatted to four decimal places
            vtt_file.write(f"{start_time_str} --> {end_time_str}\n")
            vtt_file.write(f"{min_sample:.4f}, {max_sample:.4f}\n\n")


def setup_waveforms_args(subparsers):
    waveforms_parser = subparsers.add_parser('waveforms', aliases=['w'], help='create audio waveforms')

    waveforms_parser.add_argument("-v", "--verbose", help="enable verbose output", action="store_true")
    waveforms_parser.add_argument("-i", "--input", help="input media file or directory", required=True)
    waveforms_parser.add_argument("-o", "--output", help="output directory", required=True)
    waveforms_parser.set_defaults(func=create_waveforms)


def create_waveforms(args: Namespace):
    """
    omt.py waveforms -i <input file or directory> -o <output>
    """
    if args.verbose:
        print(f"creating audio waveforms: input \'{args.input}\' | output \'{args.output}\'")

    if os.path.isfile(args.input):
        generate_audio_waveform(args.input, args.output, 1)
    elif os.path.isdir(args.input):
        for entry in os.scandir(args.input):
            if entry.name.endswith('.wav') | entry.name.endswith('.aac') | entry.name.endswith('.mp4'):
                generate_audio_waveform(entry.path, args.output, 1)
    else:
        print(f"Input {args.input} is not a valid file or directory.")
        return
