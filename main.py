from fastapi import FastAPI,HTTPException,Request,Path
from fastapi.middleware.cors import CORSMiddleware
import openai
from pydantic import BaseModel


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # You can specify specific HTTP methods, e.g., ["GET", "POST"]
    allow_headers=["*"],  # You can specify specific headers if needed
)

# Check for any connection issues.
@app.get("/hello")
async def hello_endpoint(request: Request,name: str = 'World',):
    return {"message": f"Hello, {name}!"}

# Wild card path
@app.get("/{path:path}")
async def not_found(path: str):
    raise HTTPException(status_code=404, detail="Path does not exist")

# Your OpenAI API key
OPENAI_API_KEY = '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'
openai.api_key=OPENAI_API_KEY


@app.post("/generate_emails")
async def generate_emails(user_info:dict):
 
  invitation_email= openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
          {
              "role": "user",
              "content": f"Generate an invitation email for {user_info['name']} to try out [frag ai], an app that can help them automate their social media handles. \n Use {user_info['info']} to personalize the email. Explain how automating social media handles saves them time in their profession from {user_info['info']}, and how they can focus on their tasks that require human interactions and leave tasks that can be automated to AI. \nInclude a subject field, and the to address {user_info['email']}"
          },
      ]
    )



  promotional_email=openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
          {
              "role": "user",
              "content": f"For future use, in case the user does not accept an invitation email that we sent, generate a promotional email for {user_info['name']} offering discounts for the user {user_info['name']}. \nInclude a subject field, and the to address {user_info['email']}"
          },
      ]
    )



  welcome_email=openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
          {
              "role": "user",
              "content": f"For future use, generate a welcome email for {user_info['name']} thanking them for trying out [frag ai]. \n Use {user_info['info']} and {user_info['name']} to personalize this email. \nInclude a subject field, and the to address {user_info['email']}"
          },
      ]
    )
  
  email_list=[]
  for email in [invitation_email, promotional_email, welcome_email]:  
    email_list.append(email.choices[0].message.content)
  
  return email_list
        
  
  # review_and_edit_emails = await openai.Edit.create(
  #     input=final_invitation_email,
  #     engine="davinci",
  #     instruction=f"Please edit and review the following emails to make them more clear, concise, and engaging. Carefully review the emails and verify that they are tailored for {user_info['info']} and ensure their name is matching {user_info['name']}.",
  # )
  # print(review_and_edit_emails)
  # return review_and_edit_emails