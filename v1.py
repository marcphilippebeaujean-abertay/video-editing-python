import numpy as np
from moviepy.editor import VideoFileClip, concatenate

clip = VideoFileClip("intro.mp4")

get_clip_audio_at_second = lambda second: clip.audio.subclip(second, second + 1).to_soundarray(fps=22000)
get_audio_volume = lambda audio: np.sqrt(((1.0 * audio) ** 2).mean())

volumes = [get_audio_volume(get_clip_audio_at_second(i)) for i in range(0, int(clip.duration - 1))]

clip_seconds_to_remove = []

average_clip_volume = sum(volumes) / clip.duration

is_quiet_clip = lambda volume_val: volume_val < (average_clip_volume * 0.8)

for i in range(1, int(clip.duration - 2)):
    # check if there is a quiet section
    # and is_quiet_clip(volumes[i - 1]) and is_quiet_clip(volumes[i + 1]):
    if is_quiet_clip(volumes[i]):
        clip_seconds_to_remove.append(i)

main_clips = []
last_second_clip_starts_from = 0

seconds_in_final_video = [second for second in range(0, int(clip.duration - 1))
                          if second not in clip_seconds_to_remove]

final_video_clip = concatenate([clip.subclip(max(0, second), min(second + 1, clip.duration))
                               for second in seconds_in_final_video])
final_video_clip.to_videofile('cut_video1.mp4')
