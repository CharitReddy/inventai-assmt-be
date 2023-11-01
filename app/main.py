from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api.api import router as api_router
from mangum import Mangum
import openai
import os
from dotenv import load_dotenv


app = FastAPI()
handler=Mangum(app=app)


load_dotenv()
OPENAI_API_KEY = os.getenv("OPEN_AI_KEY")
openai.api_key=OPENAI_API_KEY

@app.get("/")
def hello():
    return{"message":"Hello lambda"}


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
    
    except Exception as e:
      raise HTTPException(status_code=400, detail=f"OPEN AI Error - {e}")
       


@app.post('/generate-emails')
async def generate_emails(user_info:dict):
  try:
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
    
    email_list=[]
    for email in [invitation_email, promotional_email, welcome_email]:  
      email_list.append(email.choices[0].message.content)
    
    return email_list
  except Exception as e:
    raise HTTPException(status_code=400, detail=f"Error generating emails - {e}")



app.include_router(api_router, prefix="/api")

