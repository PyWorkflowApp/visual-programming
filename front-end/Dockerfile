FROM node:current-slim

WORKDIR /visual-programming/front-end

COPY package.json .

RUN npm install

COPY . .

EXPOSE 3000

CMD npm start
