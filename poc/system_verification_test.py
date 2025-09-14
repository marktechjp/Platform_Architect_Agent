#!/usr/bin/env python3
"""
Platform Architect Agent - システム実証テスト
生成されたコードとプロジェクト構造の品質検証
"""
import os
import json
import re
from pathlib import Path
from datetime import datetime

class SystemVerificationTest:
    """システム実証テストクラス"""
    
    def __init__(self):
        self.test_results = []
        self.start_time = datetime.now()
        
    def run_full_verification(self):
        """完全なシステム検証を実行"""
        print("🧪 Platform Architect Agent - システム実証テスト開始")
        print("=" * 70)
        
        # 1. プロジェクト構造検証
        self.verify_project_structure()
        
        # 2. コード品質検証  
        self.verify_code_quality()
        
        # 3. 機能完整性検証
        self.verify_functionality()
        
        # 4. 統合性検証
        self.verify_integration()
        
        # 5. レポート生成
        self.generate_verification_report()
        
        print("\n" + "=" * 70)
        print("✅ システム実証テスト完了!")
        
        return self.test_results
    
    def verify_project_structure(self):
        """プロジェクト構造の検証"""
        print("\n📁 1. プロジェクト構造検証")
        print("-" * 40)
        
        # フルスタックプロジェクトの検証
        projects = list(Path("full_stack_projects").glob("FullStack_Project_*"))
        
        for project_path in projects:
            result = self._verify_single_project_structure(project_path)
            self.test_results.append(result)
            
            status = "✅" if result["passed"] else "❌"
            print(f"{status} {project_path.name}: {result['summary']}")
    
    def _verify_single_project_structure(self, project_path):
        """単一プロジェクトの構造検証"""
        expected_structure = {
            "frontend": ["package.json", "README.md", "src"],
            "backend": ["package.json", "README.md", "server.js"],
            "integration": ["docker-compose.yml", "README.md", "setup.sh", "api-config.json"]
        }
        
        passed_checks = 0
        total_checks = 0
        issues = []
        
        for component, expected_files in expected_structure.items():
            component_path = project_path / component
            
            for expected_file in expected_files:
                total_checks += 1
                file_paths = list(component_path.rglob(expected_file))
                
                if file_paths:
                    passed_checks += 1
                else:
                    issues.append(f"Missing {component}/{expected_file}")
        
        return {
            "test_type": "project_structure",
            "project": project_path.name,
            "passed": len(issues) == 0,
            "score": f"{passed_checks}/{total_checks}",
            "issues": issues,
            "summary": f"構造チェック {passed_checks}/{total_checks} 合格"
        }
    
    def verify_code_quality(self):
        """コード品質の検証"""
        print("\n🔍 2. コード品質検証")
        print("-" * 40)
        
        # TypeScript/JavaScript ファイルの検証
        self._verify_frontend_code_quality()
        
        # Node.js サーバーコードの検証
        self._verify_backend_code_quality()
    
    def _verify_frontend_code_quality(self):
        """フロントエンドコード品質検証"""
        tsx_files = list(Path("full_stack_projects").rglob("*.tsx"))
        css_files = list(Path("full_stack_projects").rglob("*.css"))
        
        for tsx_file in tsx_files:
            result = self._analyze_tsx_file(tsx_file)
            self.test_results.append(result)
            
            status = "✅" if result["passed"] else "❌"
            print(f"{status} {tsx_file.name}: {result['summary']}")
        
        for css_file in css_files:
            result = self._analyze_css_file(css_file)
            self.test_results.append(result)
            
            status = "✅" if result["passed"] else "❌"
            print(f"{status} {css_file.name}: {result['summary']}")
    
    def _analyze_tsx_file(self, file_path):
        """TSXファイルの分析"""
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # 品質チェック項目
            checks = {
                "typescript_import": "import.*from.*react" in content.lower(),
                "interface_definition": "interface " in content,
                "state_management": "useState" in content,
                "error_handling": "error" in content.lower(),
                "accessibility": "aria-" in content or "htmlFor" in content,
                "proper_exports": "export default" in content
            }
            
            passed_checks = sum(checks.values())
            total_checks = len(checks)
            
            return {
                "test_type": "frontend_code_quality",
                "file": str(file_path),
                "passed": passed_checks >= total_checks * 0.7,  # 70%以上で合格
                "score": f"{passed_checks}/{total_checks}",
                "checks": checks,
                "summary": f"品質スコア {passed_checks}/{total_checks}"
            }
            
        except Exception as e:
            return {
                "test_type": "frontend_code_quality",
                "file": str(file_path),
                "passed": False,
                "error": str(e),
                "summary": "読み取りエラー"
            }
    
    def _analyze_css_file(self, file_path):
        """CSSファイルの分析"""
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # CSS品質チェック
            checks = {
                "responsive_design": "@media" in content,
                "animations": "animation" in content or "transition" in content,
                "flexbox_grid": "flex" in content or "grid" in content,
                "hover_effects": ":hover" in content,
                "proper_selectors": re.search(r'\.[a-zA-Z]', content) is not None
            }
            
            passed_checks = sum(checks.values())
            total_checks = len(checks)
            
            return {
                "test_type": "css_quality",
                "file": str(file_path),
                "passed": passed_checks >= total_checks * 0.6,  # 60%以上で合格
                "score": f"{passed_checks}/{total_checks}",
                "checks": checks,
                "summary": f"CSS品質 {passed_checks}/{total_checks}"
            }
            
        except Exception as e:
            return {
                "test_type": "css_quality",
                "file": str(file_path),
                "passed": False,
                "error": str(e),
                "summary": "読み取りエラー"
            }
    
    def _verify_backend_code_quality(self):
        """バックエンドコード品質検証"""
        js_files = list(Path("full_stack_projects").rglob("server.js"))
        
        for js_file in js_files:
            result = self._analyze_server_file(js_file)
            self.test_results.append(result)
            
            status = "✅" if result["passed"] else "❌"
            print(f"{status} {js_file.name}: {result['summary']}")
    
    def _analyze_server_file(self, file_path):
        """サーバーファイルの分析"""
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # サーバーコード品質チェック
            checks = {
                "express_framework": "express" in content,
                "cors_enabled": "cors" in content,
                "jwt_auth": "jwt" in content,
                "error_handling": "try" in content and "catch" in content,
                "middleware": "app.use" in content,
                "api_routes": "/api/" in content,
                "security": "bcrypt" in content or "hash" in content
            }
            
            passed_checks = sum(checks.values())
            total_checks = len(checks)
            
            return {
                "test_type": "backend_code_quality",
                "file": str(file_path),
                "passed": passed_checks >= total_checks * 0.7,  # 70%以上で合格
                "score": f"{passed_checks}/{total_checks}",
                "checks": checks,
                "summary": f"バックエンド品質 {passed_checks}/{total_checks}"
            }
            
        except Exception as e:
            return {
                "test_type": "backend_code_quality", 
                "file": str(file_path),
                "passed": False,
                "error": str(e),
                "summary": "読み取りエラー"
            }
    
    def verify_functionality(self):
        """機能完整性の検証"""
        print("\n⚙️  3. 機能完整性検証")
        print("-" * 40)
        
        # package.jsonの依存関係チェック
        self._verify_dependencies()
        
        # APIエンドポイント定義チェック
        self._verify_api_endpoints()
    
    def _verify_dependencies(self):
        """依存関係の検証"""
        package_files = list(Path("full_stack_projects").rglob("package.json"))
        
        for package_file in package_files:
            result = self._analyze_package_json(package_file)
            self.test_results.append(result)
            
            status = "✅" if result["passed"] else "❌"
            print(f"{status} {package_file.parent.name}/package.json: {result['summary']}")
    
    def _analyze_package_json(self, file_path):
        """package.jsonの分析"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                package_data = json.load(f)
            
            dependencies = package_data.get("dependencies", {})
            scripts = package_data.get("scripts", {})
            
            # 必要な依存関係のチェック
            if "frontend" in str(file_path):
                required_deps = ["react", "typescript"]
                required_scripts = ["start", "build"]
            else:  # backend
                required_deps = ["express", "cors", "jsonwebtoken"]
                required_scripts = ["start"]
            
            dep_score = sum(1 for dep in required_deps if dep in dependencies)
            script_score = sum(1 for script in required_scripts if script in scripts)
            
            total_score = dep_score + script_score
            max_score = len(required_deps) + len(required_scripts)
            
            return {
                "test_type": "dependencies",
                "file": str(file_path),
                "passed": total_score >= max_score * 0.8,  # 80%以上で合格
                "score": f"{total_score}/{max_score}",
                "dependencies": dep_score,
                "scripts": script_score,
                "summary": f"依存関係 {total_score}/{max_score}"
            }
            
        except Exception as e:
            return {
                "test_type": "dependencies",
                "file": str(file_path),
                "passed": False,
                "error": str(e),
                "summary": "JSON解析エラー"
            }
    
    def _verify_api_endpoints(self):
        """APIエンドポイントの検証"""
        server_files = list(Path("full_stack_projects").rglob("server.js"))
        
        for server_file in server_files:
            result = self._analyze_api_endpoints(server_file)
            self.test_results.append(result)
            
            status = "✅" if result["passed"] else "❌"
            print(f"{status} APIエンドポイント: {result['summary']}")
    
    def _analyze_api_endpoints(self, file_path):
        """APIエンドポイントの分析"""
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # 期待されるエンドポイント
            expected_endpoints = [
                "POST.*register",
                "POST.*login", 
                "GET.*me",
                "GET.*health"
            ]
            
            found_endpoints = []
            for endpoint in expected_endpoints:
                if re.search(endpoint, content, re.IGNORECASE):
                    found_endpoints.append(endpoint)
            
            return {
                "test_type": "api_endpoints",
                "file": str(file_path),
                "passed": len(found_endpoints) >= len(expected_endpoints) * 0.75,  # 75%以上で合格
                "score": f"{len(found_endpoints)}/{len(expected_endpoints)}",
                "found_endpoints": found_endpoints,
                "summary": f"エンドポイント {len(found_endpoints)}/{len(expected_endpoints)}"
            }
            
        except Exception as e:
            return {
                "test_type": "api_endpoints",
                "file": str(file_path),
                "passed": False,
                "error": str(e),
                "summary": "解析エラー"
            }
    
    def verify_integration(self):
        """統合性の検証"""
        print("\n🔄 4. 統合性検証")
        print("-" * 40)
        
        # Docker Compose設定の検証
        self._verify_docker_compose()
        
        # 統合ドキュメントの検証
        self._verify_integration_docs()
    
    def _verify_docker_compose(self):
        """Docker Compose設定の検証"""
        docker_files = list(Path("full_stack_projects").rglob("docker-compose.yml"))
        
        for docker_file in docker_files:
            result = self._analyze_docker_compose(docker_file)
            self.test_results.append(result)
            
            status = "✅" if result["passed"] else "❌"
            print(f"{status} Docker Compose: {result['summary']}")
    
    def _analyze_docker_compose(self, file_path):
        """Docker Compose設定の分析"""
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Docker Composeの必要要素チェック
            checks = {
                "version_specified": "version:" in content,
                "services_defined": "services:" in content,
                "frontend_service": "frontend:" in content,
                "backend_service": "backend:" in content,
                "database_service": "mongodb:" in content or "postgres:" in content,
                "port_mapping": "ports:" in content,
                "volumes_defined": "volumes:" in content
            }
            
            passed_checks = sum(checks.values())
            total_checks = len(checks)
            
            return {
                "test_type": "docker_compose",
                "file": str(file_path),
                "passed": passed_checks >= total_checks * 0.7,  # 70%以上で合格
                "score": f"{passed_checks}/{total_checks}",
                "checks": checks,
                "summary": f"Docker設定 {passed_checks}/{total_checks}"
            }
            
        except Exception as e:
            return {
                "test_type": "docker_compose",
                "file": str(file_path),
                "passed": False,
                "error": str(e),
                "summary": "設定解析エラー"
            }
    
    def _verify_integration_docs(self):
        """統合ドキュメントの検証"""
        readme_files = list(Path("full_stack_projects").glob("*/integration/README.md"))
        
        for readme_file in readme_files:
            result = self._analyze_integration_readme(readme_file)
            self.test_results.append(result)
            
            status = "✅" if result["passed"] else "❌"
            print(f"{status} 統合README: {result['summary']}")
    
    def _analyze_integration_readme(self, file_path):
        """統合READMEの分析"""
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # READMEの必要要素チェック
            checks = {
                "setup_instructions": "セットアップ" in content or "setup" in content.lower(),
                "architecture_description": "アーキテクチャ" in content,
                "usage_examples": "```" in content,  # コードブロック
                "project_structure": "プロジェクト構成" in content,
                "next_steps": "次のステップ" in content,
                "generated_notice": "自動生成" in content
            }
            
            passed_checks = sum(checks.values())
            total_checks = len(checks)
            
            return {
                "test_type": "integration_docs",
                "file": str(file_path),
                "passed": passed_checks >= total_checks * 0.7,  # 70%以上で合格
                "score": f"{passed_checks}/{total_checks}",
                "checks": checks,
                "summary": f"ドキュメント品質 {passed_checks}/{total_checks}"
            }
            
        except Exception as e:
            return {
                "test_type": "integration_docs",
                "file": str(file_path),
                "passed": False,
                "error": str(e),
                "summary": "ドキュメント解析エラー"
            }
    
    def generate_verification_report(self):
        """検証レポートの生成"""
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        # 統計計算
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["passed"])
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        # カテゴリ別統計
        categories = {}
        for result in self.test_results:
            category = result["test_type"]
            if category not in categories:
                categories[category] = {"total": 0, "passed": 0}
            categories[category]["total"] += 1
            if result["passed"]:
                categories[category]["passed"] += 1
        
        # レポート生成
        report = {
            "verification_summary": {
                "timestamp": end_time.strftime("%Y-%m-%d %H:%M:%S"),
                "duration_seconds": round(duration, 2),
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "success_rate": round(success_rate, 1)
            },
            "category_breakdown": categories,
            "detailed_results": self.test_results,
            "overall_assessment": self._generate_assessment(success_rate),
            "recommendations": self._generate_recommendations()
        }
        
        # レポートファイル保存
        report_file = f"system_verification_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        # コンソール出力
        print(f"\n📊 検証結果サマリー")
        print(f"   総テスト数: {total_tests}")
        print(f"   合格数: {passed_tests}")
        print(f"   成功率: {success_rate:.1f}%")
        print(f"   実行時間: {duration:.2f}秒")
        print(f"   レポート: {report_file}")
        
        return report
    
    def _generate_assessment(self, success_rate):
        """総合評価の生成"""
        if success_rate >= 90:
            return "優秀 - 本番運用可能レベル"
        elif success_rate >= 80:
            return "良好 - 軽微な調整で本番運用可能"
        elif success_rate >= 70:
            return "合格 - 一部改善が推奨"
        elif success_rate >= 60:
            return "要改善 - 品質向上が必要"
        else:
            return "不合格 - 大幅な改善が必要"
    
    def _generate_recommendations(self):
        """改善推奨事項の生成"""
        recommendations = [
            "実際のnpm installとサーバー起動テスト",
            "ユニットテストの追加実装",
            "セキュリティ監査の実施",
            "パフォーマンステストの実行",
            "実際のデプロイ環境での動作確認"
        ]
        return recommendations


def main():
    """メイン実行関数"""
    tester = SystemVerificationTest()
    tester.run_full_verification()


if __name__ == "__main__":
    main()
