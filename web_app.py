# web_app.py
import streamlit as st
import os
import pandas as pd
from jira_extractor import JiraExtractor

st.set_page_config(page_title="Jira Affects Project 提取工具", layout="wide")

st.title("📊 Jira Affects Project 提取工具")
st.markdown("输入你的配置并点击按钮，即可一键提取影响的项目列表并下载。")

# 侧边栏配置
with st.sidebar:
    st.header("⚙️ 配置设置")
    base_url = st.text_input("🌐 Jira 实例 URL", value="https://qima.atlassian.net")
    api_token = st.text_area("🔐 API Token", value="your_api_token_here", height=100, help="从Atlassian账户设置中获取API Token")
    email = st.text_input("📧 Jira 邮箱", value="daisy.liu@qima.com")
    filter_id = st.text_input("🔍 过滤器 ID", value="20334")
    
    # 字段ID输入，支持自动检测和手动输入
    st.subheader("🏷️ Affects Project 字段 ID")
    field_id = st.text_input("字段ID", value="", help="留空可自动检测，或手动输入")
    
    # 显示当前检测到的字段ID
    if 'detected_field_id' in st.session_state:
        st.success(f"✅ 已检测: {st.session_state.detected_field_id}")
        if not field_id:
            field_id = st.session_state.detected_field_id

# 主界面
st.header("🚀 操作面板")

# 步骤指示器
st.markdown("""
### 📋 使用步骤：
1. **🔧 配置信息** (左侧边栏)
2. **🔍 检测字段ID** (下方按钮)
3. **🚀 提取数据** (检测成功后)
""")

col1, col2 = st.columns(2)

with col1:
    auto_detect_button = st.button("🔍 自动检测字段 ID", key="auto", use_container_width=True, type="primary")

with col2:
    run_button = st.button("🚀 开始提取数据", key="run", use_container_width=True, disabled=not field_id and 'detected_field_id' not in st.session_state)

# 自动检测字段ID
if auto_detect_button:
    if api_token == "your_api_token_here":
        st.error("❌ 请先输入有效的API Token")
    else:
        try:
            with st.spinner("🔍 正在识别 Affects Project 字段 ID..."):
                jira_client = JiraExtractor(base_url, api_token, email)
                detected_field_id = jira_client.find_affects_project_field_id(filter_id)
                if detected_field_id:
                    st.success(f"✅ 成功识别字段: `{detected_field_id}`")
                    st.session_state.detected_field_id = detected_field_id
                    st.rerun()  # 刷新页面以更新UI
                else:
                    st.warning("⚠️ 未自动识别字段 ID，请手动输入。")
        except Exception as e:
            st.error(f"❌ 检测失败: {str(e)}")
            st.info("💡 提示：请检查API Token、邮箱和过滤器ID是否正确")

# 提取数据
if run_button:
    # 确定使用的字段ID
    current_field_id = field_id or st.session_state.get('detected_field_id', '')
    
    if api_token == "your_api_token_here":
        st.error("❌ 请先输入有效的API Token")
    elif not current_field_id:
        st.error("❌ 请先输入或检测 Affects Project 字段 ID")
        st.info("💡 提示：点击'自动检测字段ID'按钮，或手动输入字段ID")
    else:
        try:
            jira_client = JiraExtractor(base_url, api_token, email)
            
            with st.spinner("🔄 正在从 Jira 获取数据..."):
                results = jira_client.get_affects_projects(filter_id, current_field_id)

            if results:
                st.success(f"✅ 成功提取 {len(results)} 个问题！")
                st.subheader("🔍 获取的数据预览")
                
                df = pd.DataFrame(results)
                st.dataframe(df.head(50), use_container_width=True)
                
                # 下载功能
                json_path, csv_path = jira_client.save_results_to_file(results)
                
                col1, col2 = st.columns(2)
                with open(json_path, "r", encoding="utf-8") as f:
                    col1.download_button(
                        "📥 下载 JSON", 
                        f.read(), 
                        file_name=os.path.basename(json_path), 
                        mime="application/json"
                    )
                with open(csv_path, "r", encoding="utf-8") as f:
                    col2.download_button(
                        "📎 下载 CSV", 
                        f.read(), 
                        file_name=os.path.basename(csv_path), 
                        mime="text/csv"
                    )
            else:
                st.info("📭 没有找到匹配的数据")
                
        except Exception as e:
            st.error(f"❌ 提取失败: {str(e)}")

# 使用说明
with st.expander("📖 详细使用说明"):
    st.markdown("""
    ### 🔧 配置步骤：
    1. **获取API Token**: 访问 [Atlassian账户设置](https://id.atlassian.com/manage-profile/security/api-tokens)
    2. **输入JIRA信息**: 填写你的JIRA实例URL、邮箱和过滤器ID
    3. **自动检测字段**: 点击"自动检测字段ID"按钮
    4. **提取数据**: 点击"开始提取数据"按钮
    
    ### 🏷️ 关于字段ID：
    - **Affects Project** 是JIRA中的自定义字段，标识问题影响的项目
    - 每个JIRA实例的字段ID可能不同
    - 建议先使用自动检测功能
    - 如果检测失败，可以手动查找字段ID
    
    ### 📋 注意事项：
    - 确保API Token有效且有足够权限
    - 过滤器ID必须是有效的JIRA过滤器
    - 首次使用建议先测试连接
    - 字段ID检测成功后，提取数据按钮才会启用
    """)

# 状态信息
if 'detected_field_id' in st.session_state:
    st.info(f"🔍 当前检测到的字段ID: {st.session_state.detected_field_id}")
    if not field_id:
        st.warning("⚠️ 请在上方输入框中确认字段ID，或直接使用检测到的ID")
