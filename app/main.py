from fastapi import FastAPI,HTTPException,Request
from fastapi.middleware.cors import CORSMiddleware
from api.api import router as api_router
from mangum import Mangum
import openai
import os
from dotenv import load_dotenv


app = FastAPI()

# CORS Configuration to accept requests from any client with any method.
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # You can specify specific HTTP methods, e.g., ["GET", "POST"]
    allow_headers=["*"],  # You can specify specific headers if needed
)

handler=Mangum(app=app)

load_dotenv()
OPENAI_API_KEY = os.getenv("OPEN_AI_KEY")
openai.api_key=OPENAI_API_KEY

# Test connection
@app.get("/")
def hello():
    print('hellooooooooo--------main')
    return{"message":"Hello lambda"}

# Takes in model name, user details, prompt, and requests OpenAI to generate an email.
def generate_mail(model, user_info, content):
    try:
      return model.create(
          model="gpt-3.5-turbo",
          messages=[
              {
                  "role": "user",
                  "content": content.format(**user_info),
              },
          ],
      )
    # Raise generic error.
    except Exception as e:
      raise HTTPException(status_code=400, detail=f"OPEN AI Error - {e}")
       

# Endpoint to interface with the method and trigger OpenAI calls using generate_mail method.
# user_info should be a json consisting of:
# name:str, email:str, info:str
@app.post('/generate-emails')
async def generate_emails(request:Request,user_info:dict):
  try:
    print("----------------OpenAI API----------------main--------------")
    print(f"----------request-------------\n{request}")
    print(OPENAI_API_KEY+"KEY API KEY")
    # Make 3 OpenAI calls to generate three emails.
    invitation_email = generate_mail(
            openai.ChatCompletion, user_info,
            "Generate an invitation email for {name} to try out [frag ai], an app that can help them automate their social media handles. Use {info} to personalize the email. Explain how automating social media handles saves them time in their profession from {info}, and how they can focus on their tasks that require human interactions and leave tasks that can be automated to AI. Include a subject field, and the to address {email}"
        )
    promotional_email = generate_mail(
            openai.ChatCompletion, user_info,
            f"For future use, in case the user does not accept an invitation email that we sent, generate a promotional email for {user_info['name']} offering discounts for the user {user_info['name']}. \nInclude a subject field, and the to address {user_info['email']}"
        )
    welcome_email = generate_mail(
            openai.ChatCompletion, user_info,
            f"For future use, generate a welcome email for {user_info['name']} thanking them for trying out [frag ai]. \n Use {user_info['info']} and {user_info['name']} to personalize this email. \nInclude a subject field, and the to address {user_info['email']}"
        )
    # Extract the generated emails from OpenAI Objects.
    email_list=[]
    for email in [invitation_email, promotional_email, welcome_email]:  
      email_list.append(email.choices[0].message.content)
    
    return email_list
  # Raise generic error.
  except Exception as e:
    print(f"-----------------OpenAI Error-----------------main\n{e}")
    raise HTTPException(status_code=400, detail=f"Error generating emails - {e}")


#Include and Prefix all sub routes with "/api"
app.include_router(api_router, prefix="/api")

