from pathlib import Path
from openai import OpenAI


client = OpenAI(
  organization='org-1gPz97WbvRfmVQkjHxpDGFnW',
  api_key='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'
)


speech_file_path = Path(__file__).parent / "speech.mp3"
response = client.audio.speech.create(
  model="tts-1",
  voice="alloy",
  input="Today in the luxury real estate market, America's most expensive home has hit the market for a staggering $295 million in Naples, Florida.The 9-acre compound, located in Naples' Port Royal neighborhood, consists of three houses and a private yacht basin. With approximately 1,650 feet of waterfront, this property is the highest-priced listing in the United States.Financier John Donahue purchased the initial parcel of land, just a small fishing cottage surrounded by mangroves, for $1 million in 1985. Over the years, the Donahue family expanded their holdings, eventually building a beachfront retreat for their large family.After John and Rhodora Donahue passed away, their family decided to list the crown jewel of their estate, the 9-acre compound, for a potentially record-breaking $295 million.The property's potential record-breaking sale price would make it the most expensive residential sale in the country. Real estate agents Dawn McKenna of Coldwell Banker Realty, Leighton Candler of the Corcoran Group, and Rory McMullen of Savills are marketing the property.The Donahue family's Naples compound became a beloved gathering place for their large family, spanning multiple generations. With over 175 great-grandchildren, the property holds many cherished memories.The Donahues hosted notable guests such as former President George H.W. Bush, Arnold Palmer, and even Pope John Paul II. Their strong Catholic faith, family values, and dedication to their financial business, Federated Investors, guided every aspect of their lives.After decades of creating memories, the Donahue family has decided to part ways with their beloved Naples property. This historic listing is a testament to the allure and exclusivity of luxury real estate in the United States.The sale of this extraordinary property will undoubtedly captivate both real estate enthusiasts and luxury home buyers alike."
)

response.stream_to_file(speech_file_path)