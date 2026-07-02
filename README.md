安装及注意事项：
一、安装依赖
1、新建uv 环境（python 3.13），将当前目录下所有代码复制到项目目录下
2、安装后端依赖，打开终端界面，输入 uv sync
3、安装前端依赖并运行，打开终端界面，cd ui 进入ui目录，然后执行 npm install，然后执行npm run dev
4、编辑根目录下的 .env文件，修改相应的api key及相关服务器地址

启动后端服务：
注意：
如果使用 start_server_inmem.py 启动服务，必须将langgraph_api 随意命名一下，例如修改成 langgraph_api_1

如果使用 start_server_postgres.py 启动服务，按照如下进行操作：
0、安装依赖：uv sync
1、langgraph_api、langgraph_license、langgraph_runtime_postgres 这三个文件保持在当前目录下不动
2、将langgraph_source/checkpoint/postgres 复制到 .venv/lib/langgraph/checkpoint 目录下
3、将langgraph_source/store/postgres 复制到 .venv/lib/langgraph/store 目录下
4、openapi.json 要和langgraph_api在一起，不能删除
5、storage目录下是数据库创建脚本，默认不动
6、可以在langgraph.json文件中配置智能体
7、根据自己的情况修改.env文件中的如下信息：
    DEEPSEEK_API_KEY=your-api-key-here
    REDIS_URI=redis://localhost:6379/0
    DATABASE_URI=postgres://postgres:password@localhost:5432/db

启动自定义的后端登录及注册系统的目录：直接运行 app/main.py


# 启动全部
docker compose up -d

# 查看日志
docker compose logs -f

# 停止全部
docker compose down

# 重建某个服务
docker compose build backend
docker compose up -d backend

