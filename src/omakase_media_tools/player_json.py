import json
import os.path
import re
from argparse import Namespace
from pathlib import Path

from omakase_media_tools.mediainfo import get_mediainfo_json


def add_version(player_json: dict, template: dict) -> dict:
    player_json["version"] = "2.0"
    return player_json

def add_session(player_json: dict, template: dict) -> dict:
    player_json["session"] = {
        "services": {
            "media_authentication": {
                "type": "none"
            }
        }
    }
    return player_json


def add_source_info(player_json: dict, template: dict) -> dict:
    sources = template["sources"]["mezzanine"]
    for source in sources:
        base_source_name = os.path.basename(source["src"])
        media_format = (os.path.splitext(base_source_name)[1]).lstrip(".").upper()

        media_filepath = os.path.join(template["output"]["sources_dir"], source["src"])
        mediainfo = get_mediainfo_json(media_filepath)

        media_entry = {"name": base_source_name, "id": source["id"], "format": media_format}

        # Video sources
        if source["id"].startswith("V") and mediainfo["media"]:
            media_entry["bandwidth"] = mediainfo["media"]["track"][0]["OverallBitRate_String"]
            media_entry["duration"] = float(mediainfo["media"]["track"][0]["Duration"])

            # How many video tracks are present
            video_count = mediainfo["media"]["track"][0]["VideoCount"]
            media_entry["video_tracks"] = int(video_count)

            # How many audio tracks are present
            audio_tracks = mediainfo["media"]["track"][0]["AudioCount"]
            media_entry["audio_tracks"] = int(audio_tracks)

            # How many audio channels are present
            channel_count = mediainfo["media"]["track"][0]["Audio_Channels_Total"]
            media_entry["channel_count"] = int(channel_count)

        # Audio sources
        elif source["id"].startswith("A") and mediainfo["media"]:
            media_entry["sample_rate"] = mediainfo["media"]["track"][1]["SamplingRate_String"]
            media_entry["duration"] = float(mediainfo["media"]["track"][0]["Duration"])

            # How many audio tracks are present
            audio_tracks = mediainfo["media"]["track"][0]["AudioCount"]
            media_entry["audio_tracks"] = int(audio_tracks)

            # How many audio channels are present
            channel_count = mediainfo["media"]["track"][0]["Audio_Channels_Total"]
            media_entry["channel_count"] = int(channel_count)

            # Hardcoding English language for now
            media_entry["language"] = "ENG"

        # Texted sources
        elif source["id"].startswith("T") and mediainfo["media"]:
            media_entry["duration"] = mediainfo["media"]["track"][0]["Duration"]

            # Hardcoding English language for now
            media_entry["language"] = "ENG"

            # Hardcoding subtitles for usage for now
            media_entry["usage"] = "subtitles"

        player_json["data"]["source_info"].append(media_entry)

    return player_json


def add_media_info(player_json: dict, template: dict) -> dict:
    sources = template["sources"]["mezzanine"]
    for source in sources:
        media_filepath = os.path.join(template["output"]["sources_dir"], source["src"])
        mediainfo = get_mediainfo_json(media_filepath)

        media_entry = {"source_id": source["id"]}

        if mediainfo["media"]:
            track = mediainfo["media"]["track"]
        else:
            track = []
        media_entry["general_properties"] = {"track": track}

        player_json["data"]["media_info"].append(media_entry)

    return player_json


def find_master_m3u8_manifest(hls_dir: str) -> str:
    for filename in os.listdir(hls_dir):
        filepath = os.path.join(hls_dir, filename)
        try:
            if os.path.isfile(filepath) and filename.endswith(".m3u8"):

                with open(filepath, 'r') as file:
                    if "EXT-X-STREAM-INF" in file.read():
                        return filepath
        except FileNotFoundError:
            print(f"Error: M3u8 manifest file not found at {file}")
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in m3u8 manifest file at {file}")
        except Exception as e:
            print(f"An unexpected error occurred with m3u8 manifest file {file} :: {str(e)}")

    return ""


