#Router chains
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
KEY = os.getenv('OPENAI_API_KEY')
    
model= ChatOpenAI(model='gpt-3.5-turbo')
    
classification_chain = (
    PromptTemplate.from_template(
        '''
            Classifique a pergunta do usuário em um dos seguintes setores:
            
            - Financeiro
            - Suporte técnico
            - Outras Informações
            
            Pergunta: {pergunta}
        '''
    )
    | model
    | StrOutputParser()
)

financial_chain = (
    PromptTemplate.from_template(
        '''
        Você é um especealista financeiro.
        Sempre responsa as perguntas começando com "Bem vindo ao setor Financeiro".
        Pergunta: {pergunta}
        '''
    )
    | model
    | StrOutputParser()
)

tech_chain = (
    PromptTemplate.from_template(
        '''
        Você é um especealista suporte técnico.
        Sempre responsa as perguntas começando com "Bem vindo ao suporte técnico".
        Pergunta: {pergunta}
        '''
    )
    | model
    | StrOutputParser()
)

other_info_chain = (
    PromptTemplate.from_template(
        '''
        Você é um especealista informações gerais.
        Sempre responsa as perguntas começando com "Olá, em que posso ajudar?".
        Pergunta: {pergunta}
        '''
    )
    | model
    | StrOutputParser()
)

def router(classification):
    classification = classification.lower()
    if 'financeiro' in classification:
        return financial_chain
    elif 'técnico' in classification:
        return tech_chain
    else:
        return other_info_chain
    
pergunta = 'Como faço para alterar a minha senha?'

classification = classification_chain.invoke(
    {'pergunta': pergunta}
)

response_chain = router(classification=classification)

response = response_chain.invoke(
    {'pergunta': pergunta}
)
print(response)