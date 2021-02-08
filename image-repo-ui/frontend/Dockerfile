FROM node:lts-alpine

RUN npm install -g http-server

WORKDIR /app

COPY package*.json ./

ENV PATH /app/node_modules/.bin:$PATH

RUN npm install

COPY . /app

RUN npm run build

EXPOSE 8080
