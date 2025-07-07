from openai import OpenAI
import os
KEY = os.getenv('API_KEY')

client = OpenAI(
    api_key=KEY
)

response = client.images.generate(
    model='dall-e-3',
    prompt='Um setup que transmita calma e leveza para um programador trabalhar',
    size='1024x1024',
    quality='standard',
    n=1
)

image=response.data[0].url
print(image)
