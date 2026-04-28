---
title: 安装和启动
description: 安装依赖并启动 AtlasClaw Core。
sidebar_position: 3
---

# 安装和启动

## 安装依赖 {#install-dependencies}

在 AtlasClaw Core 仓库中执行：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

前端开发依赖：

```bash
cd app/frontend
npm install
npm run build
```

## 启动服务 {#start-the-service}

在组合仓库中推荐使用前台启动脚本：

```bash
atlasclaw-share/scripts/restart-atlasclaw-core-foreground.sh
```

也可以直接启动 FastAPI：

```bash
uvicorn app.atlasclaw.main:app --reload --host 0.0.0.0 --port 8000
```

Web UI 由同一个后端提供，访问 `http://127.0.0.1:8000/`。

## 默认本地管理员 {#default-local-admin}

启用本地认证时，如果默认管理员不存在，AtlasClaw 会创建它。默认开发账号通常是 `admin` / `admin`。
