import re
import pexelsPy
import requests

PEXELS_API = '0JF3nEvyZvaY2RTFVTOBInBAANyq3qiDbFgDEJppTAz3c7Am8v2iILGY'
api = pexelsPy.API(PEXELS_API)



response = '''Author: Callum Borchers Date: Feb. 7, 2024 Publication: The Wall Street Journal

Narration: It's flu season, but besides dealing with coughs and sneezes, workers are also facing a frustrating side effect: sick shaming at work. Visual: Office setting with employees working at their desks

Narration: According to the Centers for Disease Control and Prevention, respiratory illnesses have been above the national baseline since November, including influenza, Covid-19, RSV, and the common cold. Visual: Graph showing the increase in respiratory illnesses

Narration: Despite the spread of germs, American workers are reporting to the office at the highest rates in almost four years. Visual: Office occupancy graph showing an increase

Narration: Some bosses subtly or explicitly urge employees to ignore minor symptoms and come to work, creating a culture of "gut it out." Visual: Boss and employee interaction with a sick employee being encouraged to work

Narration: A recent survey found that 20% of managers encourage under-the-weather employees to come to the office, while almost a quarter suspect workers lie about being sick or exaggerate their illnesses. Visual: Survey results infographic showing manager attitudes towards sick employees

Narration: This pressure from bosses and colleagues leaves workers feeling shamed no matter what they do—staying home or coming to work sick. Visual: Office environment with employees looking uncomfortable or stressed

Narration: However, sick shaming can have consequences for businesses, including damage to reputation and morale. Visual: Business logo with a red "x" over it

Narration: Recognizing the importance of rest and recovery, some employers are encouraging their employees to take sick days and prioritize their health. Visual: Employee resting at home with a sick day message from the company

Narration: Megan Wollerton, founder of Life Force Wellness, emphasizes the need to take care of oneself and avoid spreading illnesses to the rest of the team. Visual: Megan Wollerton giving a wellness talk to employees

Narration: CEOs like Jaymes Black of Family Equality are also changing their mindset, giving employees the time they need to take care of their health. Visual: Jaymes Black talking to employees about the importance of sick days

Narration: It's time to shift the culture around sick days and prioritize the well-being of employees. Visual: Office environment with a positive and supportive atmosphere

End'''

# 使用正则表达式提取Narration和Visual信息
narrations = re.findall(r'Narration: (.*?)Visual', response)
print(narrations)
combined_narration = ''.join(narrations)
visuals = re.findall(r'Visual: (.*?)\n\n', response)
ids = []
print(combined_narration)
'''
# 输出提取的Narration和Visual信息
for visual in visuals:
    print("Visual:", visual)
    api.search_videos(visual, page=1, results_per_page=5)
    videos = api.get_videos()
    for i in range(len(videos)):
        id = videos[i].id
        if id in ids:
            continue
        url_video = 'https://www.pexels.com/video/' + str(videos[i].id) + '/download'
        break
    ids.append(id)
    r = requests.get(url_video)
    with open('./videos/'+visual+'.mp4', 'wb') as outfile:
        outfile.write(r.content)
    print()

'''