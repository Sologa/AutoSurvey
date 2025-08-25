import json
import os
from typing import List, Dict, Any

class PaperProvider:
    """
    从用户提供的JSON文件读取paper信息，替代原有的embedding-based检索
    """
    
    def __init__(self, json_file_path: str):
        """
        初始化paper provider
        
        Args:
            json_file_path: 包含paper信息的JSON文件路径
        """
        self.json_file_path = json_file_path
        self.papers = self._load_papers()
        
    def _load_papers(self) -> List[Dict[str, Any]]:
        """加载JSON文件中的paper信息"""
        if not os.path.exists(self.json_file_path):
            raise FileNotFoundError(f"Paper JSON file not found: {self.json_file_path}")
            
        with open(self.json_file_path, 'r', encoding='utf-8') as f:
            papers = json.load(f)
        
        print(f"Loaded {len(papers)} papers from {self.json_file_path}")
        return papers
    
    def get_papers_by_query(self, query: str, num: int = 50, shuffle: bool = False) -> List[str]:
        """
        根据查询获取paper IDs（为了保持接口兼容性）
        这里我们返回所有paper的ID，因为用户已经预先筛选过了
        
        Args:
            query: 查询字符串（在这里不使用）
            num: 返回的paper数量（在这里不使用）
            shuffle: 是否随机打乱（在这里不使用）
            
        Returns:
            paper ID列表
        """
        return [paper['id'] for paper in self.papers]
    
    def get_paper_info_from_ids(self, ids: List[str]) -> List[Dict[str, Any]]:
        """
        根据ID列表获取paper信息
        
        Args:
            ids: paper ID列表
            
        Returns:
            paper信息列表
        """
        # 创建ID到paper的映射
        id_to_paper = {paper['id']: paper for paper in self.papers}
        
        # 根据ID获取paper信息
        result = []
        for paper_id in ids:
            if paper_id in id_to_paper:
                paper = id_to_paper[paper_id]
                # 转换为与原数据库相同的格式
                paper_info = {
                    'id': paper['id'],
                    'title': paper['title'],
                    'abs': paper['abstract'],
                    'authors': paper.get('authors', ''),
                    'venue': paper.get('venue', ''),
                    'year': paper.get('year', ''),
                    'arxiv_id': paper.get('arxiv_id', ''),
                    'url_pdf': paper.get('url_pdf', ''),
                    'url_landing': paper.get('url_landing', '')
                }
                result.append(paper_info)
        
        return result
    
    def get_titles_from_citations(self, citations: List[str]) -> List[str]:
        """
        根据引用获取标题（为了保持接口兼容性）
        
        Args:
            citations: 引用列表
            
        Returns:
            标题列表
        """
        # 这里我们返回所有paper的标题，因为用户已经预先筛选过了
        return [paper['title'] for paper in self.papers]
    
    def get_ids_from_queries(self, queries: List[str], num: int = 50, shuffle: bool = False) -> List[List[str]]:
        """
        根据多个查询获取paper IDs（为了保持接口兼容性）
        
        Args:
            queries: 查询列表
            num: 每个查询返回的paper数量
            shuffle: 是否随机打乱
            
        Returns:
            每个查询对应的paper ID列表的列表
        """
        # 为每个查询返回所有paper的ID
        all_ids = [paper['id'] for paper in self.papers]
        return [all_ids for _ in queries]
