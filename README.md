# Welcome to my Shopify challenge

In order to start using my image repository please run the following command in the image-repository folder. ( make sure you have docker and docker compose up to date and have docker already started.)

` ./init1.sh `

while the command runs let me explain a little how my project works. 

the backend is in fastapi (python), while the frontend is in Vue.js 
## Backend
firstly, the backend is somewhat like a zookeeper ensamble.  Once a user gets created the backend creates a file for the user and saves their encrypted credentials for authentication.  I decided to go with this implementation as I did not want the images to be hosted on another server.

when the user requests to add an image an image is added to the file of the user (private) or to a public folder that can be seen by anyone (even anonymous i.e. no account).
all uploaded images are stored on the disk storage of the server.

## Frontend
The frontend offloads as much work onto the backend as possible almost no computation is done in the frontend. The frontend is forgetful of the user, this means that if you are logged in and you refresh the page you will be logged out. 

once logged in the frontend stores your token and uses it to comunicate with the api. any api call that is user specific (i.e. has /user in the url) will need to have the token. everything else is open to the public.

it is possible to add multiple images in one api call using the browse feature. 

when the containers are ready. please go to http://localhost:8080/home

### Thanks for taking a look at my repository!
