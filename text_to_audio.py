from openai import OpenAI
import os

KEY = os.getenv('API_KEY')

client = OpenAI(
    api_key=KEY
)

response = client.audio.speech.create(
    model='tts-1',
    voice='nova',
    input='Eu vou dar balinha po tarântula eu vou dar balinha po tarantula',
)
response.write_to_file('neu_audio.mp3')