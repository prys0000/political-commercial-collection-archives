import os
import subprocess

# Path to the FFMpeg executable
ffmpeg_path = 'path_to_ffmpeg_executable'

# Path to the input MPEG video directory
input_directory = 'path_to_input_mpeg_videos'

# Path to the output MP4 video directory
output_directory = 'path_to_output_mp4_videos'

# Path to the watermark image file
watermark_file = 'path_to_watermark_image'

# Loop through all the MPEG videos in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith('.mpeg'):
        # Input and output file paths
        input_file = os.path.join(input_directory, filename)
        output_file = os.path.join(output_directory, os.path.splitext(filename)[0] + '.mp4')

        # FFMpeg command for conversion with watermark
        command = [ffmpeg_path, '-i', input_file, '-i', watermark_file, '-filter_complex',
                   'overlay=W-w-10:H-h-10', '-c:v', 'libx264', '-c:a', 'copy', output_file]

        # Execute the FFMpeg command
        subprocess.run(command)

print('Conversion completed.')