def parse_hls_manifest(master_manifest_path: str) -> dict:
    manifest = {
        "width": 0,
        "height": 0,
        "bitrate_kb": 2000,
        "codec": "",
        "color_range": "sdr",
        "frame_rate": "",
        "drop_frame": False
    }
    try:
        with open(master_manifest_path, 'r') as hls_manifest_file:

            for line in hls_manifest_file.readlines():
                if line.startswith("#EXT-X-STREAM-INF"):
                    # For now, use the total stream bandwidth as the bitrate
                    bandwidth = re.search(r'BANDWIDTH=(\d+)', line).group(1)
                    manifest["bitrate_kb"] = int(bandwidth) // 1000

                    # Extract just the video codec
                    codecs = re.search(r'CODECS="([^"]+)"', line).group(1)
                    manifest["codec"] = codecs.split(",")[0]

                    # Extract the resolution
                    resolution = re.search(r'RESOLUTION=(\d+x\d+)', line).group(1)
                    manifest["width"] = int(resolution.split("x")[0])
                    manifest["height"] = int(resolution.split("x")[1])

                    # Extract the frame rate
                    frame_rate = re.search(r'FRAME-RATE=(\d+)', line)
                    manifest["frame_rate"] = frame_rate.group(1) + "000/1000"

                    return manifest
    except FileNotFoundError:
        print(f"Error: Master manifest file not found at {hls_manifest_file}")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in master manifest file at {hls_manifest_file}")
    except Exception as e:
        print(f"An unexpected error occurred with master manifest file {hls_manifest_file} :: {str(e)}")


def add_master_manifest(player_json: dict, template: dict) -> dict:
    hls_sources = template["sources"]["hls"]
    hls_dir = template["output"]["hls_dir"]

    for hls_source in hls_sources:
        hls_dir_pathname = os.path.join(hls_dir, hls_source["src"])

        # Find the master manifest file in the HLS ladder directory
        m3u8_manifest_filename = find_master_m3u8_manifest(hls_dir_pathname)

        manifest_entry = {
            "name": hls_source["display_name"],
            "id": hls_source["id"],
            "url": template["output"]["root_url"] + m3u8_manifest_filename
        }

        # Parse out just those values of interest from the master M3U8 manifest
        m3u8_manifest = parse_hls_manifest(m3u8_manifest_filename)

        manifest_entry["width"] = m3u8_manifest["width"]
        manifest_entry["height"] = m3u8_manifest["height"]
        manifest_entry["bitrate_kb"] = m3u8_manifest["bitrate_kb"]
        manifest_entry["codec"] = m3u8_manifest["codec"]
        manifest_entry["color_range"] = "sdr"
        manifest_entry["frame_rate"] = m3u8_manifest["frame_rate"]
        manifest_entry["drop_frame"] = False

        player_json["data"]["master_manifests"].append(manifest_entry)

    return player_json


def find_source_mezzanine(src_id: str, template: dict) -> dict:
    for source in template["sources"]["mezzanine"]:
        if source["id"] == src_id:
            return source
    return {}


def find_video_track_thumbnails(template: dict) -> str:
    thumbnails_dir = template["output"]["thumbnails_dir"]
    for filename in os.listdir(thumbnails_dir):
        filepath = os.path.join(thumbnails_dir, filename)

        if os.path.isfile(filepath) and filename.endswith(".vtt"):
            return filepath

    return ""


def get_analysis_track_name(filename: str) -> str:
    # Split the string based on "audio" or "video"
    if "audio" in filename:
        parts = filename.split("_audio")[0]
    elif "video" in filename:
        parts = filename.split("_video")[0]
    else:
        return ""

    # Remove underscores and capitalize each word
    return ' '.join(word.capitalize() for word in parts.split('_'))


def get_static_analysis_tracks(track_type: str, template: dict) -> list:
    analysis = []

    analysis_dir = template["output"]["analysis_dir"]

    for filename in os.listdir(analysis_dir):
        filepath = os.path.join(analysis_dir, filename)

        if os.path.isfile(filepath) and filename.endswith(".vtt") and track_type in filename:
            analysis_name = get_analysis_track_name(filename)

            if "marker" in filename:
                visualization = "marker"
            elif "point" in filename:
                visualization = "point"
            else:
                visualization = ""

            analysis_entry = {
                "name": analysis_name,
                "type": "events",
                "visualization": visualization,
                "url": template["output"]["root_url"] + filepath
            }

            analysis.append(analysis_entry)

    return analysis


def get_video_bitrate_analysis_track(template: dict) -> list:
    analysis = []
    video_source = find_source_mezzanine("V1", template)

    if video_source:
        video_filename = os.path.basename(video_source["src"])
        analysis_dir = template["output"]["analysis_dir"]
        filename_root = os.path.splitext(video_filename)[0]

        for filename in os.listdir(analysis_dir):
            filepath = os.path.join(analysis_dir, filename)

            if os.path.isfile(filepath) and filename.startswith(filename_root) and filename.endswith(".vtt"):
                analysis_entry = {
                    "name": "Bit Rate",
                    "type": "chart",
                    "visualization": "line",
                    "url": template["output"]["root_url"] + filepath
                }

                analysis.append(analysis_entry)

                break

    return analysis


