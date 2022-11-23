# base image
FROM node:13.12.0-alpine3.11

# FROM node:14.20.1-alpine

# set working directory
WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

# g++ compiler for fibers and sass
RUN apk add python make g++

# install app dependencies
COPY ./package.json /app/package.json
COPY ./package-lock.json /app/package-lock.json
RUN npm install
RUN npm install @vue/cli -g

# copy files
COPY . /app

CMD npm run serve
