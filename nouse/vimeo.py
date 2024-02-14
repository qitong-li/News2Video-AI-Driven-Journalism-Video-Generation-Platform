import pexelsPy
import requests

PEXELS_API = '0JF3nEvyZvaY2RTFVTOBInBAANyq3qiDbFgDEJppTAz3c7Am8v2iILGY'
api = pexelsPy.API(PEXELS_API)

api.search_videos('Opening shot of a smartphone displaying the TikTok app logo.', page=1, results_per_page=5)
videos = api.get_videos()
url_video = 'https://www.pexels.com/video/' + str(videos[0].id) + '/download'
r = requests.get(url_video)
with open('test.mp4', 'wb') as outfile:
    outfile.write(r.content)
