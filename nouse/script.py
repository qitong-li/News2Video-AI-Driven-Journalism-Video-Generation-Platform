from openai import OpenAI
from pathlib import Path

client = OpenAI(
  organization='org-1gPz97WbvRfmVQkjHxpDGFnW',
  api_key='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'
)

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {
      "role": "system",
      "content": '''you are designed to generate scripts for 30-second news videos for vertical screens. 
Please generate a video journalism script based on the news text I provided.

1. List the author's name, date, and publication at the top of the script
2. Narration Included at least one quote from the article 
3. Please keep the total narration under 140 words.
4. In the script, mention which video to overlay when talking
5. Narration and Visual should not be in the same line, I hope there is a line feed between them,
6. Do not use 'Quote:', use 'Narration:' instead to show the quote, I hope there is only Narration and Visual.
7.  Please keep the total narration under 140 words.
8. The format of the script you generate is Narration and visual, where navigation is the content that the commenter needs to promote through voice, and visual is the content that needs to be presented on the screen.  
9. please ensure there are at least two pairs of Narration and Visual

Please strictly follow the following return format and don't add other information:
begin:\n
Author: [Author Name]\n
Date: [Date]\n
Publication: [Publication]\n
Narration: [Narration1]\n\n
Visual:[Visual1]\n\n
Narration:  [Narration2]\n\n
Visual: [Visual2]\n\n
end


please ensure there are at least two pairs of Narration and Visual
please double check if the total narration is under 140 words '''
    },
    {
      "role": "user",
      "content": '''Germany’s Industrial Production Falls For Seventh-Straight Month
Reflects further weakness in the key manufacturing sector of Europe’s largest economy
By 
Ed Frankl
Follow
Feb. 7, 2024 3:12 am ET




Resize

Gift unlocked article

Listen

(3 min)



The Eberspaecher factory in Herxheim bei Landau, southwestern Germany. (Photo by Kirill KUDRYAVTSEV / AFP) (Photo by KIRILL KUDRYAVTSEV/AFP via Getty Images) PHOTO: KIRILL KUDRYAVTSEV/AGENCE FRANCE-PRESSE/GETTY IMAGES
Germany’s industrial production declined more than expected in December, posting a seventh-straight month of falling output and reflecting further weakness in the key manufacturing sector of Europe’s largest economy.

Output slumped 1.6% compared with the previous month, seasonally and on a calendar-adjusted basis, from an upwardly revised 0.2% decline in November, according to data published Wednesday by German statistics office Destatis.

It compared with a forecast of a 0.3% contraction, according to economists polled by The Wall Street Journal.

Output in the chemical industry fell 7.6% in December on month, while it declined 3.4% in construction. In energy-intensive industries, production dipped 5.8% on month, despite falls in gas prices. Compared with the same month of 2022, overall production was down 3.0% in December, Destatis said.

However, Germany’s key car industry, home to global brands like Volkswagen and Mercedes-Benz, saw output rise 4.0% on month, the data said.

In a less volatile three-month on three-month comparison, production from October to December was 1.8% lower than the prior quarter.

“The seventh consecutive monthly fall in German industrial output in December confirms that industry remains a significant drag on growth,” Capital Economics economist Franziska Palmas said in a note.

“High energy costs and weak domestic and external demand will cause German industrial output to decline further in 2024,” she added.

For the whole year of 2023, industrial production fell 1.5%, with energy production dragging down the performance with a 15% decline, Destatis said. Reasons included low energy requirements in an already subdued industrial sector, cheap electricity imports and the shutdown of Germany’s last nuclear-power plant in April 2023. Yet electricity generation from wind power reached its highest level to date in 2023. Chemical production, however, fell to its lowest level since 1995.

The measure of production in manufacturing, energy and construction comes after data on Tuesday showed new factory orders rose 8.9% in December, albeit heavily swayed by larger orders including from aircraft. Excluding those big-ticked purchases, orders fell by 2.2%.

Write to Ed Frankl at edward.frankl@wsj.com'''}
  ],
  temperature=1,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)
response = response.choices[0].message.content
print(response)

import re
import pexelsPy
import requests

