from openai import OpenAI
from pathlib import Path
import json
import time

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
    assistant_id='asst_ZQdIhJExtR9d3zRq0Hw8Pg4p',
    instructions=""
  )
  while run.status != 'completed':
    run = client.beta.threads.runs.retrieve(
      thread_id=thread.id,
      run_id=run.id
    )
    time.sleep(5.0)
    print(run)

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
   message_content = '''LIFESTYLE
TRAVEL
These Dogs Ended Up on a No-Fly List. Their Owners Are Baffled.
Pet owners find airlines inconsistent in how they enforce taking pets in carry-on bags—with some animals ending up banned

GETTY IMAGES
By Jacob PassyFollow
Feb. 13, 2024 9:00 am ET

SAVE

SHARE

TEXT
254 RESPONSES

Explore Audio Center
True or false: There’s a no-fly list for dogs and your pet might be on it. 

Travelers like Megan Moskowitz say it absolutely exists. When Moskowitz tried to fly with her dog, an English cocker spaniel named Maci, to visit family in Indiana, she says United Airlines agents at Newark Liberty International Airport wouldn’t let Maci on the plane.

She says the agents took photos of Maci and informed her that Maci was permanently banned from traveling with the airline.

NEWSLETTER SIGN-UP

WSJ Travel

Inspiration and advice for navigating your vacations and business trips, along with the latest travel news.


Preview

Subscribe
United declined to comment beyond pointing to the section of its website that details its policies on flying with pets. The Transportation Department granted airlines more leeway in 2021 to keep pets off planes if they aren’t service animals.

Pet owners have tangled with airlines in recent years as carriers have cracked down on people traveling with animals. Airlines said more people traveling with pets led to an uptick in incidents involving these animals, including bites, urination and defecation. They also received complaints from some passengers, including those with allergies, about the animals.

Dog owners say United Airlines has developed the strictest reputation for its policy of banning furry companions judged not to fit comfortably in a kennel, even if they behave well in the air. 

Moskowitz had chosen Maci because she wanted a small dog she could bring on trips. Her first flight with Maci in November went off without a hitch. But since the Newark incident, Moskowitz, an advertising professional in New York City, has hesitated trying flying with Maci again. 

“It seems like such a gamble,” she says.

Teddy makes the list

Gabriela Garcia-Orth’s Pomeranian Teddy. PHOTO: GABRIELA GARCIA-ORTH
Gabriela Garcia-Orth says she never used to encounter any difficulty flying with her 8-year-old Pomeranian, Teddy. The marketing professional who lives in New Jersey estimates the two have flown over a dozen times together.

In November, Garcia-Orth and her husband tried to fly back to Newark from Houston with Teddy after a wedding. The family arrived at the airport hours early as a precaution after having paid United’s $125 fee to travel with a dog.

But a United employee told them their 10-pound dog wouldn’t be allowed to fly.

Garcia-Orth says the couple pleaded with the United agent to let them travel home. The agent obliged, she says, but they were told that a note about Teddy was being added to their file.

“It was confusing,” Garcia-Orth says. “But I didn’t want to get into it because I didn’t want to escalate the situation.”

Understanding the rules
In general, airlines require an animal to be small enough to be comfortable in a carrier that can fit underneath the seat in front of a passenger. Many airlines stipulate that the pet must be able to stand up and turn around in the carrier without touching the sides to fly.

Airlines usually limit the number of pets they allow in the cabin, and passengers are typically charged a fee to fly with their pets.

Some airlines allow larger pets to be transported in a plane’s baggage hold, but have limitations based on an animal’s size. Others, including United, have discontinued this service in recent years for most travelers. Some airlines prohibit certain breeds of dogs from flying in the baggage compartment. 

Pet Protocol
A look at some of United Airlines' rules for carrying pets on board.

Rules for pets

No weight or breed limitations for pets.

Must travel in either a hard-sided or soft-sided carrier that fits under the seat in front of you, and must stay in carrier for duration of the flight.

Only be one pet per carrier, and they must be able to stand up and turn around while inside.

Only service animals are allowed on planes without a pet carrier.

Must pay a $125 fee each way for traveling with your pet. If there is a layover of more than four hours within the U.S. or 24 hours internationally, a separate fee is charged for each flight.

Hard-sided carrier

Soft-sided carrier

Pet is too large

7.5 in.

Pet is right size

11 in.

12 in.

11 in.

17.5 in.

18 in.

Note: Drawing is schematic
Source: United Airlines
Jemal R. Brinson/THE WALL STREET JOURNAL
United isn’t the only airline that pet owners have had issues getting their pets on board. 

Jimmy Chang is a YouTuber from Denver who owns a Miniature Schnauzer named Milo. Chang says he and his family are regular Southwest customers and have flown with Milo twice.

SHARE YOUR THOUGHTS
What has been your experience flying with an animal on board? Join the conversation below.

This December, when Chang and two of his kids were flying to California to attend a family member’s funeral, Milo was turned away at the check-in desk, Chang says. Milo’s carrier still had the tag from the family’s last flight attached.

Chang’s brother-in-law drove to the airport to get Milo so that the family could still make their flight. Chang says he is now re-evaluating his allegiance to Southwest.


Rachael Breder is training her 2-year-old Pembroke Welsh corgi named Chesapeake, or Chessy. PHOTO: RACHAEL BREDER
“Now if there’s another airline where the time may be a little bit more convenient or the price may be a little bit lower, then we’re flying with them,” he says.

A Southwest spokeswoman said in an email that the airline’s “pet-friendly policy is in line with” Federal Aviation Administration guidelines.

Some travelers say that the unpredictability with their pets has complicated making plans. Rachael Breder is training her 2-year-old Pembroke Welsh corgi named Chesapeake, or Chessy, to compete in dog agility competitions. On the last trip she took on United with Chessy, Breder says agents told her they were flagging her account because of Chessy’s size.

Breder, an account manager for a propane company who lives in Sellersville, Pa., hopes to enter Chessy into competitions across the U.S., and maybe one day take her to compete overseas. That is, if she can find a reliably amenable airline.

“There’s travel that I want to do with her,” she says.

Sign up for the WSJ Travel newsletter for more tips and insights from the Journal’s travel team.

Write to Jacob Passy at jacob.passy@wsj.com'''
   generate_script(message_content)


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