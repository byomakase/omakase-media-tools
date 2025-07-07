# Omakase Player JSON

The sample media reference, and its ABR ladders, are referenced in the Omakase Player JSON file, which is documented
in the Omakase Reference Player GitHub repository available
here: [Omakase Reference Player GitHub Repository](https://github.com/byomakase/omakase-reference-player).

The documentation in the [Omakase Reference Player GitHub Repository](https://github.com/byomakase/omakase-reference-player)
should serve as your primary reference for the JSON file format used by the Omakase Reference Player.

This document highlights key locations in the Omakase Player JSON file which reference the ABR ladders
and temporal metadata tracks.

Throughout this document, the Omakase Player JSON file is referred to as the `player json`.

**Please Note:** The user is highly encouraged to use the `omt` utility with command `omt player-json` to generate the
`player json` file, or at least as a starting point. This will ensure that the `player json` file is correctly formatted
and can help remove some of the complexity.

# Video Track Reference

The url of the top-level HLS manifest of each ABR ladder you create with AWS MediaConvert should be referenced in the
Omakase Player `player json` under `media` in the `main` array as shown below:

```json
{
    "version": "3.0",
    "sources": [
        ...
    ],
    "media": {
        "main": [
            {
                "name": "Confidence QC 1080p",
                "type": "hls",
                "id": "HLS-1080",
                "url": "https://localhost/content/tears_of_steel/hls/tears-of-steel_sdr_1080p24_BITC/tears-of-steel.m3u8",
                "color_range": "sdr",
                "frame_rate": "24000/1000",
                "drop_frame": false
            },
            {
                "name": "Proxy 720p",
                "type": "hls",
                "id": "HLS-720",
                "url": "https://localhost/content/tears_of_steel/hls/tears-of-steel_sdr_720p24_BITC/tears-of-steel.m3u8",
                "color_range": "sdr",
                "frame_rate": "24000/1000",
                "drop_frame": false
            }
        ]
    },
    "presentation": {
        ...
    }
}
```

## Video Thumbnail Track and Video Analysis Track References

The thumbnail track created with `omt thumbnails` utility command and the video analysis track created with
`omt video-bitrate` utility command are referenced in the `player json` as shown below:

```json
{
    "version": "3.0",
    "sources": [
        ...
    ],
    "media": {
        "main": [
            ...
        ]
    },
    "presentation": {
        "timeline": {
            "tracks": [
                {
                    "id": "VT1",
                    "type": "video",
                    "name": "tearsofsteel_4k.mov",
                    "source_id": "V1",
                    "visual_reference": [
                        {
                            "type": "thumbnails",
                            "url": "https://localhost/content/tears_of_steel/thumbnails/thumbnails.vtt"
                        }
                    ],
                    "analysis": [
                        ...
                    ]
                },
                ...
            ]
        },
        "info_tabs": [
            ...
        ]
    }
}
```

## Audio Track Waveform and Analysis Track References

References to audio tracks in the `player_json` are shown below.

The `"media_id": "EN_20"` is the name of the full English 2.0 audio track in the ABR ladder HLS manifest. This is
specified as the `StreamName` in the AWS MediaConvert job settings. Please see the [MediaConvert
Job](/src/omakase_media_tools/docs/mediaconvert_job.md) documentation in this repository for more information where this
is explained in detail.

This is where the audio waveform created with `omt waveforms` is referenced in the `player_json`.

```json
{
    "version": "3.0",
    "sources": [
        ...
    ],
    "media": {
        "main": [
            ...
        ]
    },
    "presentation": {
        "timeline": {
            "tracks": [
                ...,
                {
                    "id": "AT1",
                    "type": "audio",
                    "name": "tearsofsteel_4k.mov (English 2.0)",
                    "source_id": "V1",
                    "media_id": "EN_20",
                    "channel_layout": "L R",
                    "language": "en",
                    "visual_reference": [
                        {
                            "type": "waveform",
                            "url": "https://localhost/content/tears_of_steel/waveforms/tears-of-steel_EN_20_L.vtt",
                            "channel": "L"
                        },
                        {
                            "type": "waveform",
                            "url": "https://localhost/content/tears_of_steel/waveforms/tears-of-steel_EN_20_R.vtt",
                            "channel": "R"
                        }
                    ],
                    "analysis": [
                        ...
                    ]
                },
                ...
            ]
        },
        "info_tabs": [
            ...
        ]
    }
}
```

For each audio sound field, multiple audio metadata tracks can be specified in the `analysis` array for the audio track
in the `player_json` as shown below.

This is where the audio metric tracks created with `omt audio-metrics` are referenced in the `player_json`.

```json
{
    "version": "3.0",
    "sources": [
        ...
    ],
    "media": {
        "main": [
            ...
        ]
    },
    "presentation": {
        "timeline": {
            "tracks": [
                ...,
                {
                    "id": "AT1",
                    "type": "audio",
                    "name": "tearsofsteel_4k.mov (English 2.0)",
                    "source_id": "V1",
                    "media_id": "EN_20",
                    "channel_layout": "L R",
                    "language": "en",
                    "visual_reference": [
                        ...
                    ],
                    "analysis": [
                        {
                            "name": "Dialog",
                            "type": "events",
                            "visualization": "marker",
                            "url": "https://localhost/content/tears_of_steel/analysis/dialog_audio_events_marker.vtt"
                        },
                        {
                            "name": "Scene Changes",
                            "type": "events",
                            "visualization": "point",
                            "url": "https://localhost/content/tears_of_steel/analysis/scene_changes_audio_events_point.vtt"
                        },
                        {
                            "name": "EBU R128 M",
                            "type": "chart",
                            "visualization": "bar",
                            "y_min": -100,
                            "y_max": 0,
                            "scale": "linear",
                            "url": "https://localhost/content/tears_of_steel/analysis/tears-of-steel_sdr_BITC_EN_20_R128_2-SEC.vtt"
                        },
                        {
                            "name": "RMS Levels",
                            "type": "chart",
                            "visualization": "line",
                            "url": "https://localhost/content/tears_of_steel/analysis/tears-of-steel_sdr_BITC_EN_20_RMS_2-SEC.vtt"
                        },
                        {
                            "name": "Overall RMS Levels",
                            "type": "chart",
                            "visualization": "led",
                            "y_min": -100,
                            "y_max": 0,
                            "scale": "linear",
                            "url": "https://localhost/content/tears_of_steel/analysis/tears-of-steel_sdr_BITC_EN_20_RMS_2-SEC.vtt"
                        }
                    ]
                },
                ...
            ]
        },
        "info_tabs": [
            ...
        ]
    }
}
```