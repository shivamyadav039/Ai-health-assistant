# step1: Setup GROQ API Key
# 
import os
GROQ_API_KEY=os.environ.get("GROQ_API_KEY")


  
# step2: Convert image to required format
import base64 

#   image_path="acne.jpg"
def encode_image(image_path):
  
    image_file=open(image_path ,"rb")
    return base64.b64encode(image_file.read()).decode('utf-8')


# step3: setup Multimodal LLM

from groq import Groq

query="Is there something wrong with my face?"
model="llama-3.2-90b-vision-preview"

def analyze_image_with_query(query, model, encoded_image):
    client = Groq()
    query = "Is there something wrong with my face?"
    
    messages=[
        {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": query
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{encoded_image}",
                    },
                },
            ],
        }]
    chat_completion=client.chat.completions.create(
        messages=messages,
        model=model
    )
    return chat_completion.choices[0].message.content
































































