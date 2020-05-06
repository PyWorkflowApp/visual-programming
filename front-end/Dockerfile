FROM node:14-alpine

WORKDIR /visual-programming/front-end

COPY . .

ARG BACKEND_URL
ENV REACT_APP_SERVER_URL=$BACKEND_URL
RUN npm install && npm run-script build

EXPOSE 3000

CMD npx serve -s build -l 3000
