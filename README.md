# 💻 Jira Affects Project 提取工具 - 网页版

适合有需要登陆 Jira 获取影响项目字段的用户，可以通过网页输入自己的配置运行分析。

## 🔧 可配置项

- Jira 实例地址
- API Token
- 邮箱地址（可选）
- 过滤器 ID

## 🎯 出发点

- 用户只需要点击 "运行" 即可触发提取并展示网页结果
- 结果支持下载 CSV/JSON

## ▶️ 本地运行方法

```bash
pip install -r requirements.txt
streamlit run web_app.py
