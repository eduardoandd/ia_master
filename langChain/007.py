import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import TextLoader, PyPDFLoader,CSVLoader

os.environ['OPENAI_API_KEY'] = os.getenv('API_KEY')
model = ChatOpenAI(model='gpt-3.5-turbo')

# loader = TextLoader('anotacoes.txt')
# documents = loader.load()

loader = PyPDFLoader('cv eduardo andrade.pdf')
documents = loader.load()


prompt_anotacoes = PromptTemplate(
    input_variables=['contexto','pergunta'],
    template='Análise o contexto e responda as minhas perguntas. Contexto: {contexto} Pergunta {pergunta}'
)

chain = prompt_anotacoes | model | StrOutputParser()
response =  chain.invoke(
    {
        'contexto': '\n'.join(doc.page_content for doc in documents),
        'pergunta': 'Oq vc acha q se trata esse arquivo?'
    }
)



