from openai import OpenAI
import base64
from dotenv import load_dotenv
import os

client = OpenAI(
    api_key= os.getenv('API_KEY')
)

# primeira integração
# response = client.chat.completions.create(
#     model = 'gpt-3.5-turbo',
#     messages=[
#         {
#          'role':'user', 
#          'content': 'eu to apontando a câmera do meu celular pra um notebook por exemplo, consigo usar sua api para ver isso em tempo real e identificar q é um notebook?. E se eu perguntar para você(em audio) "oq é isso" vc consegue me responder (em aúdio também)?'
#         },
#     ],
# )
# print(response.choices[0].message.content)


# trabalhando com stream
# stream = client.chat.completions.create(
#     model = 'gpt-3.5-turbo',
#     messages=[
#         {
#          'role':'user', 
#          'content': 'Sabe me informar se existe algum modelo que consegue converter um texto em audio? que disponibiliza api'
#         },
#     ],
#     stream=True
# )

# for chunk in stream:
#     if chunk.choices[0].delta.content is not None:
#         print(chunk.choices[0].delta.content, end = '')


# Agentes e contexto
# response = client.chat.completions.create(
#     model = 'gpt-3.5-turbo',
#     messages=[
        
#         {
#            'role':'system', 
#            'content': 
#                '''
#                    Você é um assistente do meu aplicativo chamado Tasks. 
#                    é possivel fazer um crud de tarefas, e você vai responder as dúvidas do usuários de uma forma bastante amigável, de boas vindas quando vc for responder.
                   
#                    Deleção: coloque o dedo na tarefa desejada e arraste verticalmente para cima ou para baixo.
#                    Trocar de dia: Deslize horizontalmente para direita caso queira ir para o dia seguinte ou para esquerda caso queira o dia anterior, ou seleicone o calendário no canto superior direito.
#                    Adicionar: clique no icone de "+" no canto inferior direito.
#                    Editar: Selecione a tarefa desejada, clique e segure.
                   
#                '''
#         },
#         {'role':'user', 'content':'Como posso adicionar umaa tarefa em um dia que não seria hoje?'}
         
#     ],
# )

# response_text = response.choices[0].message.content

# Trabalhando com parâmetros
# response = client.chat.completions.create(
#     model = 'gpt-3.5-turbo',
#     messages=[
        
#         {
#            'role':'system', 
#            'content': 
#                '''
#                    Você é um assistente do meu aplicativo chamado Tasks. 
#                    é possivel fazer um crud de tarefas, e você vai responder as dúvidas do usuários de uma forma bastante amigável, de boas vindas quando vc for responder.
                   
#                    Deleção: coloque o dedo na tarefa desejada e arraste verticalmente para cima ou para baixo.
#                    Trocar de dia: Deslize horizontalmente para direita caso queira ir para o dia seguinte ou para esquerda caso queira o dia anterior, ou seleicone o calendário no canto superior direito.
#                    Adicionar: clique no icone de "+" no canto inferior direito.
#                    Editar: Selecione a tarefa desejada, clique e segure.
                   
#                '''
#         },
#         {'role':'user', 'content':'Como posso adicionar umaa tarefa em um dia que não seria hoje?'}
         
#     ],
#     # max_tokens=70
#     # temperature=0.1
# )
# print(response.choices[0].message.content)

# Gerando imagens
# response = client.images.generate(
#     model = 'dall-e-3',
#     prompt='gere o madara do naruto com byakugan',
#     size='1024x1024',
#     quality='hd',
#     n=1
    
# )
# image_url=response.data[0].url
# print(image_url)

# Gerador de audio
# response_audio = client.audio.speech.create(
#     model = 'tts-1',
#     voice='nova',
#     input = response_text
# )
# response_audio.write_to_file('audio.mp3')

# Transcrevendo audio
# audio_file = open('audio.mp3','rb')
# transcription = client.audio.transcriptions.create(
#     model = 'whisper-1',
#     file=audio_file
# )
# print(transcription.text)

def encode_image(imagem_path):
    with open(imagem_path, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

        return encoded_image
    
def prompt_audio_to_text(audio):
    audio_file=open(audio,'rb')
    transcription = client.audio.transcriptions.create(
        model = 'whisper-1',
        file=audio_file
    )
    print(transcription.text)
    return transcription.text;
    
def analyze_image(client, image_path,audio_prompt):
    
    prompt = prompt_audio_to_text(audio_prompt)
    base64_image=encode_image(imagem_path=image_path)
    
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages= [
            {'role':'system', 'content': 'Você é um assistente virtual preciso que você me responda as coisa como se tivesse falando normalmente.'},
            {
                'role':'user',
                'content': [
                    {'type':'text','text': prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},}
                ]
            }
        ]
    )
    return response.choices[0].message.content

def convert_texto_to_audio(client):
    response_text=analyze_image(client=client,image_path='image.jpg',audio_prompt='audio_2.wav')
    response_audio = client.audio.speech.create(
        model = 'tts-1',
        voice='nova',
        input =response_text
    )
    response_audio.write_to_file('audio.mp3')
    

convert_texto_to_audio(client=client)