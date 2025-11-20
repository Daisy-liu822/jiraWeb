"""
ArgoCD 镜像查询 Streamlit 页面
"""

import streamlit as st
import pandas as pd
import json
import sys
import os
from datetime import datetime

# 添加 modules 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.argocd_client import ArgoCDClient

# 页面配置
st.set_page_config(
    page_title="ArgoCD 镜像查询",
    page_icon="🐳",
    layout="wide"
)

# 配置文件路径
CONFIG_FILE = "config/argocd_config.json"

# 默认配置
DEFAULT_CONFIG = {
    'environment': 'preprod',
    'token': '',
    'services': []
}


# 加载配置
def load_config():
    """加载配置文件"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                for key in DEFAULT_CONFIG:
                    if key not in config:
                        config[key] = DEFAULT_CONFIG[key]
                return config
    except Exception as e:
        st.error(f"加载配置失败: {e}")
    return DEFAULT_CONFIG.copy()


# 保存配置
def save_config(config):
    """保存配置文件"""
    try:
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        # 不保存 token 到文件
        config_to_save = config.copy()
        config_to_save['token'] = ''
        
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config_to_save, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"保存配置失败: {e}")
        return False


# 对比功能函数
def compare_results(current_results, previous_results):
    """对比当前结果与上次结果"""
    if not previous_results or 'success' not in previous_results:
        return None
    
    comparison = {
        "added": {},      # 新增的服务
        "updated": {},    # 更新的服务（镜像标签变化）
        "unchanged": {},  # 未变化的服务
        "removed": {}     # 移除的服务
    }
    
    current_services = current_results.get('success', {})
    previous_services = previous_results.get('success', {})
    
    # 对比逻辑
    all_services = set(current_services.keys()) | set(previous_services.keys())
    
    for service in all_services:
        current_version = current_services.get(service)
        previous_version = previous_services.get(service)
        
        if current_version and previous_version:
            if current_version != previous_version:
                comparison["updated"][service] = {
                    "previous": previous_version,
                    "current": current_version
                }
            else:
                comparison["unchanged"][service] = current_version
        elif current_version and not previous_version:
            comparison["added"][service] = current_version
        elif not current_version and previous_version:
            comparison["removed"][service] = previous_version
    
    return comparison


def highlight_comparison(row, comparison):
    """为 DataFrame 行添加高亮样式"""
    service_name = row['service']
    
    if comparison:
        if service_name in comparison.get('added', {}):
            return ['background-color: #d4edda; color: #155724'] * len(row)  # 绿色 - 新增
        elif service_name in comparison.get('updated', {}):
            return ['background-color: #fff3cd; color: #856404'] * len(row)  # 黄色 - 更新
        elif service_name in comparison.get('removed', {}):
            return ['background-color: #f8d7da; color: #721c24'] * len(row)  # 红色 - 移除
    
    return [''] * len(row)  # 无变化


# 初始化 session state
if 'argocd_config' not in st.session_state:
    st.session_state.argocd_config = load_config()

if 'query_results' not in st.session_state:
    st.session_state.query_results = None

if 'previous_results' not in st.session_state:
    st.session_state.previous_results = None

if 'last_query_time' not in st.session_state:
    st.session_state.last_query_time = None

if 'comparison_data' not in st.session_state:
    st.session_state.comparison_data = None


# 主标题
st.title("🐳 ArgoCD 镜像查询工具")
st.markdown("查询和追踪 ArgoCD 应用部署的容器镜像版本")

# 网络限制提示
st.info("""
💡 **使用提示**

ArgoCD 服务器位于公司内网。如果在线版本无法访问，请使用本地版本。

**本地运行方法：**
- 🖱️ **Windows 用户**：双击项目中的 `启动ArgoCD工具.bat` 文件
- 💻 **命令行运行**：`streamlit run app.py`
- 📥 **首次使用**：需要先 `git clone` 并安装依赖

