import streamlit as st
import os
from langchain_openai import ChatOpenAI
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain import hub
from langchain.agents import create_react_agent,AgentExecutor


load_dotenv()

KEY = os.getenv('OPENAI_API_KEY')
model = ChatOpenAI(model='gpt-4-turbo')


st.set_page_config(
    page_title='Financeiro GPT',
    page_icon='📝'
)
st.header('Assistente Financeiro')
model_options = [
    'gpt-3.5-turbo',
    'gpt-4-turbo',
    'gpt-4o'
]

selected_model=st.sidebar.selectbox(
    label='Selecione o modelo LLM',
    options=model_options
)

st.sidebar.markdown('### Sobre')
st.sidebar.markdown('### Esse agente consulta um banco de dados de transações bancárias')

st.write('Faça perguntas sobre o tema.')
user_question=st.text_input('O que deseja saber sobre?')


model = ChatOpenAI(
    model=selected_model
)

db = SQLDatabase.from_uri('sqlite:///meu_banco.sqlite3')
toolkit = SQLDatabaseToolkit(
    db=db,
    llm=model
)
system_messag= hub.pull('hwchase17/react')
agent = create_react_agent(
    llm=model,
    tools = toolkit.get_tools(),
    prompt=system_messag
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=toolkit.get_tools(),
    verbose=True
)

prompt = '''
    Use as ferramentas necessárias para responder perguntas relacionadas ao que está no banco de dados.
    A resposta final deve ter uma formatação amigável de visualização para o usuário.
    Sempre responda em português brasileiro.
    Pergunta: {q}
'''
prompt_template = PromptTemplate.from_template(prompt)


if st.button('Consultar'):
    if user_question:
        with st.spinner('Consultando banco de dados..'):
            formated_prompt = prompt_template.format(q=user_question)
            output = agent_executor.invoke({'input': formated_prompt})
            st.markdown(output.get('output'))
        
        
    else:
        st.warning('POR FAVOR FAÇA UMA PERGUNTA')
    