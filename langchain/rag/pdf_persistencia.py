import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from dotenv import load_dotenv
from langchain.chains.retrieval import create_retrieval_chain
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain

load_dotenv()

KEY = os.getenv('OPENAI_API_KEY')
model = ChatOpenAI(model='gpt-4-turbo')

pdf='fatura.pdf'
loader=PyPDFLoader(pdf)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = text_splitter.split_documents(
    documents=docs
)

persist_directory='db'
embedding= OpenAIEmbeddings()
# vector_store=Chroma.from_documents(
#     documents=chunks,
#     embedding=embedding,
#     persist_directory=persist_directory,
#     collection_name='fatura'
# )

vector_store = Chroma(
    persist_directory='db',
    embedding_function=embedding,
    collection_name='fatura'
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

query = 'Qual foi o total de entrada e total de saida?'
response = chain.invoke(
    {'input':query}
)
