FROM node:14-alpine

WORKDIR /visual-programming/front-end

COPY . .

RUN npm install && npm run-script build

EXPOSE 3000

CMD npx serve -s build -l 3000
