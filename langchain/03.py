# 015 - Prompt Templates
import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()
KEY = os.getenv('OPENAI_API_KEY')
model = ChatOpenAI(model='gpt-3.5-turbo')

template = '''
    Traduza o texto do {idioma1} para o {idioma2}: {texto}
'''

prompt_template = PromptTemplate.from_template(
    template= template
)

prompt = prompt_template.format(
    idioma1='português',
    idioma2='francês',
    texto='boa tarde'
)

response = model.invoke(prompt)
print(response.content)