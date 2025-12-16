FROM node:18-alpine
WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install --no-audit --no-fund

COPY . /app
ENV NODE_ENV=development
EXPOSE 3001
CMD ["npm", "run", "dev", "--", "--host"]
