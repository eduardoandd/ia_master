import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain import hub
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

KEY = os.getenv('OPENAI_API_KEY')
model = ChatOpenAI(model='gpt-4-turbo')

#load pdf
file_path = 'fatura.pdf'
loader = PyPDFLoader(file_path)
documents = loader.load()

#definindo configuração de quebra
text_splitter= RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

#quebrando em chunks
chunks = text_splitter.split_documents(
    documents=documents
)

embedding = OpenAIEmbeddings() # modelo de classicação
vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embedding,
    collection_name='faturas'
) # banco de dados de vetores

#sistema de recuperação de dados
retriever = vector_store.as_retriever()

prompt = hub.pull('rlm/rag-prompt')


rag_chain = (
    {
        'context':retriever,
        'question': RunnablePassthrough()
    }
    | prompt
    | model
    | StrOutputParser()
)

question = '''
faça uma análise quais foram as principais fontes de receitas e principais fontes de despesas?

'''
response = rag_chain.invoke(question)