def add_video_analysis_tracks(template: dict) -> list:
    static_tracks = get_static_analysis_tracks("video", template)
    bitrate_tracks = get_video_bitrate_analysis_track(template)

    return static_tracks + bitrate_tracks


def add_video_track(player_json: dict, template: dict) -> dict:
    for track in template["sources"]["tracks"]["video"]:
        text_track_mezzanine = find_source_mezzanine(track["source_id"], template)
        if not text_track_mezzanine:
            continue

        manifest_ids = []
        for hls in template["sources"]["hls"]:
            manifest_ids.append(hls["id"])

        thumbnails_path = find_video_track_thumbnails(template)

        visual_reference = [
            {
                "type": "thumbnails",
                "url": template["output"]["root_url"] + thumbnails_path
            }
        ]

        analysis = add_video_analysis_tracks(template)

        track_entry = {
            "name": os.path.basename(text_track_mezzanine["src"]),
            "source_id": track["source_id"],
            "manifest_ids": manifest_ids,
            "visual_reference": visual_reference,
            "analysis": analysis
        }

        player_json["data"]["media_tracks"]["video"].append(track_entry)

    return player_json


def find_audio_track_channel_waveform(program_name: str, template: dict) -> str:
    for filename in os.listdir(template["output"]["waveforms_dir"]):
        filepath = os.path.join(template["output"]["waveforms_dir"], filename)

        if os.path.isfile(filepath) and filename.endswith(".vtt") and program_name in filename:
            return filepath

    return ""


def add_audio_track_channel_waveforms(track_entry: dict, template: dict) -> dict:
    # Get a list of audio channels for the current sound field by parsing all m3u8 master manifests
    # channels = get_audio_track_channel_list(track_entry, template)

    # Get a list of audio channels for the current sound field by looking for the channel waveform files.
    channels = get_audio_waveform_channel_list(track_entry, template)

    for channel_id, program_name in channels.items():

        # Locate the waveform file for the current channel
        filepath = find_audio_track_channel_waveform(program_name, template)

        # If a waveform file was found, add it to the track entry
        if filepath:
            visual_reference_entry = {
                    "type": "waveform",
                    "url": template["output"]["root_url"] + filepath,
                    "channel": channel_id
            }
            track_entry["visual_reference"].append(visual_reference_entry)
            track_entry["channel_layout"] = " ".join(channels.keys())

    return track_entry

def get_audio_waveform_channel_list(track_entry: dict, template: dict) -> dict:
    """
    For the audio track passed, find the waveform files in the waveforms directory that match the program name.
    :param track_entry: a dict representing the current audio track entry in the player json.
    :param template: the omt manifest loaded as a dictionary.
    :return: a dictionary of { channel_id: program_name } pairs.
    """
    waveforms_dir = template["output"]["waveforms_dir"]
    channel_list = {}

    # Walk through the directory tree
    for dirpath, dirnames, filenames in os.walk(waveforms_dir):
        for file_name in filenames:
            try:
                # Program name as EN_20_L or EN_51_LFE as examples
                match = re.search(r'([A-Za-z]{2}_\d{2}_[A-Za-z]{1,3})', file_name)
                if match:
                    program_name = match.group(1)
                    # Channel for current sound field?
                    if track_entry["program_name"] in program_name:
                        parts = program_name.split('_')
                        # Only use program names for the channels, which should be "EN" "20" "L".
                        #   If just two parts, then it's the program name for the sound field
                        if len(parts) == 3:
                            channel_id = parts[-1]
                            channel_list[channel_id] = program_name
            except Exception as e:
                print(f"An unexpected error occurred with waveform file{file_name} :: {str(e)}")

    # Make sure the channels are in the right channel order.
    desired_order = ['L', 'R', 'C', 'LFE', 'LS', 'RS']
    sorted_channel_list = {k: v for k, v in sorted(channel_list.items(), key=lambda kv: desired_order.index(kv[0]))}

    return sorted_channel_list

