"""
AI服务模块 - 集成OpenAI API进行智能分析
"""
import openai
from typing import List, Dict, Optional
import json
from ..core.config import settings


class AIService:
    """AI服务类"""
    
    def __init__(self):
        """初始化AI服务"""
        openai.api_key = settings.OPENAI_API_KEY
        if settings.OPENAI_API_BASE:
            openai.api_base = settings.OPENAI_API_BASE
        self.model = settings.AI_MODEL
        self.max_tokens = settings.AI_MAX_TOKENS
    
    async def generate_summary(self, text: str, max_length: int = 200) -> str:
        """
        生成文本摘要
        
        Args:
            text: 原始文本
            max_length: 摘要最大长度
            
        Returns:
            生成的摘要
        """
        try:
            prompt = f"""请为以下问题描述生成一个简洁的摘要（不超过{max_length}字）：

问题描述：
{text}

摘要："""
            
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的文本摘要助手，擅长提取关键信息。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=0.7
            )
            
            summary = response.choices[0].message.content.strip()
            return summary
            
        except Exception as e:
            print(f"AI摘要生成失败: {str(e)}")
            return text[:max_length] + "..." if len(text) > max_length else text
    
    async def generate_tags(self, text: str) -> List[str]:
        """
        生成标签
        
        Args:
            text: 文本内容
            
        Returns:
            标签列表
        """
        try:
            prompt = f"""请为以下问题描述生成3-5个相关的标签关键词（用逗号分隔）：

问题描述：
{text}

标签："""
            
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个标签生成助手，擅长提取关键词。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.5
            )
            
            tags_text = response.choices[0].message.content.strip()
            tags = [tag.strip() for tag in tags_text.split(',')]
            return tags[:5]  # 最多返回5个标签
            
        except Exception as e:
            print(f"标签生成失败: {str(e)}")
            return []
    
    async def suggest_category(self, text: str) -> Optional[str]:
        """
        建议问题分类
        
        Args:
            text: 问题描述
            
        Returns:
            建议的分类
        """
        try:
            categories = ["bug", "feature", "improvement", "question", "other"]
            prompt = f"""请根据以下问题描述，从这些分类中选择最合适的一个：{', '.join(categories)}

问题描述：
{text}

只需回答分类名称，不要其他内容。
分类："""
            
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个问题分类助手。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=50,
                temperature=0.3
            )
            
            category = response.choices[0].message.content.strip().lower()
            return category if category in categories else None
            
        except Exception as e:
            print(f"分类建议失败: {str(e)}")
            return None
    
    async def analyze_issue_full(self, title: str, description: str) -> Dict[str, any]:
        """
        对问题进行完整的AI分析
        
        Args:
            title: 问题标题
            description: 问题描述
            
        Returns:
            包含摘要、标签和分类建议的字典
        """
        full_text = f"{title}\n\n{description}"
        
        # 并发生成摘要、标签和分类
        summary = await self.generate_summary(full_text)
        tags = await self.generate_tags(full_text)
        category = await self.suggest_category(full_text)
        
        return {
            "summary": summary,
            "tags": tags,
            "category_suggestion": category
        }
    
    async def analyze_trends(self, issues_data: List[Dict]) -> Dict[str, any]:
        """
        分析问题趋势
        
        Args:
            issues_data: 问题数据列表
            
        Returns:
            趋势分析结果
        """
        try:
            # 准备数据摘要
            issues_summary = []
            for issue in issues_data[:20]:  # 限制数量避免token过多
                issues_summary.append({
                    "title": issue.get("title", ""),
                    "category": issue.get("category", ""),
                    "priority": issue.get("priority", ""),
                    "status": issue.get("status", "")
                })
            
            prompt = f"""请分析以下问题数据，提供趋势洞察和改进建议：

问题数据：
{json.dumps(issues_summary, ensure_ascii=False, indent=2)}

请提供：
1. 主要趋势分析（3-5条）
2. 改进建议（3-5条）

以JSON格式返回，格式如下：
{{
    "trends": ["趋势1", "趋势2", ...],
    "recommendations": ["建议1", "建议2", ...]
}}
"""
            
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个数据分析专家，擅长发现模式和提供建议。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=0.7
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # 尝试解析JSON
            try:
                result = json.loads(result_text)
                return {
                    "insights": result.get("trends", []),
                    "recommendations": result.get("recommendations", [])
                }
            except json.JSONDecodeError:
                return {
                    "insights": [result_text],
                    "recommendations": []
                }
                
        except Exception as e:
            print(f"趋势分析失败: {str(e)}")
            return {
                "insights": ["分析暂时不可用"],
                "recommendations": []
            }
    
    async def generate_solution_suggestions(self, issue_description: str, 
                                           similar_issues: List[Dict]) -> List[str]:
        """
        生成解决方案建议
        
        Args:
            issue_description: 当前问题描述
            similar_issues: 相似的已解决问题
            
        Returns:
            解决方案建议列表
        """
        try:
            similar_text = "\n".join([
                f"- {issue.get('title', '')}: {issue.get('solution', '已解决')}"
                for issue in similar_issues[:5]
            ])
            
            prompt = f"""基于以下当前问题和相似的已解决问题，提供3-5条解决方案建议：

当前问题：
{issue_description}

相似的已解决问题：
{similar_text}

解决方案建议："""
            
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个问题解决专家。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=0.7
            )
            
            suggestions_text = response.choices[0].message.content.strip()
            suggestions = [s.strip() for s in suggestions_text.split('\n') if s.strip()]
            return suggestions
            
        except Exception as e:
            print(f"解决方案建议生成失败: {str(e)}")
            return ["请联系相关技术人员协助解决"]


# 创建全局AI服务实例
ai_service = AIService()



