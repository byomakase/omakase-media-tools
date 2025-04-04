# Tears of Steel Dolby Hybrik Job

This document describes the Dolby Hybrik job used to encode the Tears of Steel video. A detailed explanation of
Dolby Hybrik transcoding job specifications is not possible, but this document should guide you on creating your own
Hybrik job to create your own media.

The Dolby Hybrik job used to build the _Tears of Steel_ sample media is a JSON file that is available in the repository
here: `/src/omakase_media_tools/hybrik/tears-of-steel_sdr_24_BITC.json`.

Please see the following documentation links for more information:

- [Dolby Hybrik Tutorials](https://tutorials.hybrik.com/)
- [Dolby Hybrik Samples on GitHub](https://github.com/hybrik/hybrik-samples/tree/master)
- [Dolby Hybrik API Getting Started Guide](https://docs.hybrik.com/api/v1/HybrikAPI.html?#getting-started)

# Input Source Media

Please see the separate page [Tears of Steel Source Media](/src/omakase_media_tools/docs/tears_of_steel_source_media.md)
for details on how to obtain the source media files from the Blender Foundation website.

## Defining the Input Video

The source mezzanine file `tearsofsteel_4k.mov`, downloaded from the _Tears of Steel_ Project website is used as the
source video file. This file is used as the input to the Hybrik job.

```json
{
    "definitions": {
        "descriptor": "tears_of_steel_24fps",
        "source_path": "s3://your-source-bucket/stems/blender/tears-of-steel",
        "source_filename": "tearsofsteel_4k.mov",
        "audio_filename": "Surround-TOS_DVDSURROUND-Dolby%205.1.ac3",
        "subtitle_filename": "TOS-en.srt",
        "destination_path": "s3://your-output-bucket/outputs/blender/tears-of-steel/hybrik/{{descriptor}}",
        "segment_duration": 6
    }
}
```

These definitions are used as string replacements in the Hybrik job JSON to enable job portability and reusability.

As an example, one can see in the JSON snippet below how the `source_path` and `source_filename` definitions are used to
specify the source video file.

The following json snippet is from `payload.elements[0].payload.payload`.

```json
{
    "asset_versions": [
        {
            "version_uid": "audio_video",
            "asset_components": [
                {
                    "component_uid": "audio_video",
                    "kind": "name",
                    "name": "{{source_filename}}",
                    "location": {
                        "storage_provider": "s3",
                        "path": "{{source_path}}"
                    }
                }
            ]
        }
    ]
}
```

## Defining the Input Audio Tracks

In the _Tears of Steel_ sample media reference, there are two sound fields used: English 2.0 and English 5.1.

The English 2.0 audio track muxed with the video is declared as `Track 1`, and the English 5.1 audio track from the
audio
sidecare file is declared as `Track 2`.

These are defined using the same definitions very close to where the video track is declared in the following json
snippet from `payload.elements[0].payload.payload.asset_versions`.

```json
{
    "asset_components": [
        {
            "component_uid": "audio_video",
            "kind": "name",
            "name": "{{source_filename}}",
            "location": {
                "storage_provider": "s3",
                "path": "{{source_path}}"
            },
            "contents": [
                { ... },
                {
                    "kind": "audio",
                    "map": [
                        {
                            "input": { ... },
                            "output": {
                                "track": 0
                            }
                        }
                    ]
                }
            ]
        }
    ]
}
```

## Defining the Input Subtile Selector

The external sidecar file `TOS-en.srt` is used as the source for the English subtitles. It is specified alongside the
audio selectors and video selector.

This declaration using the same definitions is very close to where the video track is declared in the following json
snippet from `payload.elements[0].payload.payload`.

```json
{
    "kind": "name",
    "component_uid": "captions",
    "name": "{{subtitle_filename}}",
    "location": {
        "storage_provider": "s3",
        "path": "{{source_path}}"
    },
    "contents": [
        {
            "kind": "subtitle",
            "payload": {
                "format": "srt",
                "language": "eng"
            }
        }
    ]
}
```

# Output Specification

In a Hybrik job, the specification of the output media is broken up into two parts: the output specification and the ABR
ladder packaging.

## Media Transcoding

The media transcoding specification is defined in the`payload.elements[3 ('transcode_all_renditions') ].payload.targets`
section of the Hybrik job JSON

**PLEASE NOTE:** The naming of the output files is important as the `omt` uses the naming convention to identify the
different tracks when generating the OMP Player JSON with the `omt player-json` command.

In the example below, the `EN_20` audio track is the English 2.0 sound field.

```json
{
    "targets": [
        { "file_pattern": "{source_basename}_720p24{default_extension}" ... },
        { "file_pattern": "{source_basename}_1080p24{default_extension}" ... },
        { "file_pattern": "{source_basename}_EN_20{default_extension}" ... },
        { "file_pattern": "{source_basename}_EN_51{default_extension}" ... },
        { "file_pattern": "{source_basename}_EN_SUBS.vtt" ... }
    ]
}
```

## ABR Ladder Packaging

In the _Tears of Steel_ sample media reference, two HLS ABR ladders are defined as shown below.

The `hls_single_fmp4_720p` ABR ladder contains the following tracks:

- 720p24 video track at 2000 kbps
- English 2.0 sound field
- English Subtitles as a VTT track

The `hls_single_fmp4_1080p` ABR ladder contains the following tracks:

- 1080p24 video track at 5000 kbps
- English 2.0 sound field
- English 5.1 sound field
- English Subtitles as a VTT track

The packaging of the media outputs into the ABR ladders is defined in the following locations in the Hybrik job JSON:

- `payload.elements[4 ('hls_single_fmp4_720p')].payload`
- `payload.elements[5 ('hls_single_fmp4_1080p')].payload`

The following is a JSON snippet from the 'hls_single_fmp4_720p' section:

```json
{
    "uid": "hls_single_fmp4_720p",
    "task": {
        "extended": {
            "start_payload_filter": {
                "processing_group_ids": [
                    "hls_720p"
                ]
            }
        },
        "name": "package_720p"
    },
    "kind": "package",
    "payload": {
        "uid": "main_manifest",
        "kind": "hls",
        "location": {
            "storage_provider": "s3",
            "path": "{{destination_path}}/tears-of-steel_sdr_720p24_BITC"
        },
        "file_pattern": "{source_basename}.m3u8",
        "segmentation_mode": "fmp4",
        "segment_duration_sec": "{{segment_duration}}",
        "force_original_media": false,
        "media_location": {
            "storage_provider": "s3",
            "path": "{{destination_path}}/tears-of-steel_sdr_720p24_BITC",
            "attributes": [
                {
                    "name": "ContentType",
                    "value": "application/x-mpegURL"
                }
            ]
        },
        "media_file_pattern": "{source_basename}.fmp4",
        "hls": {
            "version": 7,
            "media_playlist_location": {
                "storage_provider": "s3",
                "path": "{{destination_path}}/tears-of-steel_sdr_720p24_BITC",
                "attributes": [
                    {
                        "name": "ContentType",
                        "value": "application/x-mpegURL"
                    }
                ]
            }
        }
    }
}
```

**IMPORTANT:** The destination directory you specify in the Hybrik job JSON is the name of directory where the ABR
ladder and HLS manifest file are written. This will be needed to build the OMP Player JSON.

## Video Specification

The specification of the video tracks in the ABR ladders can be modified to whatever matches your requirements. These
examples are basic and simple specifications to provide a simple working example.

## Audio Specification

The audio track specifications are also simple and straightforward.

**IMPORTANT:** As mentioned above, the filename used for the audio tracks is used to map and identify the audio track
to the in the Omakase Player JSON file and associate the audio wave form and audio metric analysis tracks with the audio
track.

For example, the `EN_20` audio track is the English 2.0 sound field. When `EN_20` is appended to the filename,
this allows generation of the OMP Player JSON with the `omt player-json` command.

## Subtitle Track Specification

As with the audio tracks, the use of the appendix text `EN_SUBS` in the filename is used to map and identify the
subtitle track in the Omakase Player JSON file.

# HLS Manifest Post Processing

The HLS manifest for each HLS ABR ladder requires some manual post-processing in order for the `omt player-json` command
to generate the OMP Player JSON correctly and completely.

An example of a Hybrik HLS manifest after manual post-processing is can be found here:
- `/src/omakase_media_tools/hybrik/tears-of-steel_sdr_24_BITC.m3u8`.



The `omt player-json` uses the `NAME` attribute of a stream in the HLS manifest to identify the video, audio, and
subtitle streams and associate them with the media tracks in the OMP Player JSON.

For each of the audio streams in the HLS manifest, the `NAME` attribute must be set to the value appended to the stream
filename. For example, the `EN_20` audio stream must have the `NAME` attribute set to `EN_20`.

As an example, a snippet of the original Hybrik generated HLS manifest is shown below:
```text
#EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="audio_high",LANGUAGE="en",NAME="English",AUTOSELECT=YES,DEFAULT=YES,CHANNELS="2",URI="tearsofsteel_4k_EN_20.m3u8"
#EXT-X-MEDIA:TYPE=SUBTITLES,GROUP-ID="subs",NAME="English",DEFAULT=NO,AUTOSELECT=YES,FORCED=NO,LANGUAGE="en",URI="tearsofsteel_4k_EN_SUBS.m3u8"
```

After manual post-processing, the HLS manifest should look like this:
```text
#EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="audio_high",NAME="EN_20",LANGUAGE="en",AUTOSELECT=YES,DEFAULT=YES,CHANNELS="2",URI="tearsofsteel_4k_EN_20.m3u8"
#EXT-X-MEDIA:TYPE=SUBTITLES,GROUP-ID="subs",NAME="English Subtitles",DEFAULT=NO,AUTOSELECT=YES,FORCED=NO,LANGUAGE="en",URI="tearsofsteel_4k_EN_SUBS.m3u8"
```


