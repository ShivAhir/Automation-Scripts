import os
import subprocess
import json
from collections import defaultdict



# your directory containing the .ts files from which you want to find your desired stream
directory = r'C:\Users\sahir\Documents\MPEG2-HD'
listOfStreams = []
codec_type = (input("Enter the desired codec type - Audio/Video/Subtitle: ")).lower().strip()
if codec_type == 'audio':
    codec_name = (input("Enter the desired codec_name (ac3/mp2): ")).lower().strip()
    bits = int((input("Enter the desired bits(20): ")).strip())
elif codec_type == 'video':
    resolution = (input("Enter the desired resolution (SD/HD): ")).upper().strip()
    codec_name = (input("Enter the desired codec_name (mpeg2video/h264): ")).lower().strip()
    pix_format = (input("Enter the desired pixel format (yuv420p/yuv422p): ")).lower().strip()
else:
    codec_name = (input("Enter the desired codec_name (dvb_subtitle/dvb_teletext): ")).lower().strip()
print(" ")

def get_codec_info(file_path):
    try:
        # capturing the output
        ffprobe_cmd = [
            'ffprobe',
            '-v', 'error',
            '-print_format', 'json',
            '-show_streams',
            file_path
        ]
        result = subprocess.run(ffprobe_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # parsing the JSON output from ffprobe
        info = json.loads(result.stdout)

        # for debugging
        print(json.dumps(info, indent=4))

        # extracting the codec names for each stream
        video_info = []
        for stream in info['streams']:
            if stream['codec_type'] == 'video':    
                if 'codec_name' in stream and 'width' in stream and 'height' in stream and 'r_frame_rate' in stream:
                    video_info.append({
                        'codec_type': stream['codec_type'],
                        'codec_name': stream['codec_name'],
                        'width': stream["width"],
                        'height': stream["height"],
                        'resolution': 'HD' if stream['width'] >= 1280 and stream['height'] >= 720 else 'SD',
                        'frame_rate': stream['r_frame_rate'],
                        'pix_fmt': stream['pix_fmt'],
                    })
            elif stream['codec_type'] == 'audio':
                video_info.append({
                    'codec_type': stream['codec_type'],
                    'codec_name': stream['codec_name'],
                    'bits_per_sample': stream['bits_per_sample']
                })
            elif stream['codec_type'] == 'subtitle':
                video_info.append({
                    'codec_type': stream['codec_type'],
                    'codec_name': stream['codec_name']
                })
        return video_info

    except Exception as e:
        print(f"An error occurred while processing file {file_path}: {e}")
        return None

for filename in os.listdir(directory):
    if filename.endswith('.ts'):
        file_path = os.path.join(directory, filename)
        print(f"Processing file: {filename} on location: {directory}")
        video_info = get_codec_info(file_path)
        if video_info:
            for info in video_info:
                if info['codec_type'] == 'audio':
                    if info['codec_name'] == codec_name:
                        listOfStreams.append({
                                'stream_name': filename,
                                'codec_type': info['codec_type'],
                                'codec_name': info['codec_name'],
                                'bits_per_sample': info['bits_per_sample'],
                        })
                elif info.get('codec_type') == 'video':
                    listOfStreams.append({
                                'stream_name': filename,
                                'codec_type': info['codec_type'],
                                'codec_name': info['codec_name'],
                                'resolution': info['resolution'],
                                'frame_rate': info['frame_rate'],
                                'pix_fmt': info['pix_fmt'],
                            })
                else:
                    listOfStreams.append({
                                'stream_name': filename,
                                'codec_type': info['codec_type'],
                                'codec_name': info['codec_name'],
                            })
        else:
            print("Codec information could not be retrieved.")

def addNumberOfChannels(streams):
    channel = defaultdict(int)
    
    for entry in streams:
        key = tuple(sorted(entry.items()))
        channel[key] += 1
    result = []
    for key, count in channel.items():
        entry_dict = dict(key)
        entry_dict['channel'] = count
        result.append(entry_dict)
    return result


if listOfStreams:
    print(" ")
    print(" ")
    print("List of streams")
    result = addNumberOfChannels(listOfStreams)
    if result:
        for stream in result:
            if codec_type == 'video':  
                if stream['codec_name'] == codec_name and stream['resolution'] == resolution and stream['pix_fmt'] == pix_format:
                    print(stream)
            elif codec_type == 'audio':
                if 'bits_per_sample' in stream and (stream['bits_per_sample'] == bits):
                    print(stream)
            elif codec_type == 'subtitle':
                if stream['codec_name'] == codec_name:
                    print(stream)
            
    else:
        print(" No streams found according to your requirement!") 
