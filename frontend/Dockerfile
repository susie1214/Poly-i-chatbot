FROM node:18
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends build-essential libc6

RUN rm -rf node_modules package-lock.json

COPY package.json package-lock.json* ./
RUN npm ci --no-audit --no-fund

COPY . /app
ENV NODE_ENV=development
EXPOSE 3001
CMD ["npm", "run", "dev", "--", "--host"]
