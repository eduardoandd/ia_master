from langchain_openai import OpenAI,ChatOpenAI
import os 
from dotenv import load_dotenv
from langchain_community.cache import InMemoryCache,SQLiteCache 
from langchain.globals import set_llm_cache # set cache na aplicação

load_dotenv()
KEY = os.getenv('API_KEY')

model = OpenAI(openai_api_key=KEY)
# set_llm_cache(InMemoryCache()) #não persistida
set_llm_cache(
    SQLiteCache(database_path='cache.db')
)

prompt = 'Quem foi aeinstein'
response1 = model.invoke(prompt)
print(f'chamada 1: {response1}')

response2 = model.invoke(prompt)
print(f'chamada 2: {response2}')

