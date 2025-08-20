# 🚀 Jira Affects Project 提取工具

一个基于 Streamlit 的 Jira 项目影响分析工具，帮助团队快速识别和导出问题影响的项目列表。

## ✨ 主要功能

### 🔍 核心功能
- **智能字段检测**: 自动识别 Jira 中的 "Affects Project" 字段
- **批量数据提取**: 从指定过滤器中批量提取问题数据
- **项目去重**: 自动去除重复项目，生成唯一项目列表
- **多格式导出**: 支持 JSON 和 CSV 格式下载

### 🆕 新增功能
- **项目映射**: 自动添加关联项目（如 `aca` 自动添加 `aca-cn`）
- **映射管理**: 可视化界面管理项目映射规则
- **配置持久化**: 本地文件存储配置，刷新页面后保持不变
- **智能匹配**: 支持部分匹配和模糊匹配项目名称

### 🔒 安全特性
- **API Token 保护**: 默认以密码形式输入，防止屏幕泄露
- **显示/隐藏切换**: 用户可选择是否显示完整Token
- **Token摘要显示**: 显示前4位和后4位，中间用*号隐藏
- **安全提示**: 提醒用户在安全环境下操作

### 💾 配置管理
- **本地存储**: 配置自动保存到本地 JSON 文件
- **持久化**: 即使关闭浏览器，配置也不会丢失
- **一键重置**: 支持快速恢复默认配置

## 🚀 快速开始

### 本地运行

1. **克隆项目**
```bash
git clone https://github.com/Daisy-liu822/jiraWeb.git
cd jiraWeb
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **运行应用**
```bash
streamlit run web_app.py
```

4. **访问应用**
打开浏览器访问 `http://localhost:8501`

### 在线部署

推荐使用 **Streamlit Community Cloud** 进行免费部署：

