import requests
import json

class AIService:
    def __init__(self, api_key, api_base='https://api.deepseek.com/v1'):
        self.api_key = api_key
        self.api_base = api_base
    
    def summarize_issues(self, issues):
        """使用DeepSeek API总结问题"""
        if not self.api_key:
            return "未配置DeepSeek API密钥，无法使用AI功能。请在环境变量中设置DEEPSEEK_API_KEY。"
        
        if not issues:
            return "没有问题需要总结。"
        
        # 构建提示词
        issues_text = "\n\n".join([
            f"问题 {i+1}:\n标题: {issue['title']}\n描述: {issue['description']}\n类别: {issue['category']}\n优先级: {issue['priority']}\n状态: {issue['status']}"
            for i, issue in enumerate(issues[:20])  # 限制最多20条
        ])
        
        prompt = f"""请对以下问题进行分析和总结：

{issues_text}

请从以下几个方面进行总结：
1. 问题的主要类别和分布
2. 高优先级问题的共同特点
3. 问题的主要趋势
4. 建议的改进措施

请用中文回答，并保持简洁明了。"""
        
        try:
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "system", "content": "你是一个专业的项目管理助手，擅长分析和总结项目中的问题和需求。"},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 2000
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"API调用失败: {response.status_code} - {response.text}"
        
        except Exception as e:
            return f"AI总结失败: {str(e)}"
    
    def analyze_objective_progress(self, objectives):
        """分析目标进度"""
        if not self.api_key:
            return "未配置DeepSeek API密钥。"
        
        if not objectives:
            return "没有目标数据需要分析。"
        
        objectives_text = "\n\n".join([
            f"目标 {i+1}:\n标题: {obj['title']}\n进度: {obj['progress']}%\n状态: {obj['status']}\n截止日期: {obj['deadline']}"
            for i, obj in enumerate(objectives[:15])
        ])
        
        prompt = f"""请分析以下目标的完成情况：

{objectives_text}

请提供：
1. 整体进度评估
2. 风险识别（逾期风险等）
3. 改进建议

请用中文回答。"""
        
        try:
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "system", "content": "你是一个专业的项目管理助手。"},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 2000
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"API调用失败: {response.status_code}"
        
        except Exception as e:
            return f"AI分析失败: {str(e)}"

