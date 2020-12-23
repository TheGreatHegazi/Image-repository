#!/bin/bash

echo 'building docker image of backend'

cd image-repo-backend && docker build -t image-repo-backend . 


echo 'building docker image of frontend'

cd ../image-repo-ui/frontend && docker build -t image-repo-ui . 

echo 'spinning up containers using docker compose '

cd ../../ && docker-compose up -d 
