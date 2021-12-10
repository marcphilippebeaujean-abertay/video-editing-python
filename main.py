import os
from edit_video import process_video_from_filename

input_path = os.path.join(os.getcwd(), 'input')
input_videos = os.listdir(input_path)

output_path = os.path.join(os.getcwd(), 'output')

processed_path = os.path.join(os.getcwd(), 'processed')

for video_filename in input_videos:
    full_video_path = os.path.join(input_path, video_filename)
    video_in_memory = process_video_from_filename(full_video_path)
    video_in_memory.to_videofile(os.path.join(output_path, video_filename + '-processed.mp4'))
    os.replace(full_video_path, os.path.join(processed_path, video_filename))


