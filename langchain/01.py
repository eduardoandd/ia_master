from langchain_openai import OpenAI,ChatOpenAI
import os 
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv('API_KEY')


# model = OpenAI()

# response=model.invoke(
#     input="Quem foi pericles o grego?"
# )

# print(response)

model = ChatOpenAI(
    model='gpt-3.5-turbo'
)

messages = [
    {'role': 'system', 'content': 'Você é um professor que fala sobre figuras históricas'},
    {'role': 'user', 'content':'Quem foi o pericles, o grego?'}
]

response = model.invoke(messages)
print(response.content)