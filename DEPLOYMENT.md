# 部署到 Render

## 自动部署（推荐）

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

## 手动部署

如果自动部署不工作，可以手动配置：

1. 在Render中创建新的Web Service
2. 选择你的GitHub仓库
3. 设置环境变量：
   - `PYTHON_VERSION`: `3.9.16`
4. 设置构建命令：`pip install -r requirements.txt`
5. 设置启动命令：`bash start.sh`

## 部署后

部署完成后，Render会提供一个公共URL，你可以通过该URL访问你的JIRA Web应用。

## 注意事项

- 免费计划有使用限制
- 应用会在15分钟无活动后休眠
- 首次访问可能需要等待几秒钟启动 