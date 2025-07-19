# import pandas as pd
# import sqlite3

# # 1. Carregar a planilha Excel
# df = pd.read_excel("fatura.xlsx")  # Altere o nome conforme necessário

# # 2. Criar ou conectar ao banco de dados SQLite
# conn = sqlite3.connect("meu_banco.sqlite3")

# # 3. Exportar o DataFrame para uma tabela no SQLite
# df.to_sql("minha_tabela", conn, if_exists="replace", index=False)

# # 4. Fechar a conexão
# conn.close()

import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain import hub
from langchain.prompts import PromptTemplate
from langchain.agents import create_react_agent, AgentExecutor
load_dotenv
KEY = os.getenv('OPENAI_API_KEY')
model = ChatOpenAI(model='gpt-4-turbo')

#conexao
db = SQLDatabase.from_uri('sqlite:///meu_banco.sqlite3')

#toolkit -> caixa de ferramentas
toolkit = SQLDatabaseToolkit(
    db=db,
    llm=model
)

#prompt -> mensagem do sistema
system_message = hub.pull('hwchase17/react')

#agente
agent = create_react_agent(
    llm=model,
    tools=toolkit.get_tools(),
    prompt=system_message
) 

agent_executor = AgentExecutor(
    agent=agent,
    tools= toolkit.get_tools(),
    verbose=True
)

prompt = '''
    Use as ferramentas necessárias para responder as minhas perguntas relacionadas as dados que estão dentro do meu database.
    Responsa tudo em português brasileiro.
    Pergunta: {q}
'''

prompt_template = PromptTemplate.from_template(prompt)
question = '''
Despesas: valores que apresentam um sinal de "-" na frente.
receitas: valores que não apresentam um sinal de "-" na frente.

Pergunta: Análise a coluna chamada valor do meu banco de dados e me fale qual foi o total de despesa e o total de receita q eu tive
'''
question2 = '''
Despesas: valores que apresentam um sinal de "-" na frente.
receitas: valores que não apresentam um sinal de "-" na frente.

Pergunta: Análise a coluna chamada valor e a coluna chamada data do meu banco de dados e me fale qual foi dia que
          eu tive a maior receita e o dia que eu tive a maior despesa
'''
question3 = '''
Despesas: valores que apresentam um sinal de "-" na frente.
receitas: valores que não apresentam um sinal de "-" na frente.

Pergunta: Análise a coluna chamada descrição e pense em uma forma de categorizar as linhas, resuma em 5 até categorias.
          Depois análise a oluna chamada valor e atribua o valor de despesas dessas categoria que você criou
'''

output = agent_executor.invoke(
    {
        'input': prompt_template.format(q=question3)
    }
)
output.get('output')




