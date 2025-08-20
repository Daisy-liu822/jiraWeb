# 📊 JIRA Web 应用 - Affects Project 提取工具

一个基于Streamlit的Web应用，用于从JIRA中提取"Affects Project"字段数据，支持项目去重、数据导出和配置持久化。

## ✨ 主要功能

### 🔍 **智能数据提取**
- 自动识别JIRA中的"Affects Project"字段
- 支持自定义过滤器ID
- 批量提取问题数据

### 📋 **项目去重与展示**
- 自动去除重复项目
- 一行一个项目，方便复制
- 支持一键复制到剪贴板
- 项目数量统计

### 💾 **多格式数据导出**
- JSON格式导出
- CSV格式导出
- 自动文件命名（时间戳）

### ⚙️ **智能配置管理**
- 本地文件持久化存储
- 自动配置恢复
- 支持配置重置和清除
- 无需重复输入配置

## 🚀 快速开始

### 1. **在线使用（推荐）**
访问部署好的应用：[Streamlit Community Cloud](https://share.streamlit.io)

### 2. **本地运行**
```bash
# 克隆仓库
git clone https://github.com/Daisy-liu822/jiraWeb.git
cd jiraWeb

# 安装依赖
pip install -r requirements.txt

# 运行应用
streamlit run web_app.py
```

## 🔧 配置说明

### **必需配置**
- **JIRA实例URL**: 你的JIRA服务器地址
- **API Token**: 从Atlassian账户设置获取
- **邮箱**: JIRA账户邮箱
- **过滤器ID**: 要查询的JIRA过滤器ID

### **自动检测**
- 应用会自动检测"Affects Project"字段ID
- 无需手动查找字段配置

## 📊 使用流程

### **步骤1: 配置JIRA连接**
1. 获取API Token：[Atlassian账户设置](https://id.atlassian.com/manage-profile/security/api-tokens)
2. 输入JIRA实例信息
3. 点击"💾 保存配置"按钮

### **步骤2: 检测字段ID**
1. 点击"🔍 自动检测字段ID"按钮
2. 等待检测完成
3. 字段ID自动保存到配置

### **步骤3: 提取数据**
1. 点击"🚀 开始提取数据"按钮
2. 等待数据提取完成
3. 查看去重后的项目列表

### **步骤4: 导出数据**
1. 下载JSON格式数据
2. 下载CSV格式数据
3. 复制项目列表文本

## 🆕 最新功能

### **项目去重系统**
- 自动收集所有问题中的项目
- 智能去重和排序
- 支持多种数据格式处理

### **配置持久化**
- 本地JSON文件存储
- 浏览器刷新后配置自动恢复
- 支持配置备份和恢复

### **用户友好界面**
- 侧边栏配置面板
- 步骤指示器
- 实时状态显示
- 详细使用说明

## 📁 项目结构

```
jira-web-app/
├── web_app.py              # 主应用文件
├── jira_extractor.py       # JIRA数据提取逻辑
├── requirements.txt         # Python依赖
├── .streamlit/             # Streamlit配置
│   └── config.toml        # 服务器配置
├── jira_config.json        # 用户配置（自动生成）
└── README.md              # 项目说明
```

## 🛠️ 技术架构

### **前端框架**
- **Streamlit**: 现代化的Python Web框架
- **响应式设计**: 支持各种屏幕尺寸

### **后端逻辑**
- **JIRA REST API**: 官方API集成
- **数据处理**: 智能去重和格式化
- **文件管理**: 本地配置和数据存储

### **部署平台**
- **Streamlit Community Cloud**: 官方免费部署平台
- **自动部署**: GitHub集成，代码推送后自动更新

## 📋 依赖要求

```txt
streamlit>=1.32.0
requests>=2.31.0
pandas>=2.2.0
```

## 🌐 在线部署

### **Streamlit Community Cloud**
- ✅ 完全免费
- ✅ 无需信用卡验证
- ✅ 自动HTTPS和CDN
- ✅ 自动部署和更新

### **部署状态**
- 应用已成功部署
- 支持在线访问
- 配置自动持久化

## 🔒 安全特性

### **数据安全**
- 配置仅保存在本地
- 不向第三方服务器传输敏感信息
- API Token本地加密存储

### **访问控制**
- 支持JIRA权限验证
- 过滤器级别的数据访问控制

## 📖 使用说明

### **首次使用**
1. 访问应用并配置JIRA连接
2. 保存配置到本地文件
3. 开始数据提取

### **日常使用**
1. 应用自动加载保存的配置
2. 直接开始数据提取
3. 配置无需重复输入

### **配置管理**
- **保存配置**: 将当前配置保存到本地文件
- **重置配置**: 恢复默认配置
- **清除配置**: 删除本地配置文件

## 🆘 常见问题

### **Q: 配置丢失怎么办？**
A: 点击"🔄 重新加载配置"按钮，或检查本地配置文件

### **Q: 字段ID检测失败？**
A: 检查API Token权限，确保能访问指定的过滤器

### **Q: 数据导出失败？**
A: 检查磁盘空间，确保有写入权限

### **Q: 应用无法启动？**
A: 检查Python版本（需要3.9+）和依赖安装

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

### **开发环境设置**
```bash
git clone https://github.com/Daisy-liu822/jiraWeb.git
cd jiraWeb
pip install -r requirements.txt
streamlit run web_app.py
```

### **代码规范**
- 使用Python 3.9+语法
- 遵循PEP 8代码风格
- 添加适当的注释和文档

## 📄 许可证

本项目采用MIT许可证 - 详见 [LICENSE](LICENSE) 文件

## 📞 支持与反馈

- **GitHub Issues**: [提交问题](https://github.com/Daisy-liu822/jiraWeb/issues)
- **功能请求**: 通过Issues提交新功能建议
- **Bug报告**: 详细描述问题和复现步骤

## 🎯 开发路线图

### **已完成功能**
- ✅ JIRA数据提取
- ✅ 项目去重
- ✅ 配置持久化
- ✅ 多格式导出
- ✅ 在线部署

### **计划功能**
- 🔄 批量过滤器处理
- 🔄 数据可视化图表
- 🔄 定时自动提取
- 🔄 邮件通知功能

---

**最后更新**: 2024年8月
**版本**: 2.0.0
**维护者**: Daisy Liu
