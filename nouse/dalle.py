from openai import OpenAI
from PIL import Image
from io import BytesIO
import base64


client = OpenAI(
    organization='org-1gPz97WbvRfmVQkjHxpDGFnW',
    api_key='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'
  )

images_response = client.images.generate(
  model="dall-e-3",
  prompt="Coca-Cola beverage bottles lined up with graphics showing sales growth percentages and price increase information.",
  # size="1024x1024",
  size="1024x1792",
  quality="standard",
  response_format='b64_json',
  n=1,
)
image_path = './pictures/'
for i, image_data in enumerate(images_response.data):
    image_obj = image_data.model_dump()["b64_json"]
    image_obj = Image.open(BytesIO(base64.b64decode(image_obj)))
    image_path = image_path + str(i) + '1.png'
    image_obj.save(image_path)