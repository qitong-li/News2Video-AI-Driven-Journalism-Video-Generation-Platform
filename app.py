import streamlit as st
from streamlit_player import st_player
import json
import re
from components import *
from script import generate_script
from merge import merge_videos
import threading

st.title("AVPN:movie_camera:")
message_content = st.text_area('Enter your article here.', value='', key=None)


# @st.cache_data
def script(message_content):
    print('——————————script————————————')
    # return
    generate_script(message_content)

# @st.cache_data
def audio(name, narration, voice):
    # return
    generate_audio(name, narration, voice)

# @st.cache_data
def video(index, visual):
    # return
    generate_video(index, visual)


# @st.cache_data
def image(index, visual):
    # return
    generate_picture(index, visual)

# @st.cache_data
def combine_videos(video_lists, picture_lists, durations, size):
    # return
    merge_videos(video_lists, picture_lists, durations, size)



if st.button('Generate Script:pencil:', key=None, help=None, args=None, kwargs=None, type="secondary", disabled=False, use_container_width=False):
    # threading.Thread(target=script(message_content)).start()
    script(message_content)
response = "Author: None\n Date: None\n Publication: None\n Narration: None\n Visual: None\n"
try:
    with open("test.json",'r',encoding='utf-8') as load_f:
        response = json.load(load_f)
except IOError:
    print("no test.json found")
author = re.findall(r'Author: (.*?)\n', response)
date = re.findall(r'Date: (.*?)\n', response)
publication = re.findall(r'Publication: (.*?)\n', response)
narrations = re.findall(r'Narration: (.*?)\n', response)
visuals = re.findall(r'Visual: (.*?)\n', response)

with st.expander("See Original Script:newspaper:"):
    try:
        st.write('Author: ' + author[0].replace("\\n", ""))
        st.write('Date: ' + date[0].replace("\\n", ""))
        st.write('Publication: ' + publication[0].replace("\\n", ""))
    except IndexError:
        print(IndexError)
    for i in range(len(narrations)):
        st.write('Narration: ' + narrations[i].replace("\\n", ""))
        st.write('Visual: ' + visuals[i].replace("\\n", ""))


size = st.selectbox(
    'To ensure the best viewing experience, let us know your preferred video format.',
    ('1080x1920 9:16 (for mobile) Vertical',
     '1920x1080 16:9 (for desktop) Horizontal'))[:9]

# st.write('You selected:', size)

