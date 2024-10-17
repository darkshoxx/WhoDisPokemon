import os

from PIL import Image

from WhoDisPokemon.audio import create_answer_video, create_question_video

POKE_LOG = r"C:\Code\GithubRepos\who_dis_pokemon\WhoDisPokemon\pokelog.txt"

HERE = os.path.abspath(os.path.dirname(__file__))
WTP_ANSWER_TEMPLATE = os.path.join(HERE, "WTP_answer.wav")
TTS_FILES_FOLDER = os.path.join(HERE, "generated_tts_files")
OUTPUT = os.path.join(HERE, "output")
OUTPUT_QUESTION = os.path.join(OUTPUT, "question.mp4")
OUTPUT_ANSWER = os.path.join(OUTPUT, "answer.mp4")
WTP_RAW = os.path.join(HERE, "WTP.mp4")
WTP_START = os.path.join(HERE, "WTP_start.mp4")
WTP_QUESTION = os.path.join(HERE, "WTP_question.mp4")
WTP_ANSWER = os.path.join(HERE, "WTP_answer.mp4")

WTP_ANSWER_NAME_VIDEO = os.path.join(HERE, "WTP_answer_name_video.mp4")
SPRITE_FOLDER = os.path.join(HERE, "pokemon_sprites")
NEWCOLOUR = (50, 100, 200, 255)
NEWCOLOUR3 = (NEWCOLOUR[2], NEWCOLOUR[1], NEWCOLOUR[0])
TARGET_W = 300
TARGET_H = 300

def make_transparent_image(dex):
    image_path = os.path.join(SPRITE_FOLDER, f"{dex}.png")
    save_path = os.path.join(HERE, "wtp.png")
    with Image.open(image_path) as current_image_object:
        width, height = current_image_object.size
        # alpha_channel = current_image_object.getchannel("A")
        print(current_image_object.has_transparency_data)
        # print(dir(current_image_object))
        RGBA_object = current_image_object.convert("RGBA").resize((TARGET_W,TARGET_H))
        RGBA_image = RGBA_object.load()
        # current_image = current_image_object.load()

        for wpixel in range(TARGET_W):
            for hpixel in range(TARGET_H):
                if(RGBA_image[wpixel,hpixel][3]==0):
                    RGBA_image[wpixel,hpixel] = (0,0,0,0)
                else:
                    RGBA_image[wpixel,hpixel] = NEWCOLOUR
        RGBA_object.save(save_path)

import cv2


def generate_video_files(pokedex:int):
    source_image_path = os.path.join(SPRITE_FOLDER, f"{pokedex}.png")
    transparent_image_path = os.path.join(HERE, "wtp.png")
    cap = cv2.VideoCapture(WTP_RAW)
    STARTFRAME = 20
    ENDFRAME = 255
    frame_counter = 1
    ret, frame = cap.read()
    file_writer_start = cv2.VideoWriter(WTP_START,-1,30.0,(1280,720))
    file_writer_question = cv2.VideoWriter(WTP_QUESTION,-1,30.0,(1280,720))
    file_writer_answer = cv2.VideoWriter(WTP_ANSWER,-1,30.0,(1280,720))

    with Image.open(transparent_image_path) as current_image_object:
        RGBA_object = current_image_object.convert("RGBA").resize((TARGET_W,TARGET_H))
        RGBA_image = RGBA_object.load()

    with Image.open(source_image_path) as current_image_object:
        ORIG_RGBA_object = current_image_object.convert("RGBA").resize((TARGET_W,TARGET_H))
        ORIG_RGBA_image = ORIG_RGBA_object.load()

    while ret:
        if ENDFRAME > frame_counter > STARTFRAME:
            for wpixel in range(TARGET_W):
                for hpixel in range(TARGET_H):
                    if(RGBA_image[hpixel, wpixel][3]!=0):
                        frame[wpixel+180,hpixel+200] = NEWCOLOUR3
            file_writer_question.write(frame)
        elif frame_counter >= ENDFRAME:
            for wpixel in range(TARGET_W):
                for hpixel in range(TARGET_H):
                    orig_R, orig_G, orig_B, orig_A = ORIG_RGBA_image[hpixel, wpixel]
                    if(orig_A!=0):
                        frame[wpixel+180,hpixel+200] = orig_B, orig_G, orig_R
            file_writer_answer.write(frame)
        else:
            file_writer_start.write(frame)
        ret, frame = cap.read()
        frame_counter += 1

    cap.release()
    file_writer_answer.release()
    file_writer_question.release()
    file_writer_start.release()

def get_tts_path(pokedex:int)->str:
    start_string = f"{pokedex}_"
    start_string_length = len(start_string)
    for file in os.listdir(TTS_FILES_FOLDER):
        if file[:start_string_length] == start_string:
            return os.path.join(TTS_FILES_FOLDER, file)



def prepare_question(dex, output_file=OUTPUT_QUESTION):
    make_transparent_image(dex)
    generate_video_files(dex)
    create_question_video(output_file)


def prepare_answer(dex, output_file=OUTPUT_ANSWER):
    pokename_path = get_tts_path(dex)
    create_answer_video(bg_path = WTP_ANSWER_TEMPLATE, pokename_path = pokename_path, video_path=WTP_ANSWER, export_path=output_file)

if __name__ == "__main__":

    dex = 120
    prepare_question(dex)
    prepare_answer(dex)

    # with open(POKE_LOG, "r") as log_file:
    #     lines = log_file.readlines()
    # for line in lines:
    #     if line != "":
    #         num, sig = line.split(" ")
    #         if sig == "-\n":
    #             print(num)