def get_audio_track_channel_list(track_entry: dict, template: dict) -> dict:
    """
    For each audio sound field, there may be a separate audio program for each channel in the ABR ladder.
    Search the m3u8 manifest file for each ABR ladder in the HLS directory and find audio programs that match
    the sound filed program name, but appended with a channel ID.
    :param track_entry: a dict representing the current audio track entry in the player json.
    :param template: the omt manifest loaded as a dictionary.
    :return: a dictionary of { channel_id: program_name } pairs.
    """
    hls_dir = template["output"]["hls_dir"]
    channel_list = {}

    # Walk through the directory tree
    for dirpath, dirnames, filenames in os.walk(hls_dir):
        for dir_name in dirnames:
            try:
                m3u8_pathname = find_master_m3u8_manifest(str(os.path.join(dirpath, dir_name)))

                if m3u8_pathname:
                    with open(m3u8_pathname, 'r') as m3u8_manifest_file:
                        for line in m3u8_manifest_file.readlines():
                            if line.startswith("#EXT-X-MEDIA:TYPE=AUDIO"):
                                # Program name as EN_20_L or EN_51_LFE as examples
                                program_name = re.search(r'NAME="([^"]+)"', line).group(1)
                                if program_name:
                                    # Channel for current sound field?
                                    if track_entry["program_name"] in program_name:
                                        parts = program_name.split('_')
                                        # Only use program names for the channels, which should be "EN" "20" "L".
                                        #   If just two parts, then it's the program name for the sound field
                                        if len(parts) == 3:
                                            channel_id = parts[-1]
                                            channel_list[channel_id] = program_name
            except FileNotFoundError:
                print(f"Error: M3u8 manifest file not found at {m3u8_manifest_file}")
            except json.JSONDecodeError:
                print(f"Error: Invalid JSON in m3u8 manifest file at {m3u8_manifest_file}")
            except Exception as e:
                print(f"An unexpected error occurred with m3u8 manifest file{m3u8_manifest_file} :: {str(e)}")

    return channel_list


def add_audio_metric_tracks(track_entry: dict, template: dict) -> list:
    analysis = []

    analysis_dir = template["output"]["analysis_dir"]
    rms_analysis = track_entry["program_name"] + "_RMS"
    r128_analysis = track_entry["program_name"] + "_R128"

    for filename in os.listdir(analysis_dir):
        filepath = os.path.join(analysis_dir, filename)

        if os.path.isfile(filepath) and filename.endswith(".vtt"):
            if rms_analysis in filename:
                analysis_entry = {
                    "name": "RMS Levels",
                    "type": "chart",
                    "visualization": "line",
                    "url": template["output"]["root_url"] + filepath
                }
                analysis.append(analysis_entry)

                analysis_entry = {
                    "name": "Overall RMS Levels",
                    "type": "chart",
                    "visualization": "led",
                    "y_min": -100,
                    "y_max": 0,
                    "scale": "linear",
                    "url": template["output"]["root_url"] + filepath
                }
                analysis.append(analysis_entry)

            elif r128_analysis in filename:
                analysis_entry = {
                    "name": "EBU R128 M",
                    "type": "chart",
                    "visualization": "bar",
                    "y_min": -100,
                    "y_max": 0,
                    "scale": "linear",
                    "url": template["output"]["root_url"] + filepath
                }
                analysis.append(analysis_entry)

    return analysis


def add_audio_analysis_tracks(track_entry: dict, template: dict) -> dict:
    static_tracks = get_static_analysis_tracks("audio", template)
    metric_tracks = add_audio_metric_tracks(track_entry, template)
    track_entry["analysis"] = static_tracks + metric_tracks

    return track_entry


def add_audio_track(player_json: dict, template: dict) -> dict:
    for track in template["sources"]["tracks"]["audio"]:
        text_track_mezzanine = find_source_mezzanine(track["source_id"], template)
        if not text_track_mezzanine:
            continue

        track_entry = {
            "name": f'{os.path.basename(text_track_mezzanine["src"])} ({track["display_text"]})',
            "source_id": track["source_id"],
            "program_name": track["program_name"],
            "channel_layout": "",
            "language": "eng",
            "visual_reference": [],
            "analysis": []
        }

        track_entry = add_audio_track_channel_waveforms(track_entry, template)

        track_entry = add_audio_analysis_tracks(track_entry, template)

        player_json["data"]["media_tracks"]["audio"].append(track_entry)

    return player_json


def add_text_tracks(player_json: dict, template: dict) -> dict:
    for track in template["sources"]["tracks"]["text"]:
        text_track_mezzanine = find_source_mezzanine(track["source_id"], template)
        if not text_track_mezzanine:
            continue

        track_entry = {
            "name": f'{os.path.basename(text_track_mezzanine["src"])} ({track["display_text"]})',
            "source_id": track["source_id"],
            "program_name": track["program_name"],
            "language": "eng",
        }

        player_json["data"]["media_tracks"]["text"].append(track_entry)

    return player_json


