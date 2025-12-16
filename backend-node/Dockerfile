FROM node:18-alpine
WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install --production=false --no-audit --no-fund

COPY . /app
ENV NODE_ENV=development
EXPOSE 5000
CMD ["npm", "run", "dev"]
