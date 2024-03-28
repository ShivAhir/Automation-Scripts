import os
import subprocess
import json



def get_video_codec(file_path):
    try:
        
        command = [
            'ffprobe',
            '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=codec_name',
            '-of', 'json',
            file_path
        ]

        
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        
        output = json.loads(result.stdout)

        codec = output['streams'][0]['codec_name']
        return codec
    except Exception as e:
        print(f"Error getting codec for file {file_path}: {e}")
        return None


ts_files = [
    'C:/Users/sahir/Documents/MPEG2-HD',

]

for file_path in ts_files:
    codec = get_video_codec(file_path)
    if codec:
        print(f"File: {file_path}, Codec: {codec}")