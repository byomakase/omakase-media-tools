# Omakase Media Tools Utility

This PIP package contains the `omt` utility and sample media reference for use with
the [Omakase Player](https://player.byomakase.org/)
and [Omakase Reference Player](https://github.com/byomakase/omakase-reference-player) open source projects.

The sample media is provided to demonstrate the capabilities of the Omakase Player framework and to bootstrap small POC
projects. The sample media reference and `omt` utility are provided as-is and are not intended for use in production
environments.

The Python `omt.py` utility and documentation can be used to create your own sample media, temporal metadata tracks and OMP player
JSON for use with the Omakase Player framework and the Omakase Reference Player.

The utility can create an OMP player json file from a template, source media and HLS media:

- **OMP Player JSON** using the `omt player-json` CLI command

The utility can generate the following types of metadata tracks:

- **Audio Metric Analysis Tracks** using the `omt audio-metrics` CLI command
- **Audio Waveform Analysis Tracks** using the `omt waveforms` CLI command
- **Video Bitrate Analysis Tracks** using the `omt video-bitrate` CLI command
- **Video Thumbnail Tracks** using the `omt thumbnails` CLI command

The reference implementation of the Omakase player can be found in GitHub
at [omakase-reference-player](https://github.com/byomakase/omakase-reference-player).

Contents:

- Requirements
- Installation
- Usage
    - Usage `omt player-json`
    - Usage `omt thumbnails`
    - Usage `omt video-bitrate`
    - Usage `omt audio-metrics`
    - Usage `omt waveforms`
- External Links
- License

## Requirements

------

### Python

- Python 3.8 or higher

### ffmpeg

- Download a static build from the [ffmpeg website](http://ffmpeg.org/download.html) and install using the instructions
  for your platform.
- Ensure that the `ffmpeg` executable is in your path.

### audiowaveform

`audiowaveform` is a C++ program that takes an audio file and generates raw waveform data from it.

This data is then used to generate an OMP v1.0 VTT file containing the waveform metadata needed by the Omakase Player.

- download and install from GitHub here: [audiowaveform](https://github.com/bbc/audiowaveform)

### ffmpeg-bitrate-stats

The `ffmpeg-bitrate-stats` Python package is used to generate raw video bitrate metrics, when are then processed to
create an OMP v1.0 VTT file for use with Omakase Player.

- Install the `ffmpeg-bitrate-stats` Python package from the following GitHub
  repository: [ffmpeg-bitrate-stats](https://github.com/slhck/ffmpeg-bitrate-stats)

### MediaInfo

The `mediainfo` CLI utility is used to extract media file information, that is then used to populate metadata in the OMP
player json file.

IMPORTANT: **The CLI version** of `MediaInfo` must be installed on your system and available in your path. This
installation is in addition to the GUI version of `MediaInfo` that may already be installed on your system.

- Download and install the **CLI VERSION** from [MediaInfo website](https://mediaarea.net/en/MediaInfo/Download) for
  your platform.

## Installation

------

- Install the PIP package `omp-media-tools` from PyPi.

## Usage

------

The Python utility `omt.py` is a command line utility that can generate Omakase Player temporal metadata
tracks and OMP player json files from source media.

The utility can create an OMP player json file from a template, source media and HLS media:

- **OMP Player JSON** using the `omt player-json` CLI command

The utility can generate the following types of metadata tracks:

- **Audio Metric Analysis Tracks** using the `omt audio-metrics` CLI command
- **Audio Waveform Analysis Tracks** using the `omt waveforms` CLI command
- **Video Bitrate Analysis Tracks** using the `omt video-bitrate` CLI command
- **Video Thumbnail Tracks** using the `omt thumbnails` CLI command

## Usage omt player-json

To assist with creation of an OMP player json file, the `omt player-json` utility command can be used to generate the
OMP player json file from a template.

The template file contains the minimal essential information required to generate the OMP player json. With a default
directory structure to hold the source media, HLS media and metadata tracks, the `omt player-json` utility command can
search the directories for the required file references, create required technical metadata and generate the OMP player
json.

### Default Directory Structure

The `omt player-json` utility command expects the default directory structure as shown below. The OMP player json
does not require this structure, but using this default makes a sparse template json possible.

The utility command should be run from the `working_directory` directory where the `template.json` file is located. This
is passed as follows:

- `omt player-json --template template.json`

The `media_root` directory is the root directory for all HLS media, analysis metadata tracks, thumbnails and waveforms.
This directory will be uploaded to the CDN or webserver.

The `analysis` directory contains the audio and video analysis metadata tracks. This includes metadata tracks created
with the `omt` utility as well as those created manually or through some other process.

The metadata tracks created with the following `omt` utility commands should be placed in the `analysis` directory:

- `omt audio-metrics` for the EBU R128 and RMS Levels audio metric metadata tracks
- `omt video-bitrate` for the video bitrate metadata track

The `thumbnails` directory contains the video thumbnail metadata track and images created with the `omt thumbnails`
utility command.

The `waveforms` directory contains the audio waveform metadata track created with the `omt waveforms` utility command.

The `hls` directory contains a directory for each HLS ABR rendition to be included. During creation of the OMP player
json, the `hls` directories are searched for media files to be referenced.

The `sources` directory contains the source media files to be used to generate the HLS ABR renditions. These files are
referenced to create audio and video metadata files and as a source of technical metadata (MediaInfo) to be presented
within the player.

```text
working_directory/
    ├── root_dir/
    │   └── player.json
    │   └── analysis/
    │   └── thumbnails/
    │   └── waveforms/
    │   └── hls/
    │       └── hls_abr_1/
    │       └── hls_abr_2/
    ├── sources/
    └── template.json
  ```

### Template Structure and Example

An example `template.json` file is shown below. The `template.json` file contains the minimal essential information
needed to create an OMP player json.

The `output` section contains several key fields used by the `omt player-json` utility command to generate the OMP
player json and navigate the directory structure.

The `root_dir` field specifies the name of the root directory (see above). The `sources_dir` field specifies the name
where the `mezzanine` files are located (see above).

The `root_url` field specifies the URL root that prepended to all file references in the OMP player json. For example,
it the `root_url` is `https://localhost:8080/`, the url reference to the HLS m3u8 manifest `tears-of-steel.m3u8` for the
`tears-of-steel_sdr_1080p24_BITC` rendition would be:

- `https://localhost:8080/hls/tears-of-steel_sdr_1080p24_BITC/tears-of-steel.m3u8`.

The `mezzanine` section contains the names of the source media files and assigned an ID to them. The `omt player-json`
utility command will search the `sources` directory for these files. Video files are assigned an ID starting with `V`,
audio files are assigned an ID starting with `A` and text files are assigned an ID starting with `T`.

The `hls` section contains the directories holding the HLS ABR renditions to be included in the player. Each rendition
is assigned an ID and a display name for presentation in the Omakase Player. The `omt player-json` utility command will
search the `hls` directory for these directories.

The `tracks` section contains the video, audio and text tracks to be presented in OMP player. Each track is mapped to
the source mezzanine file via the `source_id` field and the media track in the HLS ABR m3u8 manifest via the
`program_name`
field. The`display_text` field is used to present the track name in OMP player.

```json
{
    "sources": {
        "mezzanine": [
            {
                "id": "V1",
                "src": "tearsofsteel_4k.mov"
            },
            {
                "id": "A1",
                "src": "Surround-TOS_DVDSURROUND-Dolby%205.1.ac3"
            },
            {
                "id": "T1",
                "src": "TOS-en.srt"
            }
        ],
        "hls": [
            {
                "id": "HLS-1080",
                "display_name": "Confidence QC 1080p",
                "src": "tears-of-steel_sdr_1080p24_BITC"
            },
            {
                "id": "HLS-720",
                "display_name": "Proxy 720p",
                "src": "tears-of-steel_sdr_720p24_BITC"
            }
        ],
        "tracks": {
            "video": [
                {
                    "source_id": "V1"
                }
            ],
            "audio": [
                {
                    "source_id": "V1",
                    "display_text": "English 2.0",
                    "program_name": "EN_20"
                },
                {
                    "source_id": "A1",
                    "display_text": "English 5.1",
                    "program_name": "EN_51"
                }
            ],
            "text": [
                {
                    "source_id": "T1",
                    "display_text": "English Subtitles",
                    "program_name": "English Subtitles"
                }
            ]
        },
        "metadata": [
            {
                "display_name": "OMDb Title Metadata",
                "src": "omdb.json"
            }
        ]
    },
    "output": {
        "root_dir": "tears-of-steel",
        "sources_dir": "sources",
        "root_url": "https://localhost:8080/"
    }
}
```

## Usage omt thumbnails

A thumbnail timeline metadata track and series of thumbnail images, can be generated with this command.

An input video file must be specified and the VTT and image files generated are written to the output directory
specified.

The frequency of the thumbnails is controlled by the `--seconds-interval` CLI option.

```text
usage: omt.py thumbnails [-h] [-v] -i INPUT -o OUTPUT
                         [-s {1,2,3,4,5,10,12,15}]

options:
  -h, --help            show this help message and exit
  -v, --verbose         enable verbose output
  -i INPUT, --input INPUT
                        input video file
  -o OUTPUT, --output OUTPUT
                        output directory
  -s {1,2,3,4,5,10,12,15}, --seconds-interval {1,2,3,4,5,10,12,15}
                        seconds between video thumbnails
```

### Example - Thumbnail Timeline Metadata Track

```text
WEBVTT

00:00:00.000 --> 00:00:01.999
tearsofsteel_4k00001.jpg

00:00:02.000 --> 00:00:03.999
tearsofsteel_4k00002.jpg
```

## Usage omt video-bitrate

A metadata track of the video bitrate can be generated with this utility command. The resulting metadata track can then
be used
to visualize the video bitrate as a line chart on the Omakase Player timeline.

```text
usage: omt.py video-bitrate [-h] [-v] -i INPUT -o OUTPUT
                            [-s {1,2,3,4,5,10,12,15}]

options:
  -h, --help            show this help message and exit
  -v, --verbose         enable verbose output
  -i INPUT, --input INPUT
                        input video file
  -o OUTPUT, --output OUTPUT
                        output directory
  -s {1,2,3,4,5,10,12,15}, --seconds-interval {1,2,3,4,5,10,12,15}
                        seconds between bitrate samples
```

An input video file must be specified and the VTT and image files generated are written to the output directory
specified.

The resolution of the bitrate samples is controlled by the `--seconds-interval` CLI option.

### Example - Video Bitrate Metadata Track

```text
WEBVTT

NOTE
Omakase Player Web VTT
V1.0

00:00:00.000 --> 00:00:01.999
276.39:MEASUREMENT=avg:COMMENT=2-sec interval
```

**Please Note:** The OMP v1.0 VTT file format is a standard WebVTT file with the following additional metadata:

- The `:MEASUREMENT=<metric name>` tag is optional and can be used to specify the video bitrate metric.
- The `:COMMENT=<comment>` tag is optional indicates the sample interval for the bitrate metric.

The optional tags are used by the Omakase Player to provide telemetry metadata for the video bitrate metric as the video
is played.

## Usage omt audio-metrics

Audio metrics can be generated for an audio tracks, or all audio tracks, with this CLI command. At present, two audio
metric metadata tracks are created for each audio file:

- RMS Levels using the **ffmpeg** `ametadata` filter
- R128 Momentary Loudness also using the **ffmpeg** `ametadata` filter

If `--input` is a directory, all of the `wav` and `aac` files in the current directory are processed. If `--input` is
a file, only the audio file specified is processed.

The resulting metadata tracks are named with the basename of the audio file and appended with `R128_2-SEC` or
`RMS_2-SEC` respectively. All files are written to the directory specified with `--output`.

At present, the metrics are calculated as an average over a two-second interval.

```text
usage: omt.py audio-metrics [-h] [-v] -i INPUT -o OUTPUT

options:
  -h, --help            show this help message and exit
  -v, --verbose         enable verbose output
  -i INPUT, --input INPUT
                        input media file or directory
  -o OUTPUT, --output OUTPUT
                        output directory
```

### Example - Audio Metrics Metadata Track

```text
WEBVTT

NOTE
Omakase Player Web VTT
V1.0

00:00:00.000 --> 00:00:01.999
-56.033:MEASUREMENT=lavfi.r128.M:COMMENT=2-sec avg
```

**Please Note:** The OMP v1.0 VTT file format is a standard WebVTT file with the following additional metadata:

- The `:MEASUREMENT=<metric name>` tag is optional and can be used to specify the audio metric type.
- The `:COMMENT=<comment>` tag is optional and can be used to provide additional information about the audio metric.

The optional tags are used by the Omakase Player to provide telemetry metadata for the audio metric as the video is
played.

## Usage omt waveforms

The `waveforms` command generates audio waveform metadata tracks that can be used to provide an audio waveform
visualization in Omakase Player.

Waveform metadata can be generated for a single audio track, or all audio tracks, with this `omt` command. The
generated waveform includes the entire soundfield, but individual channels can be visualized with a dual-mono audio
track for each channel.

If `--input` is a directory, all of the `wav` and `aac` files in the current directory are processed. If `--input` is
a file, only the audio file specified is processed.

The resulting metadata tracks are named with the basename of the audio file All files are written to the directory
specified with `--output`.

At present, the metrics are calculated as an average over a 1-second interval.

```text
usage: omt.py waveforms [-h] [-v] -i INPUT -o OUTPUT

options:
  -h, --help            show this help message and exit
  -v, --verbose         enable verbose output
  -i INPUT, --input INPUT
                        input media file or directory
  -o OUTPUT, --output OUTPUT
                        output directory
```

### Example - Audio Waveform Metadata Track

```text
WEBVTT
  
00:00:00.000 --> 00:00:00.999
-0.0101, 0.0108
```

# External Links

___

- [Omakase Player Project Page](https://player.byomakase.org/)
- [Omakase Player GitHub Repository](http://github.com/byomakase/omakase-player)
- [Omakase Reference Player GitHub Repository](https://github.com/byomakase/omakase-reference-player)
- [ffmpeg Project Page](https://ffmpeg.org)
- [ffmpeg-bitrate-stats GitHub Repository](https://github.com/slhck/ffmpeg-bitrate-stats)
- [audiowaveform Project Page](https://www.bbc.co.uk/opensource/projects/audiowaveform)
- [audiowaveform GitHub Repository](https://github.com/bbc/audiowaveform)## License

# License

___
`omakase-media-tools`, Copyright 2024 ByOmakase, LLC (https://byomakase.org)