PEXELS_API = '0JF3nEvyZvaY2RTFVTOBInBAANyq3qiDbFgDEJppTAz3c7Am8v2iILGY'
api = pexelsPy.API(PEXELS_API)



# response = '''ChatCompletion(id='chatcmpl-8ptz7uafAo6YIkk5ocfI3ST1Z6rMN', choices=[Choice(finish_reason='length', index=0, logprobs=None, message=ChatCompletionMessage(content="Narration: TikTok, the popular social media app known for its short video content, has recently lost a significant catalog of music. But what exactly happened?\n\nVisual: Opening shot of a smartphone displaying the TikTok app logo.\n\nNarration: It all started when TikTok's parent company, ByteDance, failed to reach a music licensing agreement with Universal Music Group (UMG).\n\nVisual: Split-screen showcasing logos of TikTok and Universal Music Group.\n\nNarration: The music licensing agreement between TikTok and UMG allowed users to freely use a vast selection of songs provided by the record label.\n\nVisual: B-roll footage of users on TikTok dancing and creating videos to popular songs.\n\nNarration: With the absence of this licensing deal, TikTok users are no longer able to use UMG's music without facing potential copyright infringement issues.\n\nVisual: Illustration of a copyright symbol with a red X over it, indicating the unavailability of UMG's music on TikTok.\n\nNarration: This loss of a massive catalog of music is a significant blow to TikTok, as it heavily relies on its users' ability to create and share content set to popular songs.\n\nVisual: Montage of TikTok videos with various users dancing and lip-syncing to songs, highlighting", role='assistant', function_call=None, tool_calls=None))], created=1707380625, model='gpt-3.5-turbo-0613', object='chat.completion', system_fingerprint=None, usage=CompletionUsage(completion_tokens=256, prompt_tokens=216, total_tokens=472))'''

narrations = re.findall(r'Narration: (.*?)\n', response)
visuals = re.findall(r'Visual: (.*?)\n', response)
ids = []
for narration, visual in zip(narrations, visuals):
    print("Narration:", narration)
    print("Visual:", visual)
    response = client.audio.speech.create(
      model="tts-1",
      voice="alloy",
      input="Today in the luxury real estate market, America's most expensive home has hit the market for a staggering $295 million in Naples, Florida.The 9-acre compound, located in Naples' Port Royal neighborhood, consists of three houses and a private yacht basin. With approximately 1,650 feet of waterfront, this property is the highest-priced listing in the United States.Financier John Donahue purchased the initial parcel of land, just a small fishing cottage surrounded by mangroves, for $1 million in 1985. Over the years, the Donahue family expanded their holdings, eventually building a beachfront retreat for their large family.After John and Rhodora Donahue passed away, their family decided to list the crown jewel of their estate, the 9-acre compound, for a potentially record-breaking $295 million.The property's potential record-breaking sale price would make it the most expensive residential sale in the country. Real estate agents Dawn McKenna of Coldwell Banker Realty, Leighton Candler of the Corcoran Group, and Rory McMullen of Savills are marketing the property.The Donahue family's Naples compound became a beloved gathering place for their large family, spanning multiple generations. With over 175 great-grandchildren, the property holds many cherished memories.The Donahues hosted notable guests such as former President George H.W. Bush, Arnold Palmer, and even Pope John Paul II. Their strong Catholic faith, family values, and dedication to their financial business, Federated Investors, guided every aspect of their lives.After decades of creating memories, the Donahue family has decided to part ways with their beloved Naples property. This historic listing is a testament to the allure and exclusivity of luxury real estate in the United States.The sale of this extraordinary property will undoubtedly captivate both real estate enthusiasts and luxury home buyers alike."
    )
    response.stream_to_file('./speeches/' + narration[:20] + '.mp3')

    api.search_videos(visual, page=1, results_per_page=5)
    videos = api.get_videos()
    for i in range(len(videos)):
        id = videos[i].id
        if id in ids:
            continue
        url_video = 'https://www.pexels.com/video/' + str(videos[i].id) + '/download'
        # break
        ids.append(id)
        r = requests.get(url_video)
        with open('./videos/'+ visual[:20] + str(i) +'.mp4', 'wb') as outfile:
            outfile.write(r.content)
        print()