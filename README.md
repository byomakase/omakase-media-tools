# Omakase Player Media Tools and Sample Media Reference

This repository contains the `omt` utility and sample media reference for use with
the [Omakase Player](https://player.byomakase.org/)
and [Omakase Reference Player](https://github.com/byomakase/omakase-reference-player) open source projects.

The sample media is provided to demonstrate the capabilities of the Omakase Player framework and to bootstrap small POC
projects. The sample media reference and `omt` utility are provided as-is and are not intended for use in production
environments.

The `omt` utility and documentation can be used to create your own sample media, temporal metadata tracks and OMP player
JSON for use with the Omakase Player framework and the Omakase Reference Player.

# Contents

- [Introduction](#introduction)
- [Source Media](#source-media)
- [Omakase Player HLS Media](#omakase-player-hls-media)
- [Omakase Player JSON](#omakase-player-json)
- [MediaConvert Job](#mediaconvert-job)
- [Dolby Hybrik Job](#dolby-hybrik-job)
- [Command Line Utility](#command-line-utility)
    - [Player JSON Generator](#player-json-generator)
    - [Thumbnail Generator](#thumbnail-generator)
    - [Video Bitrate Visualization Generator](#video-bitrate-visualization-generator)
    - [Audio Waveform Visualization Generator](#audio-waveform-visualization-generator)
    - [Audio Metrics Generator](#audio-metrics-generator)
- [External Links](#external-links)

# Introduction

___
This repository provides a sample media reference and CLI utility (the `omt` utility) for use with the Omakase Player
framework. An annotated player JSON file is provided with the media, which contains examples of the different types of
temporal metadata tracks and visualizations available with the Omakase Player framework. The `omt` utility can be used
to create your own temporal metadata tracks for use with the Omakase Player framework.

This sample media reference is intended to serve as an example for creating your own sample media, player JSON and
temporal metadata tracks for demonstration and POC purposes.

Further documentation is provided below to assist you with the following:

- How to obtain the source mezzanine-level media for _Tears of Steel_
- Documentation of the sample media reference and description of the visualizations and temporal metadata tracks
  that are provided as an example
- An AWS MediaConvert job template for transcoding the source media, which can be used as a guide and modified for your
  own media
- An annotated Omakase Player JSON file to assist in creating your own player JSON
- Documentation for the CLI utility `omt` to generate your own temporal metadata tracks for use
  with the Omakase Player framework.

# [Source Media](src/omakase_media_tools/docs/tears_of_steel_source_media.md)

___
(Further detailed documentation can be found here: [_Tears of
Steel_ Source Media](src/omakase_media_tools/docs/tears_of_steel_source_media.md).)

This sample media reference is based upon the open source media project _Tears of Steel_ sponsored by the Blender
Foundation, a 12-minute short film created using open source software and released under the Creative Commons
Attribution 3.0 license.

The _Tears of Steel_ project page can be found here:

- [_Tears of Steel_ Project Page](https://mango.blender.org/)

The details for downloading the original mezzanine-level media for building your own sample media can be found here:

- [_Tears of Steel_ Source Media](src/omakase_media_tools/docs/tears_of_steel_source_media.md)

# [Omakase Player HLS Media](src/omakase_media_tools/docs/omakase_player_hls_media.md)

___
(Further detailed documentation can be found
here: [Omakase Player HLS Media](src/omakase_media_tools/docs/omakase_player_hls_media.md))

For this sample media reference, the _Tears of Steel_ mezzanine-level media has been transcoded into two separate HLS
ABR ladders to demonstrate features of the Omakase Player framework and provide examples of the sidecar metadata
files used to render analysis and visualization tracks the Omakase Player framework.

Please see the link above for a very detailed description of the sample reference media and the visualizations and
temporal metadata tracks that are available.

### Proxy Media Example

An example of a general purpose low-resolution proxy with basic audio and no subtitles:

- 720p resolution
- 1.5 Mbps top bitrate
- English 2.0 sound field only

### Confidence QC Media Example

An example of 'Confidence QC' media, e.g., to be used for validation of sound field configurations, track alignments,
subtitle timing, etc., but not qualitative video QC:

- 1080p resolution
- 4.5 Mbps top bitrate
- English 2.0 sound field
- English 5.1 sound field
- English subtitles

# [Omakase Player JSON](src/omakase_media_tools/docs/omakase_player_json.md)

___
(Further detailed documentation can be found
here: [Omakase Player JSON](src/omakase_media_tools/docs/omakase_player_json.md).)

An annotated Omakase Player JSON file is provided for the _Tears of Steel_ same media, which is populated with examples
of different types of temporal metadata tracks for visualization in Omakase Player:

**Video**

- Thumbnail timeline track
- Video bitrate as a line chart
- Program scenes as a marker event metadata track
- Points-of-Interest as a point event metadata track

**Audio**

- Audio waveform visualizations
- Dialog timeline as a marker event metadata track
- Scene changes as a point event metadata track
- Audio RMS Levels presented as a line chart
- EBU R128 M metric presented as a bar chart
- Audio RMS Levels presented as a LED chart

**Subtitles**

- Subtitle visualization metadata track

# [MediaConvert Job](/src/omakase_media_tools/docs/mediaconvert_job.md)

___
(Further detailed documentation can be found
here: [MediaConvert Job](src/omakase_media_tools/docs/mediaconvert_job.md).)

AWS MediaConvert was used to transcode the _Tears of Steel_ mezzanine media into the two HLS ABR ladders.

The AWS MediaConvert job JSON template used is provided as an example on how to transcode the _Tears of Steel_
mezzanine media for use with the Omakase Player framework.

The job template is provided as a JSON file that can be imported into an AWS MediaConvert job and is annotated on the
page above with comments to help you generate your own media.

# [Dolby Hybrik Job](/src/omakase_media_tools/docs/dolby_hybrik_job.md)

___
(Further detailed documentation can be found
here: [Dolby Hybrik Job](src/omakase_media_tools/docs/dolby_hybrik_job.md).)

Dolby Hybrik was also used to transcode the _Tears of Steel_ mezzanine media into the two HLS ABR ladders.

The Dolby Hybrik job JSON used is provided as an example on how to transcode the _Tears of Steel_ mezzanine media for
use with the Omakase Player framework.

The job JSON provided can be imported into Hybrik and is annotated on the page above with comments to help you generate
your own media.

# [Command Line Utility](src/omakase_media_tools/docs/omt.md)

___
In a production environment, workflow automation would generate the necessary temporal metadata tracks for use in
Omakase Player from the mezzanine-level media.

For POC and demo use cases, the repository includes the CLI utility `omt`, a Python utility that supports numerous
commands to generate temporal metadata tracks and an OMP player json for your own media.

## [Player JSON Generator](src/omakase_media_tools/docs/omt.md)

- (Further detailed documentation can be found
  here: [omt.py](src/omakase_media_tools/docs/omt.md).)

The Python utility command `omt player-json` can generate an OMP Player json file from a template and access to the
source media, HLS media and metadata tracks. A default directory structure is used to stage the media and metadata
tracks, which is then searched to find the correct paths to populate the OMP Player json.

## [Thumbnail Generator](src/omakase_media_tools/docs/omt.md)

- (Further detailed documentation can be found
  here: [omt.py](src/omakase_media_tools/docs/omt.md).)

The Python utility with command `omt thumbnails` can generate a thumbnail timeline track for use in
the Omakase Player. The frequency with which thumbnails are generated can be adjusted to meet your needs.

The `omt` utility uses **ffmpeg** to generate a series of thumbnails from a video file and then creates a JSON file that
can be used to render the thumbnails in Omakase Player.

## [Video Bitrate Visualization Generator](src/omakase_media_tools/docs/omt.md)

- (Further detailed documentation can be found
  here: [omt.py](src/omakase_media_tools/docs/omt.md).)

The Python utility with command `omt video-bitrate` can generate the metadata track used to visualize the video bitrate
of the mezzanine media file in Omakase Player.

The utility uses the open-source **ffmpeg-bitrate-stats** Python package to generate the raw metrics, which are then
processed into a temporal metadata track for Omakase Player.

## [Audio Waveform Visualization Generator](src/omakase_media_tools/docs/omt.md)

- (Further detailed documentation can be found
  here: [omt.py](src/omakase_media_tools/docs/omt.md).)

The waveform visualization of an entire audio sound field or an individual audio channel in Omakase Player can be
created with a metadata track generated by the Python utility with command `omt waveforms`.

The utility uses the open-source **audiowaveform** project from the BBC to generate the raw audio metrics, which are
then
processed into a temporal metadata track for use in Omakase Player.

## [Audio Metrics Generator](src/omakase_media_tools/docs/omt)

- (Further detailed documentation can be found
  here: [omt.py](src/omakase_media_tools/docs/omt.md).)

The Python script and option `omt audio-metrics` can generate an audio metric metadata track that can render metric
visualizations in Omakase Player.

Two sample audio metrics are available:

- RMS Levels using the **ffmpeg** `ametadata` filter
- R128 Momentary Loudness also using the `ametadata` filter

# External Links

___

- [Omakase Player Project Page](https://player.byomakase.org/)
- [Omakase Player GitHub Repository](http://github.com/byomakase/omakase-player)
- [Omakase Reference Player GitHub Repository](https://github.com/byomakase/omakase-reference-player)
- [Tears of Steel Project Page](http://mango.blender.org/)
- [Tears of Steel Media Download Page](https://mango.blender.org/download/)
- [ffmpeg Project Page](https://ffmpeg.org)
- [ffmpeg-bitrate-stats GitHub Repository](https://github.com/slhck/ffmpeg-bitrate-stats)
- [audiowaveform Project Page](https://www.bbc.co.uk/opensource/projects/audiowaveform)
- [audiowaveform GitHub Repository](https://github.com/bbc/audiowaveform)
- [MediaInfo Project Page](https://mediaarea.net/MediaInfo)