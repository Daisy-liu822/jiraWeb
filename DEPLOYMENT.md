# 部署说明

## 🚀 Deta Space 部署 (最推荐 - 完全免费，无需信用卡)

### 步骤：
1. 访问 [Deta.space](https://deta.space)
2. 使用GitHub账户登录
3. 点击 "Create a new project"
4. 选择 "Micro" 类型
5. 连接你的GitHub仓库 `jiraWeb`
6. 配置部署：
   - **Name**: `jira-web-app`
   - **Engine**: `Python 3.9`
   - **Run Command**: `streamlit run web_app.py --server.port 8080 --server.address 0.0.0.0`
7. 点击 "Deploy"

### 优点：
- ✅ **完全免费，无需信用卡**
- ✅ **无使用限制**
- ✅ **部署简单快速**
- ✅ **支持Python应用**
- ✅ **自动HTTPS**

---

## 🚂 Railway 部署 (需要信用卡验证)

### 步骤：
1. 访问 [Railway.app](https://railway.app)
2. 使用GitHub账户登录
3. 点击 "Start a New Project"
4. 选择 "Deploy from GitHub repo"
5. 选择你的 `jiraWeb` 仓库
6. 等待自动部署完成

### 注意：
- ⚠️ 需要信用卡验证
- ⚠️ 有试用期限制

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

### 注意：
- ⚠️ 需要信用卡验证

---

## 🚀 Fly.io 部署

### 步骤：
1. 安装Fly CLI: `curl -L https://fly.io/install.sh | sh`
2. 登录: `fly auth login`
3. 创建应用: `fly launch`
4. 部署: `fly deploy`

### 注意：
- ⚠️ 需要信用卡验证

---

## 📱 本地部署 (完全免费)

### 步骤：
1. 安装Python 3.9+
2. 安装依赖: `pip install -r requirements.txt`
3. 运行应用: `streamlit run web_app.py`
4. 访问: `http://localhost:8501`

### 优点：
- ✅ **完全免费**
- ✅ **无限制**
- ✅ **快速开发调试**

---

## 部署后

部署完成后，平台会提供一个公共URL，你可以通过该URL访问你的JIRA Web应用。

## 注意事项

- 免费计划有使用限制
- 应用会在一定时间无活动后休眠
- 首次访问可能需要等待几秒钟启动
- 确保你的JIRA API Token在部署后仍然有效

## 🎯 推荐顺序

1. **Deta Space** - 完全免费，无需信用卡
2. **本地部署** - 开发和测试用
3. **其他平台** - 需要信用卡验证 