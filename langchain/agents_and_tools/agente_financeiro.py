from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.agents import Tool, create_react_agent, AgentExecutor
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_experimental.utilities import PythonREPL
from langchain import hub

load_dotenv
KEY = os.getenv('OPENAI_API_KEY')
model = ChatOpenAI(model='gpt-3.5-turbo')

prompt = '''
    Como assistente financeiro pessoal, que responderá as perguntas dando dicas financeiras e de invesimento.
    Responsa tudo em português brasileiro
    Perguntas: {q}
'''
prompt_template = PromptTemplate.from_template(prompt)

python_repl= PythonREPL()
python_repl_tool = Tool(
    name='Python REPL',
    description='Um shell Python. Use isso para executar código Python. Execute apenas códigos Python válidos.'
                'Se você precisar obter o retorno do código, use a função "print(...)".'
                'Use para realizar cálculos financeiros necessários para responder as perguntas e dar dicas..'
                ,
    func=python_repl.run
)

search = DuckDuckGoSearchRun()
duckduckgo_tool = Tool(
    name='Busca DuckDuckGo',
    description='Útil para encontrar informações e dicas de economia e opções de investimento.'
                'Você sempre deve pesquisar na internet as melhoras dicas usando esta ferramenta, não responsa diretamente. Sua resposta deve informa que há elementos pesquisado na internet',
    func=search.run
)

react_instructions = hub.pull('hwchase17/react')

tools = [python_repl_tool, duckduckgo_tool]
agent = create_react_agent(
    llm=model,
    tools=tools,
    prompt= react_instructions
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)

question = '''
Minha renda é de R$3000, tenho despesas fixas com faculdade de 700 reais. Quais dicas de
investimento você me da?

'''
output = agent_executor.invoke(
    {'input': prompt_template.format(q=question)}
)


