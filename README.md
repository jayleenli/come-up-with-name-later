# gah! Emails
#### Setup and Installation Instructions
So I made a script `gah_emails.py`  
  
To use it, get a credentials.json file from clicking "Enable the Gmail API" on this page:  
https://developers.google.com/gmail/api/quickstart/python  
  
Make sure to install the google python library  
`pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`   
  
Put it in the same directory as `gah_emails.py`   
  
To run:  
`python gah_emails.py`  
  
####What does this do?
What this script does is uses the Gmail API to read your emails. (Don't worry, can't change anything) and try to find valid company contact emails from two sources: Job rejection related emails or interview related emails.  

Feel free to change the queries inside the script to potentially get a better range of emails. This script isn't perfect but it does it's job.

