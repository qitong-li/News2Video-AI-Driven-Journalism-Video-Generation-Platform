import streamlit as st
import json
import re
from components import *
from script import generate_script
from merge import merge_videos

st.title("AVPN:movie_camera:")

message_content = st.text_area('Enter your article here.', value='', key=None)
response = "Author: None\n Date: None\n Publication: None\n Narration: None\n Visual: None\n"
try:
    with open("test.json",'r',encoding='utf-8') as load_f:
        response = json.load(load_f)
except IOError:
    print("no test.json found")

def script():
    # return
    generate_script(message_content)

def audio(name, narration):
    # return
    generate_audio(name, narration)

def video(index, visual):
    # return
    generate_video(index, visual)

def combine_videos(video_lists):
    # return
    merge_videos(video_lists)


chosen_videos = []

author = re.findall(r'Author: (.*?)\n', response)
date = re.findall(r'Date: (.*?)\n', response)
publication = re.findall(r'Publication: (.*?)\n', response)
narrations = re.findall(r'Narration: (.*?)\n', response)
visuals = re.findall(r'Visual: (.*?)\n', response)

st.button('Generate Script:pencil:', key=None, help=None, on_click=script, args=None, kwargs=None, type="secondary", disabled=False, use_container_width=False)

with st.expander("See Original Script:newspaper:"):
    st.write_stream(stream_data(author[0].replace("\\n", "")))
    st.write_stream(stream_data(date[0].replace("\\n", "")))
    st.write_stream(stream_data(publication[0].replace("\\n", "")))
    for i in range(len(narrations)):
        st.write_stream(stream_data('Narration: ' + narrations[i].replace("\\n", "")))
        st.write_stream(stream_data('Visual: ' + visuals[i].replace("\\n", "")))


number = [':zero:', ':one:', ':two:', ':three:', ':four:', ':five:', ':six:']
for index, (narration, visual) in enumerate(zip(narrations, visuals)):
    with st.expander("See part" + number[index]):
        new_narration = st.text_area('Narration', value=narration.replace("\\n", ""), key=None)
        narrations[index] = new_narration
        st.button('Generate Audio', on_click=audio(str(index), new_narration), type='secondary', key=new_narration[:5])
        audio_file = open('./speeches/' + str(index) + '.mp3', 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mp3')
        
        new_visual = st.text_input('Visual description', value=visual.replace("\\n", ""))
        st.button(label='Generate Video', on_click=video(str(index), new_visual), type='secondary', key=new_visual[:5])
        visuals[index] = new_visual
        cols = st.columns(5)
        for i in range(len(cols)):
            with cols[i]:
                video_file = open('./videos/'+ str(index) + str(i) +'.mp4', 'rb')
                chosen = st.checkbox('Video ' + str(index) + str(i))
                if chosen:
                    st.write('Great! This video has been added')
                    chosen_videos.append(str(index) + str(i))
                video_bytes = video_file.read()
                st.video(video_bytes)

# st.write('chosen_videos:')
# st.write(chosen_videos)
st.button(label='Merge Video', on_click=combine_videos(chosen_videos), type='secondary', key=chosen_videos)

with st.expander("See Final Video:clapper:"):
    video_file = open('./videos/target.mp4', 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)

with st.expander("See Current Script:newspaper:"):
    st.write_stream(stream_data(author[0].replace("\\n", "")))
    st.write_stream(stream_data(date[0].replace("\\n", "")))
    st.write_stream(stream_data(publication[0].replace("\\n", "")))
    for i in range(len(narrations)):
        st.write_stream(stream_data('Narration: ' + narrations[i].replace("\\n", "")))
        st.write_stream(stream_data('Visual: ' + visuals[i].replace("\\n", "")))