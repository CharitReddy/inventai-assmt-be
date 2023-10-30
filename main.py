from fastapi import FastAPI,HTTPException,Request,Path
from fastapi.middleware.cors import CORSMiddleware
import openai
from pydantic import BaseModel
import requests
import asyncio

class PromptData(BaseModel):
    prompt: str

app = FastAPI()

origins = ["*"]



app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # You can specify specific HTTP methods, e.g., ["GET", "POST"]
    allow_headers=["*"],  # You can specify specific headers if needed
)

@app.get("/hello")
async def hello_endpoint(request: Request,name: str = 'World',):
    return {"message": f"Hello, {name}!"}

@app.get("/{path:path}")
async def not_found(path: str):
    raise HTTPException(status_code=404, detail="Path does not exist")

# Your OpenAI API key
OPENAI_API_KEY = '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'
openai.api_key=OPENAI_API_KEY


@app.post("/generate_emails")
async def test_openai_api(user_info:dict):
   try:
      async def generate_invitation_email():
        invitation_email= openai.ChatCompletion.create(
              model="gpt-3.5-turbo",
              messages=[
                {
                    "role": "user",
                    "content": f"Generate an invitation email for {user_info['name']} to try out [frag ai], an app that can help them automate their social media handles. \n Use {user_info['info']} to personalize the email. Explain how automating social media handles saves them time in their profession from {user_info['info']}, and how they can focus on their tasks that require human touch"
                },
            ]
          )
        return invitation_email
   
      async def generate_promotional_email():
        promotional_email=openai.ChatCompletion.create(
              model="gpt-3.5-turbo",
              messages=[
                {
                    "role": "user",
                    "content": f"For future use, in case the user does not accept an invitation email that we sent, generate a promotional email for {user_info['name']} offering discounts for the user {user_info['name']}"
                },
            ]
          )
        return promotional_email
      
      async def generate_welcome_email():
        welcome_email=openai.ChatCompletion.create(
              model="gpt-3.5-turbo",
              messages=[
                {
                    "role": "user",
                    "content": f"For future use, generate a welcome email for {user_info['name']} thanking them for trying out [frag ai]. \n Use {user_info['info']} and {user_info['name']} to personalize this email."
                },
            ]
          )
        return welcome_email
      
      invitation_email_task = generate_invitation_email()
      # invitation_email_result = await invitation_email_task

      promotional_email_task = generate_promotional_email()
      # promotional_email_result = await promotional_email_task

      welcome_email_task=generate_welcome_email()
      # welcome_email_result=await welcome_email_task


      
      review_and_edit_emails = await openai.Edit.create(
          input=[invitation_email_task, promotional_email_task,welcome_email_task],
          engine="davinci",
          instruction=f"Please edit and review the following emails to make them more clear, concise, and engaging. Carefully review the emails and verify that they are tailored for {user_info['info']} and ensure their name is matching {user_info['name']}.",
      )
   
      return review_and_edit_emails
   except Exception as error:
      return {"error": str(error)}