def add_media_tracks(player_json: dict, template: dict) -> dict:
    player_json["data"]["media_tracks"] = {
        "video": [],
        "audio": [],
        "text": []
    }

    player_json = add_video_track(player_json, template)
    player_json = add_audio_track(player_json, template)
    player_json = add_text_tracks(player_json, template)

    return player_json


def load_metadata(metadata_file: str) -> dict:
    metadata = {}

    # If full path has not been provided,
    if not Path(metadata_file).exists():
        # Look in default 'sources' directory
        metadata_file = os.path.join("sources", metadata_file)
        # If still not found, return empty metadata
        if not Path(metadata_file).exists():
            print(f"Error: Media manifest file not found at {metadata_file}")
            return metadata

    try:
        with open(metadata_file, 'r') as media_manifest_file:
            metadata = json.load(media_manifest_file)
    except FileNotFoundError:
        print(f"Error: Media manifest file not found at {metadata_file}")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in media manifest file at {metadata_file}")
    except Exception as e:
        print(f"An unexpected error occurred with {metadata_file} :: {str(e)}")

    return metadata


def add_presentation(player_json: dict, template: dict) -> dict:
    # Create an empty presentation object
    player_json["presentation"] = {}
    player_json["presentation"]["layout"] = {}
    player_json["presentation"]["info_tabs"] = []
    player_json["presentation"]["timeline_configuration"] = {}
    player_json["presentation"]["segmentation_actions"] = []

    if "src" not in template["sources"]["metadata"][0]:
        return player_json

    metadata_path = template["sources"]["metadata"][0]["src"]

    if "display_name" not in template["sources"]["metadata"][0]:
        display_name = os.path.splitext(os.path.basename(metadata_path))[0]
    else:
        display_name = template["sources"]["metadata"][0]["display_name"]

    metadata = load_metadata(metadata_path)

    new_info_tab = {
        "name": display_name,
        "type": "json",
        "visualization": "json_tree",
        "data": {
            os.path.splitext(os.path.basename(metadata_path))[0]: metadata
        }
    }

    player_json["presentation"]["info_tabs"].append(new_info_tab)

    return player_json


def create_player_json_from_template(template: dict) -> dict:
    player_json = {}

    # Add a version stub
    add_version(player_json, template)
    
    # Add a security token stub
    add_session(player_json, template)

    player_json["data"] = {
        "source_info": [],
        "media_info": [],
        "master_manifests": [],
        "media_tracks": {}
    }

    # Add source info
    player_json = add_source_info(player_json, template)

    # Add media info
    player_json = add_media_info(player_json, template)

    # Add master manifest
    player_json = add_master_manifest(player_json, template)

    # Add media tracks
    player_json = add_media_tracks(player_json, template)

    # Add presentation
    player_json = add_presentation(player_json, template)

    return player_json


def load_template(template_path) -> dict:
    """
    Load the template player json file into a dictionary
    :param template_path: Path to the template player json file
    :return: Dictionary containing the template player json file
    """
    template = {}
    try:
        with open(template_path, 'r') as template_file:
            template = json.load(template_file)
    except FileNotFoundError:
        print(f"Error: Template file not found at {template_path}")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in template file at {template_path}")
    except Exception as e:
        print(f"An unexpected error occurred with {template_file} :: {str(e)}")
    return template


