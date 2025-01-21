import os
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

os.environ['OPENAI_API_KEY'] = os.getenv('API_KEY')

model = ChatOpenAI(model='gpt-3.5-turbo')

prompt = 'oi tudo bem'
chat_template= ChatPromptTemplate.from_messages(
    [
        SystemMessage(content='Você é um assistente virtual preciso que você me responda as coisa como se tivesse falando normalmente.'),
        HumanMessagePromptTemplate.from_template(prompt)
    ]
)

response = model.invoke(prompt)


