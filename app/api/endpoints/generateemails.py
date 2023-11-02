from fastapi import APIRouter, HTTPException,Request
import openai
import os
from dotenv import load_dotenv

router = APIRouter()
load_dotenv()

# Load OpenAI API key from .env
OPENAI_API_KEY = os.getenv("OPEN_AI_KEY")

openai.api_key=OPENAI_API_KEY


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
@router.post("/")
async def generate_emails(user_info:dict,request:Request):
  try:
    print(f"----------------OpenAI API----------------\n{request}")
    print(user_info)
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
    print(f"-----------------OpenAI Error-----------------\n{e}")
    raise HTTPException(status_code=400, detail=f"Error generating emails - {e}")
        
  
  # review_and_edit_emails = await openai.Edit.create(
  #     input=final_invitation_email,
  #     engine="davinci",
  #     instruction=f"Please edit and review the following emails to make them more clear, concise, and engaging. Carefully review the emails and verify that they are tailored for {user_info['info']} and ensure their name is matching {user_info['name']}.",
  # )
  # print(review_and_edit_emails)
  # return review_and_edit_emails