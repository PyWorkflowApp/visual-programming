FROM node:14-alpine

WORKDIR /visual-programming/front-end

COPY package.json .

RUN npm install

COPY src/ ./src/
COPY public/ ./public/

EXPOSE 3000

CMD npm start
