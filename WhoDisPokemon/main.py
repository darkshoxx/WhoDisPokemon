import os

import cv2
from PIL import Image

from WhoDisPokemon.audio import create_answer_video, create_question_video

# Folder Names
HERE = os.path.abspath(os.path.dirname(__file__))
SPRITE_FOLDER = os.path.join(HERE, "pokemon_sprites")
OUTPUT = os.path.join(HERE, "output")
# File Names
POKE_LOG = os.path.join(HERE, "pokelog.txt")
WTP_ANSWER_TEMPLATE = os.path.join(HERE, "WTP_answer.wav")
TTS_FILES_FOLDER = os.path.join(HERE, "generated_tts_files")
OUTPUT_QUESTION = os.path.join(OUTPUT, "question.mp4")
OUTPUT_ANSWER = os.path.join(OUTPUT, "answer.mp4")
WTP_RAW = os.path.join(HERE, "WTP.mp4")
WTP_START = os.path.join(HERE, "WTP_start.mp4")
WTP_QUESTION = os.path.join(HERE, "WTP_question.mp4")
WTP_ANSWER = os.path.join(HERE, "WTP_answer.mp4")
WTP_ANSWER_NAME_VIDEO = os.path.join(HERE, "WTP_answer_name_video.mp4")

# Mask colour as RGB and BGR
NEWCOLOUR = (50, 100, 200, 255)
NEWCOLOUR3 = (NEWCOLOUR[2], NEWCOLOUR[1], NEWCOLOUR[0])

# Target dimensions of sprite
TARGET_W = 300
TARGET_H = 300


def make_transparent_image(dex):
    # get sprite of pokemon with pokedex dex
    image_path = os.path.join(SPRITE_FOLDER, f"{dex}.png")
    save_path = os.path.join(HERE, "wtp.png")
    # resize and make mask image
    with Image.open(image_path) as current_image_object:
        rgba_object = current_image_object.convert("RGBA").resize(
            (TARGET_W, TARGET_H)
            )
        rgba_image = rgba_object.load()

        for wpixel in range(TARGET_W):
            for hpixel in range(TARGET_H):
                if (rgba_image[wpixel, hpixel][3] == 0):
                    rgba_image[wpixel, hpixel] = (0, 0, 0, 0)
                else:
                    rgba_image[wpixel, hpixel] = NEWCOLOUR
        rgba_object.save(save_path)


def generate_video_files(pokedex: int):
    # get original and masked image paths
    source_image_path = os.path.join(SPRITE_FOLDER, f"{pokedex}.png")
    transparent_image_path = os.path.join(HERE, "wtp.png")
    # create capture object, start three video writer objects
    cap = cv2.VideoCapture(WTP_RAW)
    start_frame = 20
    end_frame = 255
    frame_counter = 1
    ret, frame = cap.read()
    file_writer_start = cv2.VideoWriter(WTP_START, -1, 30.0, (1280, 720))
    file_writer_question = cv2.VideoWriter(WTP_QUESTION, -1, 30.0, (1280, 720))
    file_writer_answer = cv2.VideoWriter(WTP_ANSWER, -1, 30.0, (1280, 720))

    # load images
    with Image.open(transparent_image_path) as current_image_object:
        rgba_object = current_image_object.convert("RGBA").resize(
            (TARGET_W, TARGET_H)
            )
        rgba_image = rgba_object.load()
    with Image.open(source_image_path) as current_image_object:
        orig_rgba_object = current_image_object.convert("RGBA").resize(
            (TARGET_W, TARGET_H)
            )
        orig_rgba_image = orig_rgba_object.load()

    while ret:
        # create question part of video
        if end_frame > frame_counter > start_frame:
            for wpixel in range(TARGET_W):
                for hpixel in range(TARGET_H):
                    if (rgba_image[hpixel, wpixel][3] != 0):
                        frame[wpixel+180, hpixel+200] = NEWCOLOUR3
            file_writer_question.write(frame)
        elif frame_counter >= end_frame:
            # create answer part of video
            for wpixel in range(TARGET_W):
                for hpixel in range(TARGET_H):
                    orig_r, orig_g, orig_b, orig_a = orig_rgba_image[
                        hpixel,
                        wpixel
                    ]
                    if (orig_a != 0):
                        frame[wpixel+180, hpixel+200] = orig_b, orig_g, orig_r
            file_writer_answer.write(frame)
        else:
            # create start of video
            file_writer_start.write(frame)
        ret, frame = cap.read()
        frame_counter += 1

    cap.release()
    file_writer_answer.release()
    file_writer_question.release()
    file_writer_start.release()


def get_tts_path(pokedex: int) -> str:
    # convert pokedex number to TTS filepath
    start_string = f"{pokedex}_"
    start_string_length = len(start_string)
    for file in os.listdir(TTS_FILES_FOLDER):
        if file[:start_string_length] == start_string:
            return os.path.join(TTS_FILES_FOLDER, file)


def prepare_question(dex, output_file=OUTPUT_QUESTION):
    # convenience function turning dex into question video
    make_transparent_image(dex)
    generate_video_files(dex)
    create_question_video(output_file)


def prepare_answer(dex, output_file=OUTPUT_ANSWER):
    # convenience function turning dex into answer video
    pokename_path = get_tts_path(dex)
    create_answer_video(
        bg_path=WTP_ANSWER_TEMPLATE,
        pokename_path=pokename_path,
        video_path=WTP_ANSWER,
        export_path=output_file
    )


if __name__ == "__main__":

    dex = 120
    prepare_question(dex)
    prepare_answer(dex)

    # ##  Overnight test run to find errors in video generation (case 678)

    # with open(POKE_LOG, "r") as log_file:
    #     lines = log_file.readlines()
    # for line in lines:
    #     if line != "":
    #         num, sig = line.split(" ")
    #         if sig == "-\n":
    #             print(num)
