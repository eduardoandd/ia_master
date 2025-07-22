import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from dotenv import load_dotenv
from langchain.chains.retrieval import create_retrieval_chain
from langchain_chroma import Chroma
from langchain_community.document_loaders import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain



load_dotenv()

KEY = os.getenv('OPENAI_API_KEY')
model = ChatOpenAI(model='gpt-4-turbo')

loader=CSVLoader('fatura.csv')
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = text_splitter.split_documents(
    documents=docs
)

embedding = OpenAIEmbeddings()
# vector_store = Chroma.from_documents(
#     documents=chunks,
#     embedding=embedding,
#     persist_directory='db',
#     collection_name='fatura_csv'
# )

vector_store = Chroma(
    persist_directory='db',
    embedding_function=embedding,
    collection_name='fatura_csv'
)
retriever = vector_store.as_retriever()

system_prompt= '''
Use o contexto para responder as perguntas.
contexto:{context}
'''
prompt = ChatPromptTemplate.from_messages(
    [
        ('system', system_prompt),
        ('human', '{input}'),
    ]
)
question_answer_chain = create_stuff_documents_chain(
    llm=model,
    prompt=prompt
)

chain= create_retrieval_chain(
    retriever=retriever,
    combine_docs_chain=question_answer_chain
)

query = 'Por que você consegue analisar apenas 4 registros? esse arquivo csv tem mais de 4 registros'
response = chain.invoke(
    {'input':query}
)
