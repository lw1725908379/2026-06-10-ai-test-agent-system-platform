# Docker 部署中 AI 助手 LangGraph 连接失败 `ERR_NAME_NOT_RESOLVED` 排查与修复

---

## 现象

浏览器控制台报错：
```
Failed to load resource: net::ERR_NAME_NOT_RESOLVED
ConnectionError: Unable to connect to LangGraph server. Please ensure the server is running and accessible. Original error: Failed to fetch
```

同时后端 API 也返回 `500 Internal Server Error`。

---

## 排查过程

### 第一步：确认服务是否在运行

```bash
docker-compose ps
```

所有 8 个服务（postgres, redis, mongodb, minio, langgraph-server, backend, frontend, gitnexus-web）均为 `Up` 状态。

### 第二步：单独测试后端 API 和 LangGraph

```bash
# 测试后端
curl http://localhost:3001/api/v2/projects?page_size=10
# -> 返回 200，后端正常

# 测试 LangGraph
curl http://localhost:2026/info
# -> 返回 {"ok":true}，LangGraph 正常

# 但通过前端代理访问
curl http://localhost:3000/api/v2/projects?page_size=10
# -> Internal Server Error (500)
```

**关键发现**：直接访问服务正常，通过前端代理就报错。

### 第三步：检查容器内环境变量

```bash
docker exec ai-test-agent-system-platform-frontend-1 env | grep NEXT_PUBLIC
```

发现容器内环境变量是旧的 `host.docker.internal` 值，即使 `docker-compose.yml` 已经修改。这是因为容器需要重新创建才能读取新环境变量。

### 第四步：分析 URL 寻址问题（核心原因）

需要理解两个变量的**使用场景差异**：

| 变量 | 在何处执行 | 需要解析的目标 |
|------|-----------|---------------|
| `NEXT_PUBLIC_LANGGRAPH_API_URL` | **浏览器端**（JavaScript 代码在用户浏览器运行） | 宿主机可达地址 `localhost:2026` |
| `NEXT_PUBLIC_API_URL` | **Next.js 服务端**（`next.config.mjs` 中的 rewrites） | Docker 内部可达地址 `backend:3001` |
| `NEXT_PUBLIC_API_URL` | **浏览器端**（某些组件直接调用） | 宿主机可达地址 `localhost:3001` |

容器内 `127.0.0.1` 指向容器自己，`host.docker.internal` 指向宿主机但浏览器不认识它。

### 第五步：检查前端代码

查看 `ui/lib/langgraph/config.ts`：

```typescript
const deploymentUrl = process.env.NEXT_PUBLIC_LANGGRAPH_API_URL;
```

LangGraph SDK 在前端运行时直接用这个 URL 发起 fetch，浏览器解析这个域名 → 如果值是 `host.docker.internal`，浏览器不认识 → `ERR_NAME_NOT_RESOLVED`。

查看 `ui/next.config.mjs`：

```javascript
const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
// 用同一个变量做服务端代理转发
```

`NEXT_PUBLIC_API_URL` 同时服务端用（代理转发）和浏览器用（直接调用），需要拆分。

---

## 解决方案

### 修复一：分离服务端内部地址与浏览器端地址

修改 `next.config.mjs`，使用独立的环境变量 `API_SERVER_INTERNAL_URL` 用于服务端代理，不再复用 `NEXT_PUBLIC_API_URL`：

```javascript
// next.config.mjs
const apiUrl = process.env.API_SERVER_INTERNAL_URL || "http://backend:3001";
```

### 修复二：docker-compose.yml 配置正确地址

```
frontend 容器:
  NEXT_PUBLIC_LANGGRAPH_API_URL=http://localhost:2026     # 浏览器调 LangGraph
  NEXT_PUBLIC_API_URL=http://localhost:3001               # 浏览器调后端（直接调用场景）
  API_SERVER_INTERNAL_URL=http://backend:3001             # 服务端代理调后端
```

- `localhost` → 浏览器可解析，指向宿主机
- `backend` → Docker 内部 DNS 可解析，指向后端容器

### 修复三：重建容器使配置生效

```bash
# 修改 next.config.mjs 需要重建镜像
docker-compose build frontend

# 修改环境变量需要重新创建容器
docker-compose up -d --force-recreate frontend
```

---

## 修复后验证

| 测试项 | 结果 |
|--------|------|
| 后端 API 直连 | ✅ 200 |
| 前端代理 `/api/v2/projects` | ✅ 200 |
| LangGraph `/info` | ✅ 200 |
| LangGraph 创建 Run | ✅ 成功返回 run_id |
| 前端 HTML 加载 | ✅ 200 |
| 前端日志无连接错误 | ✅ 无报错 |

---

## 经验教训

1. **`NEXT_PUBLIC_` 前缀的含义**：Next.js 中带此前缀的变量会被编译进浏览器端 JS bundle，必须在浏览器可访问的地址
2. **Docker 网络三层独立**：宿主机浏览器、Docker 容器内、容器间 DNS，各自有独立的地址空间
3. **同一个变量不同用途要拆分**：服务端代理地址和浏览器端地址是两回事，不能复用同一个环境变量
4. **容器环境变量不会热更新**：修改 `docker-compose.yml` 后需要 `--force-recreate`；修改 `next.config.mjs` 后需要 `build`
