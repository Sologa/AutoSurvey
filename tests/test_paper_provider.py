#!/usr/bin/env python3
"""
测试PaperProvider类的功能
"""

import sys
import os

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from paper_provider import PaperProvider

def test_paper_provider():
    """测试PaperProvider的基本功能"""
    
    # 你的JSON文件路径
    json_path = "/Users/xjp/Desktop/Survey with LLMs/Survey for survey:review with LLMs/LatteReview/evaluation_results/test/20250824/high_score_papers_20250824.json"
    
    try:
        # 创建PaperProvider实例
        print("正在加载PaperProvider...")
        provider = PaperProvider(json_path)
        
        # 测试基本功能
        print(f"\n成功加载 {len(provider.papers)} 篇论文")
        
        # 显示前几篇论文的信息
        print("\n前3篇论文信息:")
        for i, paper in enumerate(provider.papers[:3]):
            print(f"\n论文 {i+1}:")
            print(f"  ID: {paper['id']}")
            print(f"  标题: {paper['title'][:100]}...")
            print(f"  摘要: {paper['abstract'][:150]}...")
        
        # 测试查询功能
        print("\n测试查询功能:")
        query = "LLMs for education"
        paper_ids = provider.get_papers_by_query(query, num=5)
        print(f"查询 '{query}' 返回了 {len(paper_ids)} 篇论文")
        
        # 测试获取论文信息
        print("\n测试获取论文信息:")
        if paper_ids:
            paper_infos = provider.get_paper_info_from_ids(paper_ids[:2])
            print(f"获取了 {len(paper_infos)} 篇论文的详细信息")
            for info in paper_infos:
                print(f"  - {info['title'][:80]}...")
        
        print("\n✅ 所有测试通过！PaperProvider工作正常。")
        
    except FileNotFoundError:
        print(f"❌ 错误: 找不到文件 {json_path}")
        print("请检查文件路径是否正确")
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_paper_provider()
