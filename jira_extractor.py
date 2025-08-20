# jira_extractor.py
import requests
import json
import csv
import os
import logging
from datetime import datetime
from typing import List, Dict, Optional

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JiraExtractor:
    def __init__(self, base_url: str, api_token: str, email: str):
        self.base_url = base_url.rstrip('/')
        self.api_token = api_token
        self.email = email
        self.session = requests.Session()
        self.session.auth = (email, api_token)
        self.session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
        
        # 加载项目映射配置
        self.project_mappings = self._load_project_mappings()

    def _load_project_mappings(self) -> Dict[str, List[str]]:
        """加载项目映射配置"""
        try:
            mapping_file = "project_mapping.json"
            if os.path.exists(mapping_file):
                with open(mapping_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return config.get('project_mappings', {})
            else:
                logger.warning(f"项目映射文件 {mapping_file} 不存在，使用默认映射")
                return {
                    "aca": ["aca-cn"],
                    "public-api": ["public-api-job"]
                }
        except Exception as e:
            logger.error(f"加载项目映射失败: {e}")
            return {}

    def _apply_project_mappings(self, projects: List[str]) -> List[str]:
        """应用项目映射，添加关联项目"""
        if not self.project_mappings:
            return projects
        
        expanded_projects = projects.copy()
        
        for project in projects:
            project_lower = project.lower().strip()
            
            # 检查是否有映射规则
            for source_project, target_projects in self.project_mappings.items():
                if source_project.lower() in project_lower or project_lower in source_project.lower():
                    # 添加关联项目
                    for target_project in target_projects:
                        if target_project not in expanded_projects:
                            expanded_projects.append(target_project)
                            logger.info(f"添加关联项目: {source_project} -> {target_project}")
        
        return expanded_projects

    def find_affects_project_field_id(self, filter_id: str) -> Optional[str]:
        """查找Affects Project字段ID"""
        try:
            url = f"{self.base_url}/rest/api/3/search"
            params = {
                'jql': f'filter={filter_id}',
                'fields': 'summary,key',
                'maxResults': 10,
                'startAt': 0
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            issues = response.json().get('issues', [])
            
            if not issues:
                logger.warning("过滤器中没有找到问题")
                return None
            
            potential_fields = []

            for issue in issues:
                issue_key = issue.get('key', '')
                issue_url = f"{self.base_url}/rest/api/3/issue/{issue_key}?expand=names"
                issue_data = self.session.get(issue_url).json()
                fields = issue_data.get('fields', {})
                names = issue_data.get('names', {})

                for field_id, value in fields.items():
                    if field_id.startswith('customfield_') and value:
                        field_name = names.get(field_id, 'N/A')
                        if any(kw in field_name.lower() or (isinstance(value, str) and kw in value.lower())
                               for kw in ['service', 'cloud', 'legacy', 'web', 'api', 'project']):
                            return field_id

        except Exception as e:
            logger.error(f"字段识别失败: {e}")
        return None

    def extract_projects_from_filter(self, filter_id, custom_field_id: str = None) -> List[Dict]:
        field_client = JiraExtractor(self.base_url, self.api_token, self.email)

        return field_client.get_affects_projects(filter_id, custom_field_id)

    def get_affects_projects(self, filter_id, custom_field_id: Optional[str]) -> List[Dict]:
        url = f"{self.base_url}/rest/api/3/search"
        fields = ["summary", "key", "status"]
        if custom_field_id:
            fields.append(custom_field_id)

        params = {
            'jql': f'filter={filter_id}',
            'fields': ','.join(fields),
            'maxResults': 1000,
            'startAt': 0
        }

        response = self.session.get(url, params=params)
        response.raise_for_status()
        issues = response.json().get('issues', []) or []
        return self._extract_affects_projects(issues, custom_field_id)

    def _extract_affects_projects(self, issues: List[Dict], custom_field_id: Optional[str]) -> List[Dict]:
        results = []
        for issue in issues:
            fields = issue.get('fields', {})
            issue_key = issue.get('key', '')
            summary = fields.get('summary', '')
            status = fields.get('status', {}).get('name', '')

            affects_projects_str = ""
            affects_projects = []

            if custom_field_id:
                affects_project_raw = fields.get(custom_field_id)
                affects_projects_str, affects_projects = self._process_field_value(affects_project_raw)
                
                # 应用项目映射
                if affects_projects:
                    affects_projects = self._apply_project_mappings(affects_projects)
                    # 重新生成字符串表示
                    affects_projects_str = ", ".join(affects_projects)

            results.append({
                'issue_key': issue_key,
                'summary': summary,
                'status': status,
                'affects_projects': affects_projects,
                'affects_projects_raw': affects_projects_str
            })
        return results

    def _process_field_value(self, field_val):
        if isinstance(field_val, str):
            val = field_val.strip()
            return val, [p.strip() for p in val.split(",") if p.strip() and p.strip().upper() != "NA"]
        elif isinstance(field_val, list):
            val = ", ".join([str(i.get('value') if isinstance(i, dict) else i) for i in field_val])
            return val, [str(i.get('value') if isinstance(i, dict) else i).strip() for i in field_val]
        elif isinstance(field_val, dict):
            val = str(field_val.get('value', field_val.get('name', '')))
            return val, [val.strip()]
        else:
            return "", []

    def save_results_to_file(self, results: List[Dict]):
        results_dir = "results"
        os.makedirs(results_dir, exist_ok=True)

        prefix = f"jira_affects_projects_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        json_path = os.path.join(results_dir, f"{prefix}.json")
        csv_path = os.path.join(results_dir, f"{prefix}.csv")
        
        # 保存JSON文件
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        # 准备CSV数据，确保列名匹配
        csv_data = []
        for result in results:
            csv_row = {
                'issue_key': result.get('issue_key', ''),
                'summary': result.get('summary', ''),
                'status': result.get('status', ''),
                'affects_projects_raw': result.get('affects_projects_raw', ''),
                'affects_projects_count': len(result.get('affects_projects', []))
            }
            csv_data.append(csv_row)
        
        # 保存CSV文件
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            if csv_data:
                fieldnames = list(csv_data[0].keys())
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(csv_data)
        
        return json_path, csv_path

    def get_project_mappings(self) -> Dict[str, List[str]]:
        """获取当前项目映射配置"""
        return self.project_mappings.copy()

    def update_project_mappings(self, new_mappings: Dict[str, List[str]]) -> bool:
        """更新项目映射配置"""
        try:
            config = {
                "project_mappings": new_mappings,
                "description": "当检测到左侧项目时，自动添加右侧的关联项目到结果中",
                "version": "1.0.0",
                "last_updated": datetime.now().strftime("%Y-%m-%d")
            }
            
            with open("project_mapping.json", "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            
            # 更新内存中的配置
            self.project_mappings = new_mappings
            return True
        except Exception as e:
            logger.error(f"更新项目映射失败: {e}")
            return False
