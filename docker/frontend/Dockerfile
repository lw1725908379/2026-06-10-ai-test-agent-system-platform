FROM node:20-alpine

WORKDIR /app

# 复制依赖文件并安装
COPY ui/package*.json ./
RUN npm ci

# 复制源码
COPY ui/ .

# 生产构建（预编译所有页面，避免运行时编译卡顿）
RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