number = [':zero:', ':one:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:', ':one::zeron:', ':one::one:', ':one::two:', ':one::three:', ':one::four:', ':one::five:', ':one::six:']
chosen_videos = []
chosen_pictures = []
durations = []
for index, (narration, visual) in enumerate(zip(narrations, visuals)):
    with st.expander("See part" + number[index]):
        new_narration = st.text_area('Narration Text', value=narration.replace("\\n", ""), key=None)
        narrations[index] = new_narration
        voice_type = st.selectbox(
            "Choose your narrator",
            ("alloy", "echo", "fable", "onyx", "nova", "shimmer"),
            placeholder="Select voice...",
            key=str(index) + 'voice_type'
        )
        
        if st.button('Generate Audio', type='secondary', key=str(index) + str(index) + new_narration[:2]):
            # threading.Thread(target=audio(str(index), new_narration, voice_type)).start()
            audio(str(index), new_narration, voice_type)
        try:
            audio_file = open('./speeches/' + str(index) + '.mp3', 'rb')
            audio_bytes = audio_file.read()
            
            st.audio(audio_bytes, format='audio/mp3')
        except IOError:
            print('audio', IOError)
        
        duration = st.number_input('How long would you like this part last? If left 0.0, we will use the length of the audio.', 
                                   key=str(index) + new_narration[:7])
        durations.append(duration)

        new_video_visual = st.text_input('Video visual description', value=visual.replace("\\n", ""))
        if st.button(label='Search Videos', type='secondary', key=str(index) + new_video_visual[:2]):
        #     threading.Thread(target=video(str(index), new_video_visual)).start()
        # st.button(label='Search Videos', type='secondary', key=str(index) + new_video_visual[:2],
        #           on_click=video(str(index), new_video_visual))
            video(str(index), new_video_visual)
        visuals[index] = new_video_visual
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                try:
                    video_file = open('./videos/'+ str(index) + str(i) +'.mp4', 'rb')
                    chosen = st.checkbox('Video ' + str(index) + str(i))
                    if chosen:
                        chosen_videos.append(str(index) + str(i))
                    video_bytes = video_file.read()
                    st.video(video_bytes)
                except IOError:
                    print('pexel vid', IOError)
        cols_col = st.columns([3, 2])
        with cols_col[0]:
            try:
                new_picture_visual = st.text_input('Image visual description', value=visual.replace("\\n", ""))
                if st.button(label='Generate Images', type='secondary', key=str(index) + new_picture_visual[:3]):
                # st.button(label='Generate Images', type='secondary', key=str(index) + new_picture_visual[:3],
                #           on_click=image(str(index), new_picture_visual))
                    image(str(index), new_picture_visual)
                cols_pictures = st.columns(3)
                for i in range(3):
                    with cols_pictures[i]:
                        image_file = open('./videos/'+ str(index) + str(i) +'.mp4', 'rb')
                        # image_file = './pictures/'+ str(index) + str(i) + '.png'
                        chosen = st.checkbox('Picture ' + str(index) + str(i))
                        if chosen:
                            chosen_pictures.append(str(index) + str(i))
                        st.image(image_file)
            except:
                print('picture', 'error')
        with cols_col[1]:
            try:
                uploaded_files = st.file_uploader("Choose your own file", accept_multiple_files=True, key=str(index)+'uploadfile')
                if len(uploaded_files) != 0:
                    cols_upload = st.columns(2)
                    for i in range(len(uploaded_files)):
                        with cols_upload[i]:
                            if i >= len(uploaded_files):
                                continue
                            uploaded_file = uploaded_files[i]
                            chosen = st.checkbox('Video ' + str(index) + str(5 + i))
                            if chosen:
                                chosen_videos.append(str(index) + str(i))
                            video_bytes = uploaded_file.read()
                            file = open("./videos/" + str(index) + str(5 + i) + '.mp4', 'wb')
                            file.write(video_bytes)
                            file.close()
                            st.video(video_bytes)  
            except IOError:
                print('upload', IOError)






# st.write('chosen_videos:')
# st.write(chosen_videos)
# st.write('chosen_pictures:')
# st.write(chosen_pictures)
# st.write('durations:')
# st.write(durations)

if len(chosen_videos) != 0 or len(chosen_pictures) != 0:
    if st.button('Merge Video', type='secondary', key=chosen_videos):
    # st.button('Merge Video', type='secondary', key=chosen_videos,
    #            on_click=combine_videos(chosen_videos, chosen_pictures, durations, size))
        combine_videos(chosen_videos, chosen_pictures, durations, size)
with st.expander("See Final Video:clapper: and Current Script:newspaper:"):
    cols = st.columns([0.3,0.7])
    with cols[0]:
        try:
            # st.button('renew', key='renew')
            video_file = open('./videos/target.mp4', 'rb')
            video_bytes = video_file.read()
            st.video(video_bytes)
        except IOError:
            print('final', IOError)

    with cols[1]:
        try:
            st.write('Author: ' + author[0].replace("\\n", ""))
            st.write('Date: ' + date[0].replace("\\n", ""))
            st.write('Publication: ' + publication[0].replace("\\n", ""))
        except IndexError:
            print('final script', IndexError)
        for i in range(len(narrations)):
            st.write('Narration: ' + narrations[i].replace("\\n", ""))
            st.write('Visual: ' + visuals[i].replace("\\n", ""))