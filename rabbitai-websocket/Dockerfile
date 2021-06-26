FROM node:14.16.1

WORKDIR /home/rabbitai-websocket

COPY . .

RUN npm ci
RUN npm run build

CMD ["npm", "start"]
