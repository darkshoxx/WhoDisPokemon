import os

import boto3
import botocore
import pypokedex
from dotenv import load_dotenv

region_name = "us-east-1"
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

HERE = os.path.abspath(os.path.dirname(__file__))
FILES_FOLDER = os.path.join(HERE, "generated_tts_files")
ENV = os.path.join(HERE, ".env")
load_dotenv(ENV)
# Note, credentials have been removed, because I am paranoid about AWS bills
# Disclaimer: Part of this file was generated by Gemini.
polly = boto3.client('polly', region_name=region_name)

sts_client = boto3.client('sts')

try:
    # Get caller identity (optional)
    identity = sts_client.get_caller_identity()
    print("Credentials found successfully!")
except botocore.exceptions.ClientError as error:
    print(f"Error getting identity: {error}")

# This was used to generate the TTS Soundfiles for the pokemon.
start = 1
end = 1025
for dex in []:  # range(1, 1026):
    p = pypokedex.get(dex=dex)
    name = p.name

    response = polly.synthesize_speech(
        Text=name,
        OutputFormat='mp3',
        VoiceId='Joanna'  # Choose a voice (adjust as needed)
    )

    with open(os.path.join(FILES_FOLDER, f"{dex}_{name}.mp3"), 'wb') as f:
        f.write(response['AudioStream'].read())
