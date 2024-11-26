FROM node:14

WORKDIR /app

COPY package.json /app/
COPY package-lock.json /app/

RUN npm install

COPY . /app/

EXPOSE 8002

CMD ["node", "main.js"]
