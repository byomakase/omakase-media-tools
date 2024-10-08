#!/usr/bin/env python3

import contextlib
import io
import json
import os
from argparse import Namespace
from pathlib import Path

try:
    from ffmpeg_bitrate_stats.bitrate_stats import BitrateStats
except ImportError:
    print("Error: ffmpeg_bitrate_stats package not found. Please install it separately.")
    print("For installation instructions, visit: https://github.com/slhck/ffmpeg-bitrate-stats")
    BitrateStats = None


def create_vtt_timestamps(sample_index, samples_per_sec):
    """
    Generate VTT starting and ending timestamps for a given sample interval in HH:MM:SS.000 format
    :param sample_index:
    :param samples_per_sec:
    :return: start_time, end_time

    CAUTION: This currently does not genrate a valid end_time if 60 % sample_interval_secs != 0.
    """

    hours = (sample_index * samples_per_sec) // 3600
    minutes = ((sample_index * samples_per_sec) % 3600) // 60
    seconds = ((sample_index * samples_per_sec) % 3600) % 60
    milliseconds = (sample_index * samples_per_sec) % 1 * 1000
    start_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"

    seconds += (samples_per_sec - 1)
    end_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}.999"

    return start_time, end_time


def create_bitrate_vtt_file(bitrate_json, output_vtt_path, sample_interval_secs=2):
    """
    Generate an OMP VTT 1.0 file for the bitrate_json provided
    :param bitrate_json: The video bitrate JSON generated by the ffmpeg_bitrate_stats Python package.
    :param output_vtt_path: The VTT file to write the output to.
    :param sample_interval_secs: The sample interval used to calculate the average video bitrate.
    :return:
    """
    with open(output_vtt_path, 'w') as f:
        # Write header lines
        f.write("WEBVTT\n\n")
        f.write("NOTE\nOmakase Player Web VTT\nV1.0\n\n")

        # Iterate over bitrate_per_chunk array
        for i, bitrate in enumerate(bitrate_json['bitrate_per_chunk']):
            start_time, end_time = create_vtt_timestamps(i, sample_interval_secs)

            f.write(f"{start_time} --> {end_time}\n")
            f.write(f"{bitrate}:MEASUREMENT=avg:COMMENT={sample_interval_secs}-sec interval\n\n")


def generate_video_bitrate_vtt(source_video_file_path, output_vtt_dir, sample_interval_secs=2):
    """
    Generates a video bitrate JSON for a given video file.
    :param source_video_file_path: Path to the video file to be processed.
    :param output_vtt_dir: The directory to write the VTT file to.
    :param sample_interval_secs: Interval in seconds over which to calculate an average video bitrate.
    :return: a video bitrate JSON.

    The video bitrate JSON is created by the ffmpeg_bitrate_stats Python package which can be obtained here:
        https://github.com/slhck/ffmpeg-bitrate-stats

    An example of the bitrate JSON generated is shown below, with a 'chunksize' aka sample_interval_secs of 10.
    Each entry in the bitrate_per_chunk[] array is an average video bitrate for the sample period.
    {
        "input_file": "./source-media/tearsofsteel_4k_1m0s.mov",
        "stream_type": "video",
        "avg_fps": 24.0,
        "num_frames": 1442,
        "avg_bitrate": 55447.77,
        "avg_bitrate_over_chunks": 74068.697,
        "max_bitrate": 185830.129,
        "min_bitrate": 8020.057,
        "max_bitrate_factor": 3.351,
        "bitrate_per_chunk": [
            8020.057,
            86935.95,
            65789.099,
            51523.297,
            51626.147,
            68756.199,
            185830.129
        ],
        "aggregation": "time",
        "chunk_size": 10,
        "duration": 60.084
    }
    """
    # BitrateStats will be none if the import failed above, return before trying
    if BitrateStats is None:
        print("Error: ffmpeg_bitrate_stats package not available. Skipping video bitrate VTT generation.")
        return

    # Use the BitrateStats class from the ffmpeg_bitrate_stats package
    br = BitrateStats(
        source_video_file_path,
        "video",
        "time",
        sample_interval_secs,
        "",
        "",
        False,
    )

    br.calculate_statistics()

    # The BitrateStats class prints the resulting json string to stdout. Capture to string here.
    output_bitrate = io.StringIO(newline='\n')
    with contextlib.redirect_stdout(output_bitrate):
        br.print_statistics("json")

    # Ensure output directory exists
    if output_vtt_dir:
        try:
            os.makedirs(output_vtt_dir, exist_ok=True)
        except PermissionError:
            print(f"Error: OMT does not have permissions to create vtt output directory {output_vtt_dir}")
            print("Change folder permissions or target folder and try again!")
            return
        except Exception as e:    
            print(f"An unexpected error occurred creating vtt output directory {output_vtt_dir} :: {str(e)}")
            return

    # Create output VTT filename path from source video filename
    output_vtt_path = str(Path(output_vtt_dir) / f'{Path(source_video_file_path).stem}_{sample_interval_secs}-SEC.vtt')

    # Generate the OMP VTT 1.0 format file from the generated JSON.
    create_bitrate_vtt_file(json.loads(output_bitrate.getvalue()), output_vtt_path, sample_interval_secs)


def setup_video_bitrate_args(subparsers):
    video_bitrate_parser = subparsers.add_parser('video-bitrate', aliases=['b'], help='create video bitrate track')

    video_bitrate_parser.add_argument("-v", "--verbose", help="enable verbose output", action="store_true")
    video_bitrate_parser.add_argument("-i", "--input", help="input video file", required=True)
    video_bitrate_parser.add_argument("-o", "--output", help="output directory", required=True)
    video_bitrate_parser.add_argument(
        "-s", "--seconds-interval",
        help="seconds between bitrate samples",
        default=2,
        choices=[1, 2, 3, 4, 5, 10, 12, 15],
        type=int)
    video_bitrate_parser.set_defaults(func=create_video_bitrate)


def create_video_bitrate(args: Namespace):
    """
    omt.py --video-bitrate -i <input> -o <output> -s <seconds_interval>
    """
    if os.path.isdir(args.input):
        print("input directory not supported for video bitrate track creation.")
        return
    elif Path(args.input).exists() is False:
        print(f"input file \'{args.input}\' does not exist.")
        return

    if args.verbose:
        print(
            f"creating video bitrate metrics: input \'{args.input}\' | output \'{args.output}\' | seconds per sample: {args.seconds_interval}")

    generate_video_bitrate_vtt(args.input, args.output, args.seconds_interval)
