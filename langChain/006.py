import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

os.environ['OPENAI_API_KEY'] = os.getenv('API_KEY')

model = ChatOpenAI(model='gpt-3.5-turbo')

classification_chain = (
    PromptTemplate.from_template(
        '''
        Classifique a pergunta do usuário em um dos seguintes setores:
        -Financeiro
        -Suporte técnico
        -Outras Informações
        
        Pergunta:{pergunta}
        
        '''
    )
    |model
    |StrOutputParser() 
)

financial_chain = (
    PromptTemplate.from_template(
        '''
        Você é um especealista financeiro.
        Sempre responda às perguntas começando com "bem vindo ao setor financeiro"
        Responda à pergunta do usuário:
        Pergunta: {pergunta}
        '''
    )
    | model
    | StrOutputParser()
)

tech_support_chain = (
    PromptTemplate.from_template(
        '''
        Você é um especealista em suporte técnico.
        Sempre responda às perguntas começando com "bem vindo ao suporte técnico!"
        Responda à pergunta do usuário:
        Pergunta: {pergunta}
        '''
    )
    | model
    | StrOutputParser()
)

other_info_chain = (
    PromptTemplate.from_template(
        '''
        Você é um especealista em informações gerais.
        Sempre responda às perguntas começando com "bem vindo!"
        Responda à pergunta do usuário:
        Pergunta: {pergunta}
        '''
    )
    | model
    | StrOutputParser()
)

def route(classification):
    classification = classification.lower()
    
    if 'financeiro' in classification:
        return financial_chain
    elif 'técnico' in classification:
        return tech_support_chain
    else:
        return other_info_chain
    
pergunta= 'Como faço para alterar minha senha?'
classification = classification_chain.invoke({'pergunta':pergunta})

response_chain = route(classification=classification)

response = response_chain.invoke({'pergunta':pergunta})