本地版本无网络限制，所有功能完全可用。
""")

st.markdown("---")


# 侧边栏配置
with st.sidebar:
    st.header("⚙️ 配置设置")
    
    # 环境选择
    st.subheader("🌍 环境配置")
    environment = st.selectbox(
        "选择环境",
        ArgoCDClient.list_environments(),
        index=ArgoCDClient.list_environments().index(st.session_state.argocd_config.get('environment', 'preprod')),
        key="environment_select"
    )
    
    # 显示环境信息
    env_config = ArgoCDClient.get_environment_config(environment)
    if env_config:
        st.info(f"🔗 服务器: {env_config['server']}")
    
    # Token 输入
    st.subheader("🔐 认证设置")
    
    # 尝试从本地 ArgoCD CLI 配置读取 token
    def try_load_token_from_cli():
        """尝试从 ArgoCD CLI 配置文件读取 token"""
        try:
            import platform
            home_dir = os.path.expanduser("~")
            
            # ArgoCD CLI 配置文件路径
            if platform.system() == "Windows":
                config_path = os.path.join(home_dir, ".argocd", "config")
            else:
                config_path = os.path.join(home_dir, ".argocd", "config")
            
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    import yaml
                    config = yaml.safe_load(f)
                    
                    # 尝试找到当前环境的 token
                    contexts = config.get('contexts', [])
                    for context in contexts:
                        if environment in context.get('server', ''):
                            return context.get('user', {}).get('auth-token', '')
                    
                    # 如果没有找到特定环境，返回第一个 token
                    if contexts and 'user' in contexts[0]:
                        return contexts[0].get('user', {}).get('auth-token', '')
        except Exception:
            pass
        return None
    
    # 尝试自动加载 token
    auto_token = try_load_token_from_cli()
    
    if auto_token and not st.session_state.get('user_entered_token', False):
        st.success("✅ 已从 ArgoCD CLI 配置自动加载 Token")
        token = auto_token
    else:
        token = st.text_input(
            "ArgoCD Bearer Token",
            type="password",
            help="输入您的 ArgoCD Token（不含 Bearer 前缀）",
            key="token_input"
        )
        if token:
            st.session_state['user_entered_token'] = True
    
    # Token 验证
    if token:
        try:
            client = ArgoCDClient(environment, token)
            is_valid, message = client.validate_token()
            
            if is_valid:
                st.success(f"✅ {message}")
            else:
                st.error(f"❌ {message}")
                st.info("💡 如需获取新 Token，请访问 ArgoCD Web 界面")
        except Exception as e:
            st.error(f"❌ Token 验证失败: {str(e)}")
    else:
        st.warning("⚠️ 请输入 ArgoCD Token")
    
    # Token 获取帮助
    with st.expander("📖 如何获取 Token？"):
        st.markdown("""
        ### 获取 ArgoCD Token 步骤：
        1. 访问 ArgoCD Web 界面
        2. F12 打开开发者工具
        3. 选择 **Application** 标签
        4. 刷新页面
        5. 找到 **argocd.token** 的value值
        6. 粘贴到左侧输入框
        """)
    
    st.markdown("---")
    
    # 服务列表管理
    st.subheader("📋 服务列表")
    
    # 预定义服务列表
    predefined_services = [
        "aims-service-cloud",
        "aims-web-cloud",
        "aca-new",
        "program-service-cloud",
        "program-web-cloud",
        "lt-external-service-cloud"
    ]
    
    # 显示预定义服务选择
    st.markdown("**常用服务：**")
    selected_predefined = st.multiselect(
        "选择常用服务",
        predefined_services,
        default=st.session_state.argocd_config.get('services', []),
        key="predefined_services"
    )
    
    # 自定义服务输入
    st.markdown("**自定义服务：**")
    custom_services = st.text_area(
        "输入服务名称（每行一个）",
        height=100,
        help="输入服务名称，不含环境前后缀",
        key="custom_services"
    )
    
    # 合并服务列表
    services_list = list(selected_predefined)
    if custom_services:
        custom_list = [s.strip() for s in custom_services.split('\n') if s.strip()]
        services_list.extend(custom_list)
    
    # 去重
    services_list = list(dict.fromkeys(services_list))
    
    st.info(f"📊 已选择 {len(services_list)} 个服务")
    
    st.markdown("---")
    
    # 配置管理
    st.subheader("💾 配置管理")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💾 保存", use_container_width=True):
            config = {
                'environment': environment,
                'services': services_list
            }
            if save_config(config):
                st.session_state.argocd_config = config
                st.success("✅ 配置已保存")
    
    with col2:
        if st.button("🔄 重置", use_container_width=True):
            st.session_state.argocd_config = DEFAULT_CONFIG.copy()
            save_config(DEFAULT_CONFIG)
            st.success("🔄 配置已重置")
            st.rerun()


# 主区域
st.header("🚀 镜像查询")

# 操作说明
st.markdown("""
### 📋 操作步骤：
1. **配置环境** - 在左侧选择目标环境（preprod/staging/prod）
2. **输入 Token** - 输入您的 ArgoCD Token
3. **选择服务** - 选择要查询的服务列表
4. **开始查询** - 点击下方按钮开始查询
""")

st.markdown("---")

# 查询按钮
col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    query_button = st.button(
        "🚀 开始查询镜像版本",
        type="primary",
        use_container_width=True,
        disabled=not (token and services_list)
    )

# 执行查询
if query_button:
    if not token:
        st.error("❌ 请先输入 ArgoCD Token")
    elif not services_list:
        st.error("❌ 请至少选择一个服务")
    else:
        try:
            # 创建客户端
            client = ArgoCDClient(environment, token)
            
            # 显示查询进度
            st.subheader(f"🔍 查询 {environment.upper()} 环境")
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            results = {
                'success': {},
                'failed': {},
                'details': []
            }
            
            # 查询每个服务
            for i, service in enumerate(services_list):
                status_text.text(f"正在查询: {service} ({i+1}/{len(services_list)})")
                progress_bar.progress((i + 1) / len(services_list))
                
                try:
                    images = client.get_service_images(service)
                    results['success'].update(images)
                    
                    # 记录详细信息
                    for svc, tag in images.items():
                        results['details'].append({
                            'service': svc,
                            'version': tag,
                            'status': '✅ 成功',
                            'environment': environment.upper()
                        })
                        
                except Exception as e:
                    error_msg = str(e)
                    results['failed'][service] = error_msg
                    results['details'].append({
                        'service': service,
                        'version': 'N/A',
                        'status': f'❌ {error_msg[:50]}...' if len(error_msg) > 50 else f'❌ {error_msg}',
                        'environment': environment.upper()
                    })
            
            # 执行对比（如果有上次结果）
            comparison = None
            if st.session_state.previous_results:
                comparison = compare_results(results, st.session_state.previous_results)
                st.session_state.comparison_data = comparison
            
            # 保存结果
            st.session_state.previous_results = st.session_state.query_results  # 保存旧结果
            st.session_state.query_results = results
            st.session_state.last_query_time = datetime.now()
            
            # 清空进度显示
            status_text.empty()
            progress_bar.empty()
            
            # 显示成功提示
            if comparison:
                total_changes = len(comparison['added']) + len(comparison['updated']) + len(comparison['removed'])
                if total_changes > 0:
                    st.success(f"✅ 查询完成！发现 {total_changes} 个变化")
                else:
                    st.success(f"✅ 查询完成！无变化")
            else:
                st.success(f"✅ 查询完成！成功: {len(results['success'])}, 失败: {len(results['failed'])}")
            
        except Exception as e:
            st.error(f"❌ 查询失败: {str(e)}")


# 显示查询结果
if st.session_state.query_results:
    results = st.session_state.query_results
    
    st.markdown("---")
    st.subheader("📊 查询结果")
    
    # 统计信息
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🎯 查询服务数", len(services_list))
    
    with col2:
        st.metric("✅ 成功", len(results['success']))
    
    with col3:
        st.metric("❌ 失败", len(results['failed']))
    
    with col4:
        success_rate = len(results['success']) / len(services_list) * 100 if services_list else 0
        st.metric("📈 成功率", f"{success_rate:.1f}%")
    
    # 结果表格
    if results['details']:
        st.markdown("### 📝 详细结果")
        
        # 如果有对比数据，显示对比分析
        comparison = st.session_state.comparison_data
        if comparison:
            total_changes = len(comparison['added']) + len(comparison['updated']) + len(comparison['removed'])
            
            if total_changes > 0:
                st.markdown("#### 🔍 部署对比分析")
                
                # 变化统计
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("🆕 新增", len(comparison['added']), delta=len(comparison['added']) if len(comparison['added']) > 0 else None)
                with col2:
                    st.metric("🔄 更新", len(comparison['updated']), delta=len(comparison['updated']) if len(comparison['updated']) > 0 else None)
                with col3:
                    st.metric("✅ 不变", len(comparison['unchanged']))
                with col4:
                    st.metric("🗑️ 移除", len(comparison['removed']), delta=-len(comparison['removed']) if len(comparison['removed']) > 0 else None, delta_color="inverse")
                
                st.markdown("---")
                
                # 显示具体变化
                if comparison['updated']:
                    with st.expander(f"🔄 更新的服务 ({len(comparison['updated'])} 个)", expanded=True):
                        for service, versions in sorted(comparison['updated'].items()):
                            st.warning(f"""
                            **{service}**  
                            📜 之前: `{versions['previous']}`  
                            🆕 现在: `{versions['current']}`
                            """)
                
                if comparison['added']:
                    with st.expander(f"🆕 新增的服务 ({len(comparison['added'])} 个)", expanded=False):
                        for service, version in sorted(comparison['added'].items()):
                            st.success(f"**{service}**: `{version}`")
                
                if comparison['removed']:
                    with st.expander(f"🗑️ 移除的服务 ({len(comparison['removed'])} 个)", expanded=False):
                        for service, version in sorted(comparison['removed'].items()):
                            st.error(f"**{service}**: `{version}` (已移除)")
        
        # 显示数据表格（带高亮）
        st.markdown("#### 📋 完整服务列表")
        df = pd.DataFrame(results['details'])
        
        # 如果有对比数据，应用高亮样式
        if comparison:
            styled_df = df.style.apply(lambda row: highlight_comparison(row, comparison), axis=1)
            st.dataframe(styled_df, use_container_width=True, hide_index=True)
            
            # 添加图例说明
            st.markdown("""
            **图例说明:**  
            🟢 绿色 = 新增服务 | 🟡 黄色 = 版本更新 | 🔴 红色 = 已移除
            """)
        else:
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.info("💡 提示：再次查询后将显示与本次结果的对比")
        
        # 导出功能
        st.markdown("---")
        st.subheader("💾 导出数据")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # CSV 导出
            csv = df.to_csv(index=False, encoding='utf-8-sig')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            st.download_button(
                "📥 下载 CSV",
                csv,
                f"argocd_images_{environment}_{timestamp}.csv",
                "text/csv",
                use_container_width=True
            )
        
        with col2:
            # JSON 导出
            json_data = {
                "environment": environment.upper(),
                "query_time": st.session_state.last_query_time.strftime("%Y-%m-%d %H:%M:%S"),
                "results": results['success'],
                "failed": results['failed']
            }
            json_str = json.dumps(json_data, ensure_ascii=False, indent=2)
            st.download_button(
                "📥 下载 JSON",
                json_str,
                f"argocd_images_{environment}_{timestamp}.json",
                "application/json",
                use_container_width=True
            )
    
    # 失败详情
    if results['failed']:
        st.markdown("---")
        st.subheader("⚠️ 失败详情")
        
        with st.expander("查看失败的服务", expanded=True):
            for service, error in results['failed'].items():
                st.error(f"**{service}**: {error}")


# 使用说明
st.markdown("---")
with st.expander("📖 使用说明和最佳实践"):
    st.markdown("""
    ### 🎯 功能特性
    
    #### 多环境支持
    - **preprod**: 预生产环境
    - **staging**: 测试环境
    - **prod**: 生产环境
    
    #### 批量查询
    - 支持一次查询多个服务
    - 自动处理失败重试
    - 详细的错误信息提示
    
    #### 数据导出
    - CSV 格式：适合 Excel 分析
    - JSON 格式：适合程序处理
    
    ### 🔐 安全说明
    
    - Token 完全隐藏，绝不显示明文
    - 配置仅保存在本地，Token 不会保存到文件
    - 符合企业最高安全标准
    
    
    ### ⚠️ 常见问题
    
    #### Q: Token 过期怎么办？
    A: 系统会自动检测，按提示重新获取即可。
    
    #### Q: 查询失败怎么办？
    A: 检查：
    - Token 是否有效
    - 网络连接是否正常
    - 服务名称是否正确
    - 是否有相应权限
    
    #### Q: 如何对比不同环境？
    A: 分别查询不同环境，导出结果后使用 Excel 或其他工具对比。
    
    #### Q: 支持自定义环境吗？
    A: 目前支持 preprod/staging/prod，如需其他环境请联系开发团队。
    """)

# 页脚
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>🐳 ArgoCD 镜像查询工具 v2.0 | Powered by Streamlit</p>
    <p>最后查询时间: {}</p>
</div>
""".format(
    st.session_state.last_query_time.strftime("%Y-%m-%d %H:%M:%S") if st.session_state.last_query_time else "未查询"
), unsafe_allow_html=True)

