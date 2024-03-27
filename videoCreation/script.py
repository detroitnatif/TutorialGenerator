from openai import OpenAI
import os
from dotenv import load_dotenv
import narration

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

with open("source_material.txt") as f:
    source_material = f.read()

response =  client.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=[
        {
            'role':'system',
            'content': '''You are a youtube short recipe narration generator, 
            emphasize the steps and not thematic presentation, 
            30 seconds to 1 minute narration,
            the narration you create will have a picture background.
            
            respond with the following format with however many steps of the recipe:

            1) [Background image: Description of image first Ingredient and step]

            Narrator: "A few sentences of the cooking step details"

            2) [Background image: Description of image second Ingredient and step]

            Narrator: "How to do this step of cooking with details"

            ... continue for all the steps
            '''
        },
        {
            'role': 'user',
            'content': f'create a Youtube Short narration based on the following source material, emphasizing the exact steps of the recipe: \n\n {source_material}'
        }
    ]

)
print(response.choices[0].message.content)
data = narration.parse(response.choices[0].message.content)
narration.create(data, 'narration.mp3')