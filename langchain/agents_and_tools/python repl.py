from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain.agents import Tool
from langchain_experimental.utilities import PythonREPL
from langchain_experimental.agents.agent_toolkits import create_python_agent
from langchain.prompts import PromptTemplate

load_dotenv
KEY = os.getenv('OPENAI_API_KEY')
model = ChatOpenAI(model='gpt-3.5-turbo')

python_repl = PythonREPL()
python_repl_tool = Tool(
    name='Python REPL',
    description='Um shell Python. Use isso para executar código Python. Execute apenas códigos Python válidos, importe as bibliotecas que precisar e julgar necessário. Se você precisar obter o retorno do código, use a função "print(...)"  dica: os valores que tiverem um sinal de menos ("-") quer dizer que são despesas',
    func=python_repl.run
)

agent_executor = create_python_agent(
    llm=model,
    tool=python_repl_tool,
    verbose=True
)

prompt_template = PromptTemplate(
    input_variables=['query'],
    template='Resolve o problema : {query}'
)

query = f'gere um datafreme aleatorio'
prompt = prompt_template.format(query=query)

response = agent_executor.invoke(prompt)
response.get('output')



