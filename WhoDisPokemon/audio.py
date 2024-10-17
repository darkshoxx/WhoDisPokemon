import os

import moviepy.editor as mpe
from pydub import AudioSegment

HERE = os.path.abspath(os.path.dirname(__file__))
WTP_ANSWER = os.path.join(HERE, "WTP_answer.wav")
TEMP_PATH = os.path.join(HERE, "WTP_TEMP.wav")
WTP_ANSWER_VID = os.path.join(HERE, "WTP_answer.mp4")
WTP_START = os.path.join(HERE, "WTP_start.wav")
WTP_START_VID = os.path.join(HERE, "WTP_start.mp4")
WTP_QUESTION = os.path.join(HERE, "WTP_question.wav")
WTP_QUESTION_VID = os.path.join(HERE, "WTP_question.mp4")
WTP_QUESTION_VIDEO_AUDIO = os.path.join(HERE, "WTP_question_complete.mp4")
WTP_QUESTION_FULL = os.path.join(HERE, "WTP_question_complete_full.mp4")
WTP_START_VIDEO_AUDIO = os.path.join(HERE, "WTP_start_complete.mp4")
WTP_ANSWER_NAME = os.path.join(HERE, "WTP_answer_name.wav")
WTP_ANSWER_NAME_VIDEO = os.path.join(HERE, "WTP_answer_name_video.mp4")
WTPIKACHU = os.path.join(HERE, "WTPIKACHU.wav")

## Adding the pokemon name to the soundfile
def add_name_to_video(bg_path, pokename_path, export_path):
    background = AudioSegment.from_file(bg_path, format="wav")
    pokename = AudioSegment.from_file(pokename_path, format="mp3")

    overlay = background.overlay(pokename, position=1500)

    overlay.export(export_path, format="wav")

## combining sound and videofile
def combine_audio_and_video(video_path=WTP_ANSWER_VID, audio_path=WTP_ANSWER_NAME, export_path =WTP_ANSWER_NAME_VIDEO):
    video_clip = mpe.VideoFileClip(video_path)
    start, end = video_clip.start, video_clip.end
    audio_clip = mpe.AudioFileClip(audio_path).subclip(start, end)
    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(export_path)

def create_answer_video(bg_path, pokename_path, video_path, export_path):
    add_name_to_video(bg_path, pokename_path, TEMP_PATH)
    combine_audio_and_video(video_path, TEMP_PATH, export_path)

def combine_start_and_question(export_path):
    start = mpe.VideoFileClip(WTP_START_VIDEO_AUDIO)
    question = mpe.VideoFileClip(WTP_QUESTION_VIDEO_AUDIO)
    full_question = mpe.concatenate_videoclips([start, question])
    full_question.write_videofile(export_path)

def create_question_video(export_path):
    combine_audio_and_video(WTP_START_VID, WTP_START, WTP_START_VIDEO_AUDIO)
    combine_audio_and_video(WTP_QUESTION_VID, WTP_QUESTION, WTP_QUESTION_VIDEO_AUDIO)
    combine_start_and_question(export_path)

if __name__ == "__main__":
    create_question_video(WTP_QUESTION_FULL)
    create_answer_video(bg_path = WTP_ANSWER, pokename_path = WTPIKACHU, video_path=WTP_ANSWER_VID, export_path=WTP_ANSWER_NAME_VIDEO)
