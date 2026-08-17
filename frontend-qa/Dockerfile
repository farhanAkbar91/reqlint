FROM node:18-alpine

WORKDIR /app

COPY frontend-qa/package.json ./

RUN npm install

COPY frontend-qa ./

EXPOSE 3000

CMD ["npm", "run", "dev"]
