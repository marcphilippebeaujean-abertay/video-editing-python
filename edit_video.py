import numpy as np
from moviepy.editor import VideoFileClip, concatenate

CLIP_DURATION_MULTIPLIER = 10


def process_video_from_filename(video_filename):
    clip = VideoFileClip(video_filename)

    clip_duration_multiplied = clip.duration * CLIP_DURATION_MULTIPLIER

    def get_clip_audio_for_second(second):
        subclip_start = second / CLIP_DURATION_MULTIPLIER
        subclip_end = subclip_start + (1 / CLIP_DURATION_MULTIPLIER)
        return clip.audio.subclip(subclip_start, subclip_end).to_soundarray(fps=22000)

    def get_audio_clip_avg_volume(audio_clip):
        return np.sqrt(((1.0 * audio_clip) ** 2).mean())

    volumes = [get_audio_clip_avg_volume(get_clip_audio_for_second(i))
               for i in range(0, int(clip_duration_multiplied - 1))]

    average_clip_volume = sum(volumes) / clip_duration_multiplied

    def is_speaking_in_clip(clip_volume):
        return clip_volume > (average_clip_volume * 0.3)

    current_subclip_starting_point = 0
    current_subclip_ending_point = 0

    final_video_subclips = []

    SILENCE_BUFFER = 4

    for i in range(0, int(clip_duration_multiplied) - 1):
        if i <= current_subclip_ending_point:
            continue
        # check if current clip is loud clip
        if is_speaking_in_clip(volumes[i]):
            # if it is, set clip endpoint to this one
            current_subclip_ending_point = i
        elif current_subclip_ending_point == current_subclip_starting_point:
            current_subclip_starting_point = i
            current_subclip_ending_point = i
        elif (i - current_subclip_ending_point) >= SILENCE_BUFFER:
            subclip_buffer = SILENCE_BUFFER / 2
            new_clip_start = ((current_subclip_starting_point - subclip_buffer) / CLIP_DURATION_MULTIPLIER)
            new_clip_end = ((i - subclip_buffer) / CLIP_DURATION_MULTIPLIER)

            subclip_for_final_video = clip.subclip(max(0, new_clip_start), min(new_clip_end, clip.duration))

            final_video_subclips.append(subclip_for_final_video)

            current_subclip_starting_point = i
            current_subclip_ending_point = i

    return concatenate(final_video_subclips)
