#Installation and Running
1. Clone this Repo
   
   `git clone https://github.com/CharitReddy/inventai-assmt-be.git`
   
3. Cd into the Fast-Api folder

   `cd inventai-assmt-be`
   
5. Create a virtual environment

   `python3 -m venv venv`
   
7. Activate virtualenv

   `source venv/bin/activate`

8. Install the required packages

   `python -m pip install -r requirements.txt`
   
9. CD into app

  `cd app`

8. Run the app using uvicorn

  `uvicorn main:app`

# View the app
The app will run on localhost:8000 by default.<br/>
localhost:8000 must return a simple welcome message {"message":"Hello lambda"}<br/>
The documentation for the APIs can be viewed at localhost:8000/docs <br/>
You can test it by using cli tools like cURL, or apps like postman, or the documentation at localhost:8000/docs. <br/>

# APIs
The app has 3 APIs:

1. GET/ api/hello/
   
   `Just returns a Hello World Message, can be used to test the server status.`
   
2. POST/ api/generate_emails/

   `Takes user information and calls OpenAI APIs to generate emails`

3. GET/ api/*

   `Wild card route, returns a 404 for any route except the above 2.`

   
   
