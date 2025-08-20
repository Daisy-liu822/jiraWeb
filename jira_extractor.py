# jira_extractor.py
import requests
import json
import csv
from typing import List, Dict, Optional
from datetime import datetime
import os
import logging

logger = logging.getLogger("jira_extractor")

class JiraExtractor:
    def __init__(self, base_url: str, api_token: str, email: str = None):
        self.base_url = base_url
        self.api_token = api_token
        self.email = email
        self.session = requests.Session()
        
        if email:
            self.session.auth = (email, api_token)
        else:
            self.session.headers.update({
                'Authorization': f'Bearer {api_token}',
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            })

    def find_affects_project_field_id(self, filter_id) -> Optional[str]:
        try:
            search_url = f"{self.base_url}/rest/api/3/search"
            params = {'jql': f'filter={filter_id}', 'fields': 'key', 'maxResults': 5}
            response = self.session.get(search_url, params=params)
            response.raise_for_status()
            data = response.json()

            issues = data.get('issues', [])
            if not issues:
                logger.info("过滤器没有返回问题")
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
        
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["issue_key", "summary", "status", "affects_projects_raw"])
            writer.writeheader()
            writer.writerows(results)
        
        return json_path, csv_path
