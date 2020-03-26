# come-up-with-name-later
Something cool?


brainstorm time!
what am i trying to do:
* make a thing that can read emails
* So must be able to get user email threads
* Get the labels for email messages, also make labels(?)
* Date emails were sent
* Contact email of the sender and recipent 
* If we sent an attachment(?)
* times someone was contacted, if they responded (probably related to the thread stuff)
* how many times followed up

Things not needed:
* Editing and sending emails
* deleting threads and emails
* So I guess don't need direct modifications like POST or whatever


So conclusion we should go with g suite developer and use external api so I can use python
Progress:
First get hello world and see what these do
is a message the same as a email?
- [ ] GET  /userId/profile
- [ ] GET  /userId/labels
- [ ] GET  /userId/messages
- [ ] GET  /userId/messages/id
- [ ] GET  /userId/messages/messageId/attachments/id
- [ ] GET  /userId/settings/filters
- [ ] GET  /userId/threads
- [ ] GET  /userId/threads/id


Setup:  
`virtualenv email-contact-scraper`  
`source email-contact-scraper/bin/activate`  

Dependenies:
virtualenv  
`pip install virtualenv`  
* google-api-python-client


References:
https://developers.google.com/gmail/api/v1/reference  
https://developers.google.com/apps-script/reference/gmail/gmail-app
can execute api with ther api explorer thing  
https://developers.google.com/gmail/api/v1/reference/users/labels/list?authuser=3&apix_params=%7B%22userId%22%3A%22me%22%7D

Potentially autogenerate google sheets
https://developers.google.com/sheets/api/reference/rest