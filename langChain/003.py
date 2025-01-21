from langchain_openai import ChatOpenAI
import os
from langchain.prompts import PromptTemplate


os.environ['OPENAI_API_KEY'] = os.getenv('API_KEY')
model = ChatOpenAI(model='gpt-3.5-turbo')
template = '''
Traduza o texto do {idioma1} para o {idioma2}: {texto}
'''

prompt_template = PromptTemplate.from_template(
    template = template
)
prompt = prompt_template.format(
    idioma1='Português',
    idioma2 = 'francês',
    texto='Boa dia!'
)

response = model.invoke(prompt)



