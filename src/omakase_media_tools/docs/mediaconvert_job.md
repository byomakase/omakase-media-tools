# Tears of Steel MediaConvert Job

This document describes the MediaConvert job used to encode the Tears of Steel video. A detailed explanation of
MediaConvert transcoding job specifications is not possible, but this document should guide you on creating your own
MediaConvert job to create your own media.

The MediaConvert job used to build the _Tears of Steel_ sample media is a JSON file that is available in the repository
here: `/src/omakase_media_tools/mediaconvert/tears-of-steel_sdr_24_BITC.json`.

Another version of the MediaConvert job template with more advanced audio channel mapping is available here:
`/src/omakase_media_tools/mediaconvert/tears-of-steel_sdr_24_BITC_by-channels.json`.

The AWS MediaConvert User Guide is available
here: [AWS MediaConvert User Guide](https://docs.aws.amazon.com/mediaconvert/latest/ug/what-is.html).

# Input Source Media

Please see the separate page [Tears of Steel Source Media](/src/omakase_media_tools/docs/tears_of_steel_source_media.md)
for details on how to obtain the source media files from the Blender Foundation website.

## Defining the Input Video

The source mezzanine file `tearsofsteel_4k.mov`, downloaded from the _Tears of Steel_ Project website is used as the
source video file. This file is used as the input to the MediaConvert job.

It is defined in the `Inputs` section of the MediaConvert job JSON as shown below.

```json
{
  ...
  ...
    "Settings":{
        "Inputs": [
            "FileInput": "s3://your-input-bucket/tearsofsteel_4k.mov"
        ]
    }
}
```

## Defining the Input Audio Selectors

In the _Tears of Steel_ sample media reference, there are two sound fields used: English 2.0 and English 5.1. These are
defined in the `AudioSelectors` section of the MediaConvert job JSON as shown below.

Additional audio selectors are defined to isolate each channel of each sound field to create a dedicated audio track for
each channel in the output (to be explained further below).

```json
{
  ...
  ...
    "Settings":{
        "Inputs": [
            "AudioSelectors": {
                "EN 2.0": { ... },
                "EN 2.0 L": { ... },
                "EN 2.0 R": { ... },
                "EN 5.1":  { ... },
                "EN 5.1 L":  { ... },
                "EN 5.1 R":  { ... },
                "EN 5.1 C":  { ... },
                "EN 5.1 LFE":  { ... },
                "EN 5.1 LS":  { ... },
                "EN 5.1 RS":  { ... }
            }
        ]
    }
}
```

Audio tracks can be within the same container as the video essence or in separate external files. In this
example, the English 2.0 audio track is embedded in the same container as the video essence, while the English 5.1 audio
track is in a separate external files.

Examples of both are shown below:

```json
    "EN 2.0": {
        "Tracks": [
            1
        ],
        "DefaultSelection": "NOT_DEFAULT",
        "SelectorType": "TRACK"
    },
    ...
    ...
    "EN 5.1": {
        "Tracks": [
            1
        ],
        "DefaultSelection": "NOT_DEFAULT",
        "SelectorType": "TRACK",
        "ExternalAudioFileInput": "s3://your-input-bucket/blender/tears-of-steel/audio/Surround-TOS_DVDSURROUND-Dolby%205.1.ac3"
    }
```

**Please Note:** Defining the audio selectors in a MediaConvert job JSON can be very confusing to the uninitiated.
Please see the following AWS MediaConvert documentation for more
information: [Setting up audio tracks and audio selectors](https://docs.aws.amazon.com/mediaconvert/latest/ug/more-about-audio-tracks-selectors.html).

## Defining the Input Caption Selector

The external sidecar file `TOS-en.srt` is used as the source for the English subtitles. It is specified in alongside the
audio selectors and video selector.

```json
{
  ...
  ...
    "Settings":{
        "Inputs": [
            AudioSelectors: { ... },
            FileInput: "...",
            "CaptionSelectors": {
                "EN Subtitles": {
                    "SourceSettings": {
                        "SourceType": "SRT",
                        "FileSourceSettings": {
                            "SourceFile": "s3://your-input-bucket/blender/tears-of-steel/subtitles/TOS-en.srt"
                        }
                    }
                }
           }
        ]
    }
}
```

# Output Specification

The output specification is defined in the `OutputGroups` section of the MediaConvert job JSON. The output specification
defines the video and audio codecs, bitrates, resolutions, and other parameters for the output media files.

## ABR Ladders

In the _Tears of Steel_ sample media reference, two HLS ABR ladders are defined as shown below.

The `Apple HLS 720p Proxy` ABR ladder contains the following tracks:

- 720p24 video track at 2000 kbps
- English 2.0 sound field
- English 2.0 Left Channel as a dual-mono audio track
- English 2.0 Right Channel as a dual-mono audio track
- English Subtitles as a VTT track

The `Apple HLS 1080p w 5.1` ABR ladder contains the following tracks:

- 1080p24 video track at 5000 kbps
- English 2.0 sound field
- English 2.0 Left Channel as a dual-mono audio track
- English 2.0 Right Channel as a dual-mono audio track
- English 5.1 sound field
- English 5.1 Left Channel as a dual-mono audio track
- English 5.1 Right Channel as a dual-mono audio track
- English 5.1 Center Channel as a dual-mono audio track
- English 5.1 LFE Channel as a dual-mono audio track
- English 5.1 Ls Channel as a dual-mono audio track
- English 5.1 Rs Channel as a dual-mono audio track
- English Subtitles as a VTT track

```json
{
  ...
  ...
    "Settings":{
        "OutputGroups": [
            {
                "Name": "Apple HLS 720p Proxy",
                "Outputs": [
                    {"NameModifier":  "_720p24_2000" ... },
                    {"NameModifier":  "_EN_20" ... },
                    {"NameModifier":  "_EN_20_L" ... },
                    {"NameModifier":  "_EN_20_R" ... },
                    {"NameModifier":  "_EN_SUBS"  ... }
                ],
                "OutputGroupSettings": { ... }
            }
            {
                "Name": "Apple HLS 1080p w 5.1",
                "Outputs": [
                    {"NameModifier":  "_1080p24_5000" ... },
                    {"NameModifier":  "_EN_20" ... },
                    {"NameModifier":  "_EN_20_L" ... },
                    {"NameModifier":  "_EN_20_R" ... },
                    {"NameModifier":  "_EN_51" ... },
                    {"NameModifier":  "_EN_51_L" ... },
                    {"NameModifier":  "_EN_51_R" ... },
                    {"NameModifier":  "_EN_51_C" ... },
                    {"NameModifier":  "_EN_51_LFE" ... },
                    {"NameModifier":  "_EN_51_LS" ... },
                    {"NameModifier":  "_EN_51_RS" ... },
                    {"NameModifier":  "_EN_SUBS"  ... }
                 ],
                "OutputGroupSettings": { ... }
            }
    }
}
```

**IMPORTANT:** The destination you specify in the `OutputGroupSettings` section of the MediaConvert job JSON determines
the name of directory where the ABR ladder is written and the root name of the HLS manifest file. This will be needed to
configure the Omakase Player to play the media.

In the example below, the ABR ladder directory is `tears-of-steel_sdr_720p24_BITC` and the HLS manifest file will be
named `tears-of-steel.m3u8`.

```json
    "OutputGroupSettings": {
        "Type": "HLS_GROUP_SETTINGS",
        "HlsGroupSettings": {
            ...,
            "Destination": "s3://your-output-bucket/outputs/blender/tears-of-steel/hls/tears-of-steel_sdr_720p24_BITC/tears-of-steel",
            ...
        }
    }
```

## Video Specification

The specification of the video tracks in the ABR ladders can be modified to whatever matches your requirements. These
examples are basic and simple specifications to provide a simple working example.

## Audio Specification

The audio track specifications are also simple and straightforward, although the creation of dual-mono audio tracks
requires some further explanation.

In order to solo individual channels within Omakase Player, each channel of a sound field is isolated and duplicated to
form a dual-mono 2.0 audio track, that is the channel is duplicated to both the left and right channels of the audio
track.

By selecting a dual-mono audio track in the Omakase Player, the user can solo the individual channels of the sound
fields. This also allows the creation of an audio waveform for each channel as well as an audio metric visualization by
channel.

**IMPORTANT:** The `StreamName` setting in the `AudioDescriptions` section is used to map and identify the audio track
to the in the Omakase Player JSON file and associate the audio wave form and audio metric analysis tracks with the audio
track.

In the example below, `EN_20` would be used to refer to this track in the Omakase Player JSON file.

```json
                "Outputs": [
                    {
                        "ContainerSettings": { },
                        "AudioDescriptions": [
                            {
                                "AudioTypeControl": "FOLLOW_INPUT",
                                "AudioSourceName": "EN 2.0",
                                "CodecSettings": { },
                                "StreamName": "EN_20",
                                "LanguageCodeControl": "USE_CONFIGURED",
                                "AudioType": 0,
                                "LanguageCode": "ENG"
                            }
                        ],
                        "OutputSettings": { },
                        "NameModifier": "_EN_20"
                    }
```

## Subtitle Track Specification

The specification for the English Subtiles VTT track is shown below.

**IMPORTANT:** The `LanguageDescription` setting in the `CaptionDescriptions` section is used to map and identify the
subtitle track in the Omakase Player JSON file.

In the example below, `English Subtitles` would be used to refer to this track in the Omakase Player JSON file.

```json
                    {
                        "ContainerSettings": { ... },
                        "NameModifier": "_EN_SUBS",
                        "CaptionDescriptions": [
                            {
                                "CaptionSelectorName": "EN Subtitles",
                                "DestinationSettings": { ... },
                                },
                                "LanguageCode": "ENG",
                                "LanguageDescription": "English Subtitles"
                            }
                        ]
                    }
```