1. 访问 [Streamlit Cloud](https://streamlit.io/cloud)
2. 使用 GitHub 账号登录
3. 点击 "New app"
4. 选择 `Daisy-liu822/jiraWeb` 仓库
5. 设置应用路径为 `web_app.py`
6. 点击 "Deploy!"

## 📖 使用指南

### 🔧 配置设置

1. **获取 API Token**
   - 访问 [Atlassian 账户设置](https://id.atlassian.com/manage-profile/security/api-tokens)
   - 创建新的 API Token

2. **填写配置信息**
   - **Jira 实例 URL**: 你的 Jira 服务器地址
   - **API Token**: 从 Atlassian 获取的 Token（默认隐藏）
   - **Jira 邮箱**: 你的 Jira 账户邮箱
   - **过滤器 ID**: 要分析的 Jira 过滤器 ID

3. **自动检测字段 ID**
   - 点击 "🔍 自动检测字段 ID" 按钮
   - 系统会自动识别 "Affects Project" 字段

### 🔐 API Token 安全设置

#### 默认安全状态
- **密码输入**: Token 默认以 `••••••••` 形式显示
- **摘要显示**: 显示格式如 `ATAT******66CE7D4C`
- **自动隐藏**: 防止他人偷看屏幕时泄露

#### 显示完整 Token
- **安全切换**: 勾选 "👁️ 显示完整 Token" 复选框
- **临时显示**: 仅在需要复制时显示
- **及时隐藏**: 操作完成后取消勾选

#### 安全建议
- **公共场合**: 保持 Token 隐藏状态
- **共享屏幕**: 确保 Token 完全隐藏
- **个人环境**: 可选择显示以便操作

### 🚀 数据提取

1. **开始提取**
   - 配置完成后，点击 "🚀 开始提取数据" 按钮
   - 系统会从 Jira 获取数据并应用项目映射规则

2. **查看结果**
   - 数据预览表格
   - 去重后的项目列表
   - 项目映射应用状态

3. **下载数据**
   - JSON 格式：完整数据结构
   - CSV 格式：表格化数据，便于分析

### ⚙️ 项目映射管理

#### 🔗 映射规则
项目映射功能允许你定义规则，当检测到特定项目时自动添加关联项目：

- `aca` → 自动添加 `aca-cn`
- `public-api` → 自动添加 `public-api-job`
- `back-office` → 自动添加 `back-office-job`
- `aims-web` → 自动添加 `aims-web-job`
- `lt-external-service` → 自动添加 `lt-external-service-job`

#### 📝 管理操作
- **添加规则**: 定义新的项目映射关系
- **编辑规则**: 修改现有的映射规则
- **删除规则**: 移除不需要的映射
- **重置规则**: 恢复默认配置

#### 💡 使用示例
假设 Jira 中检测到项目 `aca`，系统会：
1. 保留原始项目 `aca`
2. 自动添加关联项目 `aca-cn`
3. 最终结果：`aca, aca-cn`

## 🏗️ 项目结构

```
jira-web-app/
├── web_app.py              # 主应用文件 (Streamlit)
├── jira_extractor.py       # Jira API 交互核心
├── project_mapping.json    # 项目映射配置文件
├── requirements.txt        # Python 依赖
├── .streamlit/            # Streamlit 配置
│   └── config.toml       # 应用配置
├── results/               # 导出结果目录
└── README.md             # 项目文档
```

## 🔧 技术架构

### 核心组件
- **Streamlit**: Web 应用框架
- **Jira REST API**: 数据获取接口
- **Pandas**: 数据处理和分析
- **JSON/CSV**: 数据导出格式

### 配置管理
- **本地文件存储**: `jira_config.json` 存储用户配置
- **项目映射**: `project_mapping.json` 存储映射规则
- **会话状态**: Streamlit session state 管理应用状态

### 安全机制
- **密码输入**: API Token 使用 `type="password"` 输入框
- **Token 掩码**: 自定义 `mask_api_token()` 函数处理显示
- **状态保护**: 配置状态和文件内容预览时自动隐藏敏感信息
- **用户控制**: 提供显示/隐藏切换选项

### 数据处理流程
1. **配置验证** → 检查 API Token 和字段 ID
2. **数据获取** → 从 Jira 批量获取问题数据
3. **项目映射** → 应用映射规则，添加关联项目
4. **数据去重** → 去除重复项目，生成唯一列表
5. **结果导出** → 生成 JSON 和 CSV 文件

## 📦 依赖要求

```txt
streamlit>=1.32.0      # Web 应用框架
requests>=2.31.0       # HTTP 请求库
pandas>=2.2.0          # 数据处理库
```

## 🌐 在线部署

### Streamlit Community Cloud
- **免费计划**: 无限制使用
- **自动部署**: 连接 GitHub 仓库自动部署
- **全球访问**: 支持全球用户访问
- **实时更新**: 代码推送后自动更新

### 部署配置
应用已配置为 Streamlit Cloud 优化：
- 服务器端口和地址设置
- 字体和错误详情配置
- 文件上传大小限制

## 🔒 安全说明

### API Token 保护
- **默认隐藏**: Token 以密码形式输入，不显示明文
- **摘要显示**: 显示前4位和后4位，中间用*号隐藏
- **用户控制**: 提供显示/隐藏切换选项
- **安全提示**: 提醒用户在安全环境下操作

### 数据隐私
- **本地存储**: 配置仅保存在本地，不会上传到云端
- **敏感信息保护**: 配置状态和文件预览时自动隐藏Token
- **访问控制**: 需要有效的 Jira 账户和权限

### 安全最佳实践
- **环境考虑**: 在公共场合或共享屏幕时保持Token隐藏
- **临时显示**: 仅在需要复制时显示完整Token
- **及时隐藏**: 操作完成后立即隐藏Token
- **定期更新**: 定期更换API Token以提高安全性

## ❓ 常见问题

### Q: 为什么需要 API Token？
A: API Token 是访问 Jira 数据的身份验证凭证，确保数据安全。

### Q: 如何找到过滤器 ID？
A: 在 Jira 中创建或查看过滤器，URL 中的数字就是过滤器 ID。

### Q: 项目映射规则如何生效？
A: 映射规则在数据提取时自动应用，修改后需要重新提取数据。

### Q: 配置丢失怎么办？
A: 配置会自动保存到本地文件，即使刷新页面也不会丢失。

### Q: 支持哪些 Jira 版本？
A: 支持 Jira Cloud 和 Jira Server 8.0+ 版本。

### Q: API Token 安全吗？
A: 非常安全！Token 默认隐藏，支持显示/隐藏切换，防止屏幕泄露。

### Q: 如何保护我的 API Token？
A: 保持默认隐藏状态，仅在安全环境下临时显示，操作完成后立即隐藏。

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

感谢 Streamlit 团队提供的优秀框架，以及 Atlassian 的 Jira API 支持。

---

**最后更新**: 2024-08-20  
**版本**: 2.1.0  
**维护者**: Daisy Liu
