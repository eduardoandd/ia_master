from openai import OpenAI
import os

KEY = os.getenv('API_KEY')

client = OpenAI(
    api_key=KEY
)

audio_file = open('neu_audio.mp3','rb')

transcription = client.audio.transcriptions.create(
    model='whisper-1',
    file=audio_file
)
print(transcription.text)