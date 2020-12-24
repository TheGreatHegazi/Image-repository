welcome to my Shopify challenge

In order to start using my image repository please run the following command. ( make sure you have docker and docker compose up to date and have docker already started.)

./init1.sh 

while the command runs let me explain a little how my project works. 

backend is in fastapi (python)
frontend is in Vue.js 

firstly, the backend is somewhat like a zookeeper ensamble.  Once a user gets created the backend creates a file for the user and saves their encrypted credentials for authentication. 

when the user requests to add an image an image is added to the file of the user (private) or to public folder that can be seen by anyone (even anonymous i.e. no account).
all uploaded images are stored on the disk storage of the server.


The frontend offloads as much work onto the backend as possible almost no computation is done in the frontend. The frontend is forgetful of the user, this means that if you are logged in and you refresh the page you will be logged out. 

once logged in the frontend stores your token and uses it to comunicate with the api. any api call that is user specific (i.e. has /user in the url) will need to have the token. everything else is open to the public.

it is possible to add multiple images in one api call using the browse feature. 

when the containers are ready. please go to http://localhost:8080/home