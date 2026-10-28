FROM node:24-alpine

ENV NODE_ENV=production
WORKDIR /app

COPY package*.json ./
RUN npm ci --omit=dev

COPY config ./config
COPY src ./src
COPY utils ./utils

USER node
EXPOSE 3000
CMD ["node", "src/server.js"]