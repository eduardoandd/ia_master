from langchain_openai import OpenAI, ChatOpenAI
import os

os.environ['OPENAI_API_KEY'] = os.getenv('API_KEY')
model = OpenAI()

response = model.invoke(
    input = 'Quem foi Frederico barba ruiva',
    temperature = 1,
    max_tokens = 500
)

model = ChatOpenAI(
    model='gpt-3.5-turbo'
)

messages=[
    {'role': 'system', 'content': 'Você é um asistente que fornce informações sobre figuras históricas e suas princiapais conquistas'},
    {'role': 'user', 'content': 'Quem foi frederico barba ruiva?'}
]

response = model.invoke(messages)


