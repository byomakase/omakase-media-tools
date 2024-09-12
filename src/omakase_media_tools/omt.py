# !/usr/bin/env python3


import argparse

from omakase_media_tools.audio_metrics import setup_audio_metrics_args
from omakase_media_tools.player_json import setup_player_json_args
from omakase_media_tools.thumbnails import setup_thumbnails_args
from omakase_media_tools.video_bitrate import setup_video_bitrate_args
from omakase_media_tools.waveforms import setup_waveforms_args


def main():
    parser = argparse.ArgumentParser(description="Create OMP metadata tracks and player json.")

    subparsers = parser.add_subparsers(dest="command",
                                       title='commands',
                                       description='valid omt commands',
                                       help='omt commands help')

    setup_player_json_args(subparsers)
    setup_audio_metrics_args(subparsers)
    setup_waveforms_args(subparsers)
    setup_video_bitrate_args(subparsers)
    setup_thumbnails_args(subparsers)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
    else:
        args.func(args)

    return


if __name__ == "__main__":
    main()
