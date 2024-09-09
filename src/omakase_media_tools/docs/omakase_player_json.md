# Omakase Player JSON

The sample media reference, and its ABR ladders, are referenced in the Omakase Player JSON file, which is documented
on the Omakase Player GitHub repository available
here: [Omakase Player GitHub Repository](http://github.com/byomakase/omakase-player).

The documentation on the Omakase Player GitHub should serve as your primary reference for the JSON file format used by
the Omakase Player.

This document highlights some key points, however, to illustrate how ABR ladders you create with AWS MediaConvert, and
the temporal metadata tracks generated with the `omt.py` CLI utility from this repository, are referenced in the Omakase
Player JSON file.

Throughout this document, the Omakase Player JSON file is referred to as the `player json`.

**Please Note:** The user is highly encouraged to use the `omt` utility with command `omt player-json` to generate the
`player json` file, or at least as a starting point. This will ensure that the `player json` file is correctly formatted
and can help remove some of the complexity.

# Video Track Reference

The url of the top-level HLS manifest of each ABR ladder you create with AWS MediaConvert should be referenced in the
Omakase Player `player json` in the `master_manifests` array as shown below:

```json
{
    "security_token": "tbd",
    "data": {
        "source_info": [
            ...
        ],
        "media_info": [
            ...
        ],
        "master_manifests": [
            {
                "name": "Confidence QC 1080p",
                "id": "HLS-1080",
                "url": "https://localhost/tearsofsteel/v1/hls/tears-of-steel_sdr_1080p24_BITC/tears-of-steel.m3u8",
                "width": 1920,
                "height": 1080,
                "bitrate_kb": 5000,
                "codec": "h264",
                "color_range": "sdr",
                "frame_rate": "24000/1000",
                "drop_frame": false
            }
        ],
        "media_tracks": [
            ...
        ],
        "presentation": [
            ...
        ]
    }
}
```

## Video Thumbnail Track and Video Analysis Track References

The thumbnail track created with `omt thumbnails` utility command and the video analysis track created with
`omt video-bitrate` utility command are referenced in the `player json` in the `media_tracks` `video` section as shown
below.

```json
{
    "security_token": "tbd",
    "data": {
        "source_info": [
            ...
        ],
        "media_info": [
            ...
        ],
        "master_manifests": [
            ...
        ],
        "media_tracks": {
            "video": [
                {
                    "name": "tearsofsteel_4k.mov",
                    "source_id": "V1",
                    "manifest_ids": [
                        ...
                    ],
                    "visual_reference": [
                        {
                            "type": "thumbnails",
                            "url": "https://localhost/tearsofsteel/v1/thumbnails/thumbnails.vtt"
                        }
                    ],
                    "analysis": [
                        {
                            "name": "Bit Rate",
                            "type": "chart",
                            "visualization": "line",
                            "url": "https://localhost/tearsofsteel/v1/analysis/tearsofsteel_4k_2-SEC.vtt"
                        }
                    ]
                }
            ],
            "audio": [
                ...
            ],
            "text": [
                ...
            ]
        },
        "presentation": [
            ...
        ]
    }
}
```

## Audio Track Waveform and Analysis Track References

References to audio tracks in the `player_json` are shown below.

The `"program_name": "EN_20"` is the name of the full English 2.0 audio track in the ABR ladder HLS manifest. This is
specified as the `StreamName` in the AWS MediaConvert job settings. Please see the [MediaConvert
Job](/src/omakase_media_tools/docs/mediaconvert_job.md) documentation in this repository for more information where this
is explained in detail.

Below the reference to the full English 2.0 audio track is the reference to the left channel dual-mono audio track from
the HLS ABR ladder, which is `"program_name": "EN_20_L"` in the `player_json`.

(This allows individual sound field channels to be solo'ed and visualized in the Omakase Player.)

This is where the audio waveform created with `omt waveforms` is referenced in the `player_json`.

```json
{
    "security_token": "tbd",
    "data": {
        "source_info": [
            ...
        ],
        "media_info": [
            ...
        ],
        "master_manifests": [
            ...
        ],
        "media_tracks": {
            "video": [
                ...
            ],
            "audio": [
                {
                    "name": "tearsofsteel_4k.mov (English 2.0)",
                    "source_id": "V1",
                    "program_name": "EN_20",
                    "channel_layout": "L R",
                    "language": "en",
                    "channels": [
                        {
                            "channel_order": "L",
                            "program_name": "EN_20_L",
                            "visual_reference": [
                                {
                                    "type": "waveform",
                                    "url": "https://localhost/tearsofsteel/v1/waveforms/tears-of-steel_EN_20_L.vtt"
                                }
                            ]
                        },
                        {
                            ...
                        }
                    ],
                    "analysis": [
                        ...
                    ]
                }
            ]
            "text": [
                ...
            ]
        },
        "presentation": [
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
    "security_token": "tbd",
    "data": {
        "source_info": [
            ...
        ],
        "media_info": [
            ...
        ],
        "master_manifests": [
            ...
        ],
        "media_tracks": {
            "video": [
                ...
            ],
            "audio": [
                {
                    "name": "tearsofsteel_4k.mov (English 2.0)",
                    "source_id": "V1",
                    "program_name": "EN_20",
                    "channel_layout": "L R",
                    "language": "en",
                    "channels": [
                        ...
                    ],
                    "analysis": [
                        {
                            "name": "RMS Levels",
                            "type": "chart",
                            "visualization": "line",
                            "url": "https://localhost/tearsofsteel/v1/analysis/tears-of-steel_sdr_BITC_EN_20_RMS_2-SEC.vtt"
                        }
                    ]
                }
            ],
            "text": [
                ...
            ]
        },
        "presentation": [
            ...
        ]
    }
}
```