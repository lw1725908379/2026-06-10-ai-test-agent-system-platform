FROM node:20-alpine

WORKDIR /app

# 复制依赖文件并安装
COPY ui/package*.json ./
RUN npm ci

# 复制源码
COPY ui/ .

EXPOSE 3000

CMD ["npm", "run", "dev"]
