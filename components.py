from openai import OpenAI
import time
import requests
import pexelsPy

client = OpenAI(
    organization='org-1gPz97WbvRfmVQkjHxpDGFnW',
    api_key='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'
  )

def generate_audio(name, narration):
    response = client.audio.speech.create(
      model="tts-1",
      voice="alloy",
      input=narration
    )
    response.stream_to_file('./speeches/' + name + '.mp3')


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
        print()

def stream_data(text):
    for word in text.split():
        yield word + " "
        time.sleep(0.02)