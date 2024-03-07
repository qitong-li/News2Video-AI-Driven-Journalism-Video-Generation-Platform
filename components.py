from openai import OpenAI
import time
import requests
import pexelsPy
from PIL import Image
from io import BytesIO
import base64

client = OpenAI(
    organization='org-1gPz97WbvRfmVQkjHxpDGFnW',
    api_key='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'
  )

def generate_audio(name, narration, voice):
    response = client.audio.speech.create(
      model="tts-1",
      voice=voice,
      input=narration
    )
    response.stream_to_file('./speeches/' + name + '.mp3')

def generate_picture(index, visual):
    for i in range(3):
        images_response = client.images.generate(
            model="dall-e-3",
            prompt=visual,
            # size="1024x1024",
            size="1024x1792",
            quality="standard",
            response_format='b64_json',
            n=1,
        )
        image_path = './pictures/'
        image_data = images_response.data[0]
        image_obj = image_data.model_dump()["b64_json"]
        image_obj = Image.open(BytesIO(base64.b64decode(image_obj)))
        image_path = image_path + index + str(i) + '.png'
        image_obj.save(image_path)


PEXELS_API = '0JF3nEvyZvaY2RTFVTOBInBAANyq3qiDbFgDEJppTAz3c7Am8v2iILGY'
api = pexelsPy.API(PEXELS_API)


def generate_video(index, visual):
    ids = []
    api.search_videos('Vertical ' + visual, page=1, results_per_page=5)
    videos = api.get_videos()
    for i in range(len(videos)):
        id = videos[i].id
        if id in ids:
            continue
        url_video = 'https://www.pexels.com/video/' + str(videos[i].id) + '/download'
        ids.append(id)
        r = requests.get(url_video)
        with open('./videos/'+ str(index) + str(i) +'.mp4', 'wb') as outfile:
            outfile.write(r.content)

def stream_data(text):
    for word in text.split():
        yield word + " "
        time.sleep(0.02)