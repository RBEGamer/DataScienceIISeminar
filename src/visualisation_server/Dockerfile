FROM node:16

# WOKR DIR
WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install

# COPY SOURCE
COPY . .
# REMOVE DB DIR
RUN rm -f ./db
RUN mkdir -f ./db

EXPOSE 3016
CMD [ "node", "server.js" ]
