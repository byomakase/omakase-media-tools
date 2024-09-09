# Omakase Player HLS Media

This sample of OMP media has been created from the _Tears of Steel_ open-source project. Please see the
top-level [README](/README.md) for more information about the _Tears of Steel_ project.

## Renditions

To demonstrate some features of Omakase Player, the _Tears of Steel_ mezzanine-level media has been transcoded
into two separate HLS ABR ladder renditions representing different use cases.

### Proxy Media Example

This rendition is intended as a general purpose low-resolution proxy with basic audio and no subtitles:

- 720p resolution
- 1.5 Mbps top bitrate
- English 2.0 sound field only

### Confidence QC Media Example

This rendition is an example of 'Confidence QC' media, e.g., to be used for the validation of sound field
configurations, track alignments, subtitle alignment, etc., but not qualitative video QC:

- 1080p resolution
- 4.5 Mbps top bitrate
- English 2.0 sound field
- English 5.1 sound field
- English subtitles

## Thumbnail Timeline

The thumbnail timeline track is a visual representation of the video timeline with thumbnail images at regular
intervals. For the purposes of this sample media, the thumbnails are generated at 10-second intervals from the mezzanine
video source.

You can create a thumbnail timeline track for your own media using the `omt thumbnails` utility and command
provided in the `src` directory of this repository. This utility uses **ffmpeg** to generate the thumbnails and creates
a VTT file that can be used as a thumbnail timeline track in Omakase Player.

**Please Note:** An example can be found in the repository
here: [/src/omakase_media_tools/media/tears-of-steel/thumbnails/thumbnails.vtt](/src/omakase_media_tools/media/tears-of-steel/thumbnails/thumbnails.vtt)

## Video Program Scenes Metadata Track

This metadata track provides an example of an `event` metadata track of visualization type `marker` used to show the
different scenes as program segments. This could be used to represent program segments for ad avails as another example.

The metadata track was created manually for demonstration purposes.

**Please Note:** An example can be found in the repository
here: [/src/omakase_media_tools/media/tears-of-steel/analysis/program-scenes.vtt](/src/omakase_media_tools/media/tears-of-steel/analysis/program-scenes.vtt)

## Video Points of Interest Metadata Track

This is another representation of the program scene changes, but with a different visual representation. This is an
example of an `event` metadata track of visualization type `point`.

The metadata track was also created manually for demonstration purposes.

**Please Note:** An example can be found in the repository
here: [/src/omakase_media_tools/media/tears-of-steel/analysis/program-poi.vtt](/src/omakase_media_tools/media/tears-of-steel/analysis/program-poi.vtt)

## Video Bitrate Visualization

A visualization of the mezzanine video bitrate over time is provided by another metadata track of type `chart` and
visualization of `line`. This is an example of a `metric` metadata track.

The video bitrate data is presented as an average over 2-second intervals, but could be generated with higher resolution
to meet your specific use-case.

This metadata track was generated using the `omt video-bitrate` utility and command provided in the `src` directory of this
repository. An open-source utility **ffmpeg-bitrate-stats** is used to generate the raw video bitrate
data, which is then post-processed into an OMP v1.0 VTT metadata track.

**Please Note:** An example can be found in the repository
here: [/src/omakase_media_tools/media/tears-of-steel/analysis/tearsofsteel_4k_2-SEC.vtt](/src/omakase_media_tools/media/tears-of-steel/analysis/tearsofsteel_4k_2-SEC.vtt)

## Audio Waveform Visualization

Each channel of each sound field is represented by a waveform visualization in the form of an audio waveform metadata
track. If channel level waveforms are not required, and a single waveform visualization per sound field would be
sufficient, the Omakase Player JSON can accommodate this configuration as well.

These waveforms provide samples at a resolution of one sample every second, but could be generated with at a higher or
lower resolution to meet your specific use-case.

The waveforms were generated using the `omt waveforms` utility provided in the `src` directory of
this repository. The utility uses the **audiowaveform** open-source project from the BBC to generate the raw audio
waveform data, which is then post-processed into OMP v1.0 VTT files.

**Please Note:** An example can be found in the repository
here: [/src/omakase_media_tools/media/tears-of-steel/waveforms/tears-of-steel_EN_20_L.vtt](/src/omakase_media_tools/media/tears-of-steel/waveforms/tears-of-steel_EN_20_L.vtt)

## Dialog Metadata Track

This metadata track is another example of a metadata track of type `event` and visualization of `marker`, providing a
visualization on the timeline of when there is dialog present in the audio.

The metadata track was also created manually for demonstration purposes.

**Please Note:** An example can be found in the repository
here: [/src/omakase_media_tools/media/tears-of-steel/analysis/dialog.vtt](/src/omakase_media_tools/media/tears-of-steel/analysis/dialog.vtt)

## Audio Program Scene Changes Metadata Track

This metadata track provides an example of an `event` metadata track of visualization type `marker` used to show the
different scenes as program segments. This could be used to represent program segments for ad avails as another example.

This metadata track is identical to the video program scenes metadata track, but is attached to each of the audio tracks
for this sample media.

The metadata track was created manually for demonstration purposes.

**Please Note:** An example can be found in the repository
here: [/src/omakase_media_tools/media/tears-of-steel/analysis/program-scenes.vtt](/src/omakase_media_tools/media/tears-of-steel/analysis/program-scenes.vtt)

## Audio RMS Levels Metadata Track

This is an example of a metadata analysis track using an audio metric. In this case, the RMS levels of an entire sound
field have been sampled and averaged over a 2-second interval. The metric is visualized with a type of `chart` and
visualization of type `line`.

The RMS levels were generated using the `omt audio-metrics` utility provided in the `src` directory
of this repository. The utility uses **ffmpeg** to generate the raw audio metric data, which is then post-processed into
OMP v1.0 VTT files.

**Please Note:** An example can be found in the repository
here: [/src/omakase_media_tools/media/tears-of-steel/analysis/tears-of-steel_sdr_BITC_EN_20_RMS_2-SEC.vtt](/src/omakase_media_tools/media/tears-of-steel/analysis/tears-of-steel_sdr_BITC_EN_20_RMS_2-SEC.vtt)

## Audio R128 Momentary Loudness Metadata Track

Similar to the audio RMS levels metadata track, this metadata track provides the R128 Momentary Loudness metric for the
sound field, and is sampled and averaged over a 2-second interval.

The metric is visualized with a type of `chart` and visualization of type `bar`. This visualization uses some additional
visual styling to represent the R128 Momentary Loudness metric, which may be of interest.

This metric is also generated using the `omt audio-metrics` utility and command provided in the `src` directory
of this repository using **ffmpeg**.

**Please Note:** An example can be found in the repository
here: [/src/omakase_media_tools/media/tears-of-steel/analysis/tears-of-steel_sdr_BITC_EN_20_R128_2-SEC.vtt](/src/omakase_media_tools/media/tears-of-steel/analysis/tears-of-steel_sdr_BITC_EN_20_R128_2-SEC.vtt)

## Audio Overall RMS Levels Metadata Track

This is the same metric as the Audio RMS Levels Metadata Track, but using a different visualization type for
demonstration purposes. This instance is of type `chart` and visualization of type `led`.

**Please Note:** An example can be found in the repository
here: [/src/omakase_media_tools/media/tears-of-steel/analysis/tears-of-steel_sdr_BITC_EN_20_RMS_2-SEC.vtt](/src/omakase_media_tools/media/tears-of-steel/analysis/tears-of-steel_sdr_BITC_EN_20_RMS_2-SEC.vtt)


