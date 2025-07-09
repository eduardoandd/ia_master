# 016 - Chat prompt Templates
import os
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv()
KEY = os.getenv('OPENAI_API_KEY')
model = ChatOpenAI(model= 'gpt-3.5-turbo')

chat_template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content='Você é um especealista em queijo.'), # diretriz
        HumanMessagePromptTemplate.from_template('Me fale sobre o {type_cheese}'),
        HumanMessage('Certifique-se de falar se é mesmo considerado um queijo'),        
        AIMessage('Entendido, aqui estão os dados: ')
    ]
)

prompt = chat_template.format_messages(type_cheese='Cheddar')
response = model.invoke(prompt)


