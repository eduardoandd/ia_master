from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os
from langchain_community.document_loaders import TextLoader, CSVLoader,UnstructuredExcelLoader
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv
KEY = os.getenv('OPENAI_API_KEY')
model = ChatOpenAI(model='gpt-3.5-turbo')

loader = CSVLoader('../fatura.csv')
docs = loader.load()

prompt_base_conhecimento = PromptTemplate(
    input_variables=['contexto', 'pergunta'],
    template = ''' Use o seguinte contexto para responder à pergunta.
    Responsa apenas com base nas informações fornecidas.
    Não utilize informações externas ao contexto:
    Contexto: {contexto}
    Pergunta: {pergunta}
    '''
)

chain = prompt_base_conhecimento | model | StrOutputParser()

chain.invoke(
    {
        'contexto': '\n'.join(doc.page_content for doc in docs),
        'pergunta': 'Me fale quanto que eu ganhei e quanto q eu gastei e categorize e faça um pequeno relatório.'
    }
)
