# 017 - Simple Chains
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate


load_dotenv()
KEY = os.getenv('OPENAI_API_KEY')
model = ChatOpenAI(model='gpt-3.5-turbo')

# prompt_template =  PromptTemplate.from_template(
#     'Me fale sobre o queijo {type_cheese}'
# )

# chain = prompt_template | model | StrOutputParser() # chain

chain = (
    PromptTemplate.from_template(
        'Me fale sobre o queijo {type_cheese}'
    )
    | model
    | StrOutputParser()
)

result = chain.invoke({'type_cheese': 'Qualho'})
