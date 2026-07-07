-- 预创建 langgraph 迁移所需的 PostgreSQL 扩展
-- 此脚本在数据库首次初始化时以超级用户身份执行
CREATE EXTENSION IF NOT EXISTS btree_gin;
CREATE EXTENSION IF NOT EXISTS ltree;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
