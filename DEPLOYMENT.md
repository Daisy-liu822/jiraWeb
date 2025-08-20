# 部署说明

## 🚂 Railway 部署 (推荐 - 无需信用卡)

### 步骤：
1. 访问 [Railway.app](https://railway.app)
2. 使用GitHub账户登录
3. 点击 "Start a New Project"
4. 选择 "Deploy from GitHub repo"
5. 选择你的 `jiraWeb` 仓库
6. 等待自动部署完成

### 优点：
- ✅ 无需信用卡验证
- ✅ 每月有免费额度
- ✅ 部署简单快速
- ✅ 支持Python应用

---

## 🌐 Render 部署

### 自动部署（推荐）

1. 确保你的代码已经推送到GitHub
2. 访问 [Render.com](https://render.com) 并注册/登录
3. 点击 "New +" 选择 "Web Service"
4. 连接你的GitHub账户
5. 选择 `jiraWeb` 仓库
6. 配置部署：
   - **Name**: `jira-web-app`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `bash start.sh`
   - **Plan**: `Free`

### 手动部署

如果自动部署不工作，可以手动配置：

1. 在Render中创建新的Web Service
2. 选择你的GitHub仓库
3. 设置环境变量：
   - `PYTHON_VERSION`: `3.9.16`
4. 设置构建命令：`pip install -r requirements.txt`
5. 设置启动命令：`bash start.sh`

---

## 🚀 Fly.io 部署

### 步骤：
1. 安装Fly CLI: `curl -L https://fly.io/install.sh | sh`
2. 登录: `fly auth login`
3. 创建应用: `fly launch`
4. 部署: `fly deploy`

---

## 📱 Deta Space 部署

### 步骤：
1. 访问 [Deta.space](https://deta.space)
2. 使用GitHub登录
3. 创建新项目
4. 连接GitHub仓库

---

## 部署后

部署完成后，平台会提供一个公共URL，你可以通过该URL访问你的JIRA Web应用。

## 注意事项

- 免费计划有使用限制
- 应用会在一定时间无活动后休眠
- 首次访问可能需要等待几秒钟启动
- 确保你的JIRA API Token在部署后仍然有效 