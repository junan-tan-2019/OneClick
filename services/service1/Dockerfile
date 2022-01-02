
FROM node:14

# Create app directory
WORKDIR /usr/src/app


COPY src/package*.json ./

RUN npm install
RUN npm install dotenv
RUN npm install mysql2

COPY src/. .
COPY ./wait-for-it.sh .
RUN chmod +x ./wait-for-it.sh

# CMD [ "node", "app.js" ]
CMD ["npm", "start"]