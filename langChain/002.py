from langchain_community.cache import InMemoryCache, SQLiteCache
from langchain.globals import set_llm_cache
from langchain_openai import OpenAI, ChatOpenAI
import os

#CACHE

os.environ['OPENAI_API_KEY'] = os.getenv('API_KEY')

model = OpenAI()

set_llm_cache(SQLiteCache())

prompt = 'Me diga quem foi Alan Turing'

response1 = model.invoke(prompt)
print(f'Chamada1: {response1}')

resposne2 = model.invoke(prompt)
print(f'Chamada2: {resposne2}')