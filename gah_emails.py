from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import email
from apiclient import errors
import re

# If modifying these scopes, delete the file token.pickle.
#we only want the readonly scope.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

#This will open a page in web browser for authentication, and then allow this python file to gain readonly controls to email.
#"Authorization information is stored on the file system, so subsequent executions will not prompt for authorization."

'''
The purpose of this app is not exactly as original plan. This just goes through a user's emails looking for job-application related emails, interview related emails,
for direct connections to people who work for those companies.

The intention for this script is so that You can have a nice list of emails from past applications/interviews that you can contact again for the future.

'''

def get_msg(service, msg_id):
	"""Get a Message with given ID.

	Args:
	service: Authorized Gmail API service instance.
	user_id: User's email address. The special value "me"
	can be used to indicate the authenticated user.
	msg_id: The ID of the Message required.

	Returns:
	A Message.
	"""
	try:
		message = service.users().messages().get(userId='me', id=msg_id).execute()

		print('Message snippet: %s' % message['snippet'])

		return message
	except Exception as e:
		print('An error occurred: %s' % e)

def clean_dirty_email(dirty_email):
	#remove all <>
	dirty_email = dirty_email.replace('<', '')
	dirty_email = dirty_email.replace('>', '')
	dirty_email = dirty_email.replace('"', '') 

	#clean with some bad regex
	email_found = re.search('\S+@\S+', dirty_email)
	if (email_found):
		#print("match", email_found.group(), dirty_email)

		dirty_email = email_found.group()
		#Check if the email looks legit
		if (len(dirty_email) > 40):
			#average email length is 25 characters. we upperbound and trash anything over 40 characters. Highly unlikely to be an email
			return None
		#Like checking it says "do_not_reply, no-reply, bounce
		if (dirty_email.find("do_not_reply") != -1 or dirty_email.find("no-reply") != -1 or dirty_email.find("bounce") != -1
			or dirty_email.find("DoNotReply") != -1 or dirty_email.find("myworkday") != -1 or dirty_email.find("jobvite") != -1 or dirty_email.find("candidate") != -1):
			return None

		#If the word workday appears before the @ symbol, highly unlikely to be an email
		if (dirty_email.find("workday") != -1 and dirty_email.find("workday") != -1 < dirty_email.find("@")):
			return None
		
		return email_found.group()
	return None




def main():
	"""Shows basic usage of the Gmail API.
	Lists the user's Gmail labels.
	"""
	creds = None
	# The file token.pickle stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first
	# time.
	if os.path.exists('token.pickle'):
		with open('token.pickle', 'rb') as token:
			creds = pickle.load(token)
	# If there are no (valid) credentials available, let the user log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				'credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)
		# Save the credentials for the next run
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)

	service = build('gmail', 'v1', credentials=creds)

	final_scraped_emails = []

	#Get emails in inbox. Currently only looks at inbox only, no spam
	#Tried to optimize and find emails that match specific queries, so might not be perfect and miss some but maybe it will be fine.
	#check through application emails 
	#try:
	query = "thank you for applying OR applying OR application OR applied OR Update on your application"
	response = service.users().messages().list(userId='me', includeSpamTrash=False, labelIds = ["INBOX"], maxResults="25", q=query).execute()
	messages_curr_page = {}
	if 'messages' in response:
		messages_curr_page = response['messages']
		print(messages_curr_page)
		page_token = response['nextPageToken']
		#For each page in the result messages, search through headers for sender address
		#headers vary from different senders, so we are need to guess this, so also not accurate.
		#More information about email headers over HTTP
		#https://mediatemple.net/community/products/dv/204643950/understanding-an-email-header
		#Decided after research that these curernt feilds return the best results.

		#Get the message
		print("\n\n\n")
		for msg_info in messages_curr_page:
			#get id
			msg = get_msg(service, msg_info['id'])
			headers = msg['payload']['headers']

			#fields_to_search = {}
			
			fields_to_search = (list(clean_dirty_email(h['value']) for h in headers 
				if (h['name'] == 'Sender' or h['name'] == 'From' or h['name'] == 'Reply-To' or h['name'] == 'Return-Path' )))
			print(fields_to_search)
			#Take values that passed the dirt cleaning and add to final list. 
			for clean_field in fields_to_search:
				if (clean_field != None):
					final_scraped_emails.append(clean_field)
			

		#while 'nextPageToken' in response:
		#page_token = response['nextPageToken']
		#response = service.users().messages().list(userId=user_id, q=query,
											#pageToken=page_token).execute()
		#messages.extend(response['messages'])

			#print(messages)
	#except Exception as e:
	#   print('An error occurred: %s' % e)

	#Now check through interview emails. May be overlap.


	#Print out the final list of cleaned emails
	print('Searched through all emails. Emails found that are most likely valid:')
	print(final_scraped_emails)

if __name__ == '__main__':
	main()