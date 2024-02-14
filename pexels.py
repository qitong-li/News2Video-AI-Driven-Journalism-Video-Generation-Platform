'''
key:0JF3nEvyZvaY2RTFVTOBInBAANyq3qiDbFgDEJppTAz3c7Am8v2iILGY

from pexelsapi.pexels import Pexels
pexel = Pexels('0JF3nEvyZvaY2RTFVTOBInBAANyq3qiDbFgDEJppTAz3c7Am8v2iILGY')
search_videos = pexel.search_videos(query='Opening shot of a smartphone displaying the TikTok app logo.', orientation='portrait', size='small', color='', locale='', page=1, per_page=1)
print(search_videos)
'''
import json
with open("test.json",'r',encoding='utf-8') as load_f:
    response = json.load(load_f)

import re
import pexelsPy
import requests
from openai import OpenAI


client = OpenAI(
  organization='org-1gPz97WbvRfmVQkjHxpDGFnW',
  api_key='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'
)

PEXELS_API = '0JF3nEvyZvaY2RTFVTOBInBAANyq3qiDbFgDEJppTAz3c7Am8v2iILGY'
api = pexelsPy.API(PEXELS_API)

narrations = re.findall(r'Narration: (.*?)\n', response)
visuals = re.findall(r'Visual: (.*?)\n', response)
ids = []
for index, (narration, visual) in enumerate(zip(narrations, visuals)):
    print("Narration:", narration)
    print("Visual:", visual)
    response = client.audio.speech.create(
      model="tts-1",
      voice="alloy",
      input=narration
    )
    response.stream_to_file('./speeches/' + str(index) + '.mp3')

    api.search_videos('Vertical ' + visual, page=1, results_per_page=5)
    videos = api.get_videos()
    for i in range(len(videos)):
        id = videos[i].id
        if id in ids:
            continue
        url_video = 'https://www.pexels.com/video/' + str(videos[i].id) + '/download'
        ids.append(id)
        r = requests.get(url_video)
        with open('./videos/'+ str(index) + visual[:5] + str(i) +'.mp4', 'wb') as outfile:
            outfile.write(r.content)
        print()
