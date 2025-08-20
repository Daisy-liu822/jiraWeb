# web_app.py
import streamlit as st
import os
from jira_extractor import JiraExtractor

st.set_page_config(page_title="Jira Affects Project 提取工具", layout="wide")

st.title("📊 Jira Affects Project 提取工具")
st.markdown("输入你的配置并点击按钮，即可一键提取影响的项目列表并下载。")

base_url = st.text_input("🌐 Jira 实例 URL", value="https://qima.atlassian.net")
api_token = st.text_area("🔐 API Token", value="your_api_token_here", height=100)
email = st.text_input("📧 Jira 邮箱", value="daisy.liu@qima.com")
filter_id = st.text_input("🔍 过滤器 ID", value="20334")

auto_detect_button = st.button("🔍 自动检测字段 ID", key="auto")
run_button = st.button("🚀 开始提取数据", key="run")

if auto_detect_button:
    with st.spinner("🔍 正在识别 Affects Project 字段 ID..."):
        jira_client = JiraExtractor(base_url, api_token, email)
        field_id = jira_client.find_affects_project_field_id(filter_id)
        if field_id:
            st.success(f"✅ 成功识别字段: `{field_id}`")
        else:
            st.warning("⚠️ 未自动识别字段 ID，请手动输入。")

if run_button:
    jira_client = JiraExtractor(base_url, api_token, email)
    
    with st.spinner("🔄 正在从 Jira 获取数据..."):
        field_id = jira_client.find_affects_project_field_id(filter_id)
        results = jira_client.get_affects_projects(filter_id, field_id)

    st.success(f"✅ 成功提取 {len(results)} 个问题！")
    st.subheader("🔍 获取的数据预览")

    if results:
        df = pd.DataFrame(results)
        st.dataframe(df.head(50), use_container_width=True)
    else:
        st.info("没有可展示的结果")

    json_path, csv_path = jira_client.save_results_to_file(results)

    col1, col2 = st.columns(2)
    with open(json_path, "r", encoding="utf-8") as f:
        col1.download_button("📥 下载 JSON", f.read(), file_name=os.path.basename(json_path), mime="application/json")
    with open(csv_path, "r", encoding="utf-8") as f:
        col2.download_button("📎 下载 CSV", f.read(), file_name=os.path.basename(csv_path), mime="text/csv")
