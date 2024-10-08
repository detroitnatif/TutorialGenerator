import playsound
import os
import openai
import warnings
from elevenlabs.client import ElevenLabs
from elevenlabs import play, stream, save
import subprocess
import random
import requests
import logging

warnings.filterwarnings("ignore", category=DeprecationWarning)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

elevenlabs_key = os.environ.get("ELEVENLABS_API_KEY")

narration_api = 'openai' # 'elevenlabs'


client = ElevenLabs(
  api_key=elevenlabs_key
)

def parse(narration):
    output = []
    paragraphs = narration.split('\n')

    for paragraph in paragraphs:
        if paragraph.startswith("Narrator: "):
            text = paragraph.replace("Narrator: ", '')
            output.append(
                {'type': 'text',
                 'content': text}
            )
        elif 'Background image:' in paragraph:
            # Splitting by ':' to accurately remove the "[Background image:" part and the trailing ']'
            # This also handles removing any leading enumeration like "1) [" by splitting and taking the last part
            background = paragraph.split(': ', 1)[-1].rstrip(']')
            output.append(
                {'type': 'image',
                 'description': background}
            )
    
    return output
    
def create(data, name, output_folder, api_key):
    logging.info('creating narration')
    narration_file_path = os.path.join(name, output_folder)
    if not os.path.exists(narration_file_path):
        os.makedirs(narration_file_path)

    n = 0
    for element in data:
        if element['type'] != 'text':
            continue
        
        n += 1
        output_file = os.path.join(narration_file_path, f'narration_{n}.mp3')
        
        if narration_api == 'openai':
            openai.api_key = api_key
            audio = openai.audio.speech.create(
                input= element['content'],
                model='tts-1',
                voice='alloy'
            )
            audio.stream_to_file(output_file)
        else:
            audio = client.generate(
                text= element['content'],
                voice='Grace'
            
            )
            
            save(audio, output_file)
