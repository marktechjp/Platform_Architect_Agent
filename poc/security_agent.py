import os
import subprocess
import json
from langchain_core.language_models.llms import BaseLLM

class SecurityAgent:
    """
    生成されたコードのセキュリティ監査を担当するAIエージェント。
    """

    def __init__(self, llm: BaseLLM):
        """
        SecurityAgentを初期化します。

        Args:
            llm: エージェントが思考に使用する言語モデル。
        """
        self.llm = llm
        print("🤖 Security Agent initialized.")

    def run(self, project_path: str) -> str:
        """
        指定されたプロジェクトパスに対してセキュリティ監査を実行します。

        Args:
            project_path: 監査対象のプロジェクトへのパス。

        Returns:
            生成されたセキュリティ監査レポートのパス。
        """
        print(f"🛡️ Running security audit for project: {project_path}")
        
        backend_path = os.path.join(project_path, "backend")
        
        report = "## 🛡️ Security Audit Report\n\n"
        
        # バックエンドプロジェクトの監査
        if os.path.exists(backend_path) and any(fname.startswith('API_') for fname in os.listdir(backend_path)):
            api_folder_name = next((fname for fname in os.listdir(backend_path) if fname.startswith('API_')), None)
            if api_folder_name:
                target_backend_path = os.path.join(backend_path, api_folder_name)
                print(f"🔍 Analyzing backend Node.js project at: {target_backend_path}")
                
                try:
                    npm_audit_result = self._scan_nodejs_project(target_backend_path)
                    report += self._generate_report_section("Backend (Node.js)", npm_audit_result)
                except Exception as e:
                    error_message = f"Failed to run npm audit: {e}"
                    print(f"❌ {error_message}")
                    report += f"### Backend (Node.js) Analysis\n\n- {error_message}\n"
            else:
                report += "### Backend Analysis\n\n- No API sub-folder found.\n"
        else:
            report += "### Backend Analysis\n\n- No backend project found to analyze.\n"

        # TODO: フロントエンドや他のタイプのプロジェクトの監査を追加
        report += "\n### Frontend Analysis\n\n- Frontend security scan is not yet implemented.\n"
        
        report_path = os.path.join(project_path, "security_audit_report.md")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
            
        print(f"✅ Security audit report saved to: {report_path}")
        return report_path

    def _scan_nodejs_project(self, project_path: str) -> dict:
        """
        npm auditを使用してNode.jsプロジェクトの脆弱性をスキャンします。
        """
        print("... running npm audit")
        try:
            # npm install を実行して package-lock.json を生成
            subprocess.run(["npm", "install"], cwd=project_path, check=True, capture_output=True, text=True)
            # npm audit を実行
            result = subprocess.run(
                ["npm", "audit", "--json"],
                cwd=project_path,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            # 때때로 npm auditは非JSON形式のエラーを出力することがある
            try:
                return json.loads(result.stdout)
            except json.JSONDecodeError:
                return {"error": "Failed to parse npm audit JSON output", "details": result.stdout or result.stderr}
        except subprocess.CalledProcessError as e:
            return {"error": "npm audit command failed", "details": e.stderr}
        except FileNotFoundError:
            return {"error": "npm command not found. Is Node.js installed and in your PATH?"}

    def _generate_report_section(self, title: str, audit_data: dict) -> str:
        """
        LLMを使用して、監査結果のセクションを生成します。
        """
        if audit_data.get("error"):
            return f"### {title} Analysis\n\n**Error during scan:**\n```\n{audit_data.get('details', audit_data.get('error'))}\n```\n"

        summary = audit_data.get("metadata", {}).get("vulnerabilities", {})
        
        prompt = f"""
        以下のnpm auditのJSON結果を分析し、セキュリティ専門家として脆弱性の概要、リスク、および推奨される対策をマークダウン形式でまとめてください。
        重要な脆弱性があれば、特に焦点を当てて解説してください。

        **監査結果概要:**
        - クリティカル: {summary.get('critical', 0)}
        - 高: {summary.get('high', 0)}
        - 中: {summary.get('moderate', 0)}
        - 低: {summary.get('low', 0)}
        - 情報: {summary.get('info', 0)}

        **監査結果(JSON):**
        ```json
        {json.dumps(audit_data, indent=2)}
        ```
        """
        
        print(f"... asking LLM to generate report for {title}")
        response = self.llm.invoke(prompt)
        
        report_section = f"### {title} Analysis\n\n"
        report_section += f"Found **{summary.get('total', 0)}** total vulnerabilities ({summary.get('critical', 0)} critical, {summary.get('high', 0)} high).\n\n"
        report_section += response + "\n\n"
        
        return report_section

if __name__ == '__main__':
    # このエージェントを直接実行した場合のテスト用コード
    from langchain_community.llms.vertexai import VertexAI
    
    # VertexAIのラッパーを使用
    llm = VertexAI(model_name="gemini-2.5-pro")

    # テスト対象のプロジェクトパスを指定
    # この例では、AIが生成したプロジェクトの一つを指していると仮定
    test_project_path = './full_stack_projects/Final_Project_20250913_175044'

    if os.path.exists(test_project_path):
        security_agent = SecurityAgent(llm)
        security_agent.run(test_project_path)
    else:
        print(f"Test project path not found: {test_project_path}")
        print("Please run the full_agent_orchestrator first to generate a project.")
