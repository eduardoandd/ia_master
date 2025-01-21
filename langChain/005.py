import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

os.environ['OPENAI_API_KEY'] = os.getenv('API_KEY')

model = ChatOpenAI(model='gpt-3.5-turbo')

# prompt_template = PromptTemplate.from_template(
#     '{prompt}'
# )

# runnable_sequence = prompt_template | model | StrOutputParser()

# result = runnable_sequence.invoke('oi tudo bem?')

runnable_sequence = (
    PromptTemplate.from_template(
        '{prompt}'
    )
    | model
    | StrOutputParser()
)

response = runnable_sequence.invoke('oi tudo bem')