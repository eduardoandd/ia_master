from openai import OpenAI
import os
KEY = os.getenv('API_KEY')

client = OpenAI(
    api_key=KEY
)

stream = client.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=[
       {'role':'system', 'content': 'Você é um assistente virtual especealizado em carros e mecânica, passe informações técnicas sobre isso.'},
       {'role': 'user', 'content':'Me fale sobre o camaro'}, 
    ],
    stream = True
)

for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end='')


