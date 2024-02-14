from openai import OpenAI
from pathlib import Path
import json

def generate_script(message_content):
  client = OpenAI(
    organization='org-1gPz97WbvRfmVQkjHxpDGFnW',
    api_key='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'
  )

  instruction = '''
  you are designed to generate script for 30-seconds news videos for vertical screens. 
  Please generate a video journalism script based on the news text I provided.

  1. List the author name, date, and publication at the top of the script
  2. Included at least one quote from the article as narration
  3. Please ensure that the video duration does not exceed 1 minutes, so the total narration should not exceed 200 words. Thank you!
  4. In the script, mention which video to overlay when talking
  5. Have at least 2 pairs of narration and visual.
  6. 


  Please strictly follow the following return format and don't add other information:
  Author: [Author Name]
  Date: [Date]
  Publication: [Publication]
  Narration: xxx\nVisual: xxx\nNarration: xxx\nVisual: xxx\nThe format of the script you generate is Narration, Visual, where navigation is the content that the commenter needs to promote through voice and visual is the content that needs to be presented on the screen, please do not change the format and 'xxx' should be one-line
  '''

  # assistant = client.beta.assistants.create(
  #     name="AVPN",
  #     instructions=instruction,
  #     model="gpt-3.5-turbo"
  # )

  thread = client.beta.threads.create()
  
  message = client.beta.threads.messages.create(
      thread_id=thread.id,
      role="user",
      content=message_content
  )
  run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id='asst_y4jHBjTSbow6CYOroj52iqyb',
    instructions=""
  )
  while run.status != 'completed':
    run = client.beta.threads.runs.retrieve(
      thread_id=thread.id,
      run_id=run.id
    )

  messages = client.beta.threads.messages.list(
    thread_id=thread.id
  )
  print('————————————————————————')
  response = messages.data[0].content[0].text.value
  print(response)


  with open("test.json",'w',encoding='utf-8') as f:
      json.dump(response, f,ensure_ascii=False)

  return response

if __name__ == '__main__':
   generate_script('')


'''
import re
import pexelsPy
import requests

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
'''