def create_output_dir_structure(template) -> bool:
    # Ensure all output directories exist
    root_dir = template["output"]["root_dir"]
    hls_dir = os.path.join(root_dir, "hls")
    analysis_dir = os.path.join(root_dir, "analysis")
    thumbnails_dir = os.path.join(root_dir, "thumbnails")
    waveform_dir = os.path.join(root_dir, "waveforms")

    try:
        if not os.path.exists(root_dir):
            os.makedirs(root_dir)
    except PermissionError:
        print(f"Error: OMT does not have permissions to create root player json directory {root_dir}")
        print("Change folder permissions or target folder and try again!")
        return False
    except Exception as e:
        print(f"An unexpected error occurred creating root player json directory {root_dir} :: {str(e)}")
        return False

    try:
        if not os.path.exists(hls_dir):
            os.makedirs(hls_dir)
    except PermissionError:
        print(f"Error: OMT does not have permissions to create hls directory {hls_dir}")
        print("Change folder permissions or target folder and try again!")
        return False
    except Exception as e:
        print(f"An unexpected error occurred creating hls directory {hls_dir} :: {str(e)}")
        return False

    try:
        if not os.path.exists(analysis_dir):
            os.makedirs(analysis_dir)
    except PermissionError:
        print(f"Error: OMT does not have permissions to create analysis directory {analysis_dir}")
        print("Change folder permissions or target folder and try again!")
        return False
    except Exception as e:
        print(f"An unexpected error occurred creating analysis directory {analysis_dir} :: {str(e)}")
        return False

    try:
        if not os.path.exists(thumbnails_dir):
            os.makedirs(thumbnails_dir)
    except PermissionError:
        print(f"Error: OMT does not have permissions to create thumbnails directory {thumbnails_dir}")
        print("Change folder permissions or target folder and try again!")
        return False
    except Exception as e:
        print(f"An unexpected error occurred creating thumbnails directory {thumbnails_dir} :: {str(e)}")
        return False

    try:
        if not os.path.exists(waveform_dir):
            os.makedirs(waveform_dir)
    except PermissionError:
        print(f"Error: OMT does not have permissions to create waveform directory {waveform_dir}")
        print("Change folder permissions or target folder and try again!")
        return False
    except Exception as e:
        print(f"An unexpected error occurred creating waveform directory {waveform_dir} :: {str(e)}")
        return False

    return True


def add_output_defaults(template) -> bool:
    # Either the player json filename or the root directory of the output must be specified.
    if ("player_json" not in template.get("output", {})) & ("root_dir" not in template.get("output", {})):
        print("Error: Template must include either \".output.root_dir\" or \".output.player_json\"")
        return False

    if "player_json" not in template.get("output", {}):
        template.setdefault("output", {})["player_json"] = template["output"]["root_dir"] + ".json"

    if "sources_dir" not in template.get("output", {}):
        template.setdefault("output", {})["sources_dir"] = "sources"

    if "root_dir" not in template.get("output", {}):
        template.setdefault("output", {})["root_dir"] = template["output"]["player_json"].replace(".json", "")

    if "root_url" not in template.get("output", {}):
        template.setdefault("output", {})["root_url"] = "https://localhost:8080/"

    if "hls_dir" not in template.get("output", {}):
        template.setdefault("output", {})["hls_dir"] = os.path.join(template["output"]["root_dir"], "hls")

    if "analysis_dir" not in template.get("output", {}):
        template.setdefault("output", {})["analysis_dir"] = os.path.join(template["output"]["root_dir"], "analysis")

    if "thumbnails_dir" not in template.get("output", {}):
        template.setdefault("output", {})["thumbnails_dir"] = os.path.join(template["output"]["root_dir"], "thumbnails")

    if "waveforms_dir" not in template.get("output", {}):
        template.setdefault("output", {})["waveforms_dir"] = os.path.join(template["output"]["root_dir"], "waveforms")

    return True


def setup_player_json_args(subparsers):
    player_json_parser = subparsers.add_parser('player-json', aliases=['p'], help='create OMP player JSON')

    player_json_parser.add_argument("-v", "--verbose", help="enable verbose output", action="store_true")
    player_json_parser.add_argument("-t", "--template", help="path to the template file", required=True)
    player_json_parser.set_defaults(func=create_player_json)


def create_player_json(args: Namespace):
    if Path(args.template).exists() is False:
        print(f"input file {args.template} does not exist.")
        return

    if args.verbose:
        print(f"creating player json from template: input \'{args.template}\'")

    template = load_template(args.template)

    # Add any missing template inputs from defaults
    add_output_defaults(template)

    # Create output directory structure if missing
    dirs_created = create_output_dir_structure(template)

    # If directory creation failed return
    if not dirs_created:
        print("directory creation failed ... exiting")
        return

    omp_player_json = create_player_json_from_template(template)

    player_json_pathname = template["output"]["root_dir"] + "/" + template["output"]["player_json"]
    try:
        with open(player_json_pathname, "w") as omp_player_file:
            json.dump(omp_player_json, omp_player_file, indent=4)
    except FileNotFoundError:
        print(f"Error: Omp player file not found at {omp_player_file}")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in OMP player file at {omp_player_file}")
    except Exception as e:
        print(f"An unexpected error occurred with OMP player file {omp_player_file} :: {str(e)}")

    if args.verbose:
        print(f"OMP player json file created at {player_json_pathname}")
