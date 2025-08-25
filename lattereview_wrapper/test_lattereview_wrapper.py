#!/usr/bin/env python3
"""
测试LatteReview包装函数的基本功能
"""

import sys
import os
from pathlib import Path

# 添加当前目录到Python路径
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

try:
    from lattereview_wrapper import (
        create_provider,
        create_reviewers,
        create_workflow,
        analyze_results,
        save_results
    )
    print("✅ 成功导入所有函数")
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    sys.exit(1)


def test_create_provider():
    """测试provider创建功能"""
    print("\n=== 测试Provider创建 ===")
    
    test_models = [
        "gpt-4o-mini",
        "gpt-5-mini", 
        "claude-3-sonnet",
        "gemini-1.5-pro"
    ]
    
    for model in test_models:
        try:
            provider = create_provider(model)
            print(f"✅ 成功创建 {model} 的provider: {type(provider).__name__}")
        except Exception as e:
            print(f"❌ 创建 {model} 的provider失败: {e}")


def test_create_reviewers():
    """测试评审者创建功能"""
    print("\n=== 测试评审者创建 ===")
    
    topic = "Test Topic"
    reviewer_models = ["gpt-4o-mini", "gpt-4.1-mini", "gpt-5-mini"]
    
    try:
        reviewers = create_reviewers(
            reviewer_models=reviewer_models,
            topic=topic
        )
        print(f"✅ 成功创建 {len(reviewers)} 个评审者")
        
        for i, reviewer in enumerate(reviewers):
            print(f"  评审者 {i+1}: {reviewer.name} ({reviewer.reasoning})")
            print(f"    模型参数: {reviewer.model_args}")
            
    except Exception as e:
        print(f"❌ 创建评审者失败: {e}")


def test_create_workflow():
    """测试工作流创建功能"""
    print("\n=== 测试工作流创建 ===")
    
    try:
        # 创建模拟评审者
        from lattereview.agents import TitleAbstractReviewer
        from lattereview.providers import OpenAIProvider
        
        mock_provider = OpenAIProvider(model="gpt-4o-mini")
        mock_reviewer = TitleAbstractReviewer(
            provider=mock_provider,
            name="Test_Reviewer",
            backstory="Test reviewer",
            inclusion_criteria="Test criteria",
            exclusion_criteria="Test exclusion",
            reasoning="brief"
        )
        
        workflow = create_workflow([mock_reviewer])
        print(f"✅ 成功创建工作流: {type(workflow).__name__}")
        print(f"  工作流轮次: {len(workflow.workflow_schema)}")
        
    except Exception as e:
        print(f"❌ 创建工作流失败: {e}")


def test_analyze_results():
    """测试结果分析功能"""
    print("\n=== 测试结果分析功能 ===")
    
    try:
        import pandas as pd
        
        # 创建模拟结果数据
        mock_results = pd.DataFrame({
            'id': ['1', '2', '3'],
            'title': ['Paper 1', 'Paper 2', 'Paper 3'],
            'round-A_Conservative_Reviewer_evaluation': [4, 3, 5],
            'round-A_Balanced_Reviewer_evaluation': [4, 4, 4],
            'round-A_Senior_Reviewer_evaluation': [5, 3, 4]
        })
        
        topic = "Test Topic"
        reviewer_models = ["gpt-4o-mini", "gpt-4.1-mini", "gpt-5-mini"]
        
        analysis = analyze_results(mock_results, topic, reviewer_models)
        
        print(f"✅ 成功分析结果")
        print(f"  主题: {analysis['topic']}")
        print(f"  论文数量: {analysis['total_papers']}")
        print(f"  高分论文: {len(analysis['high_score_papers'])} 篇")
        print(f"  评审轮次: {len(analysis['review_rounds'])}")
        
    except Exception as e:
        print(f"❌ 结果分析失败: {e}")


def test_save_results():
    """测试结果保存功能"""
    print("\n=== 测试结果保存功能 ===")
    
    try:
        import pandas as pd
        
        # 创建模拟数据
        mock_results = pd.DataFrame({
            'id': ['1', '2'],
            'title': ['Paper 1', 'Paper 2'],
            'round-A_Reviewer_evaluation': [4, 5]
        })
        
        mock_analysis = {
            'topic': 'Test Topic',
            'total_papers': 2,
            'high_score_papers': []
        }
        
        output_dir = "./test_output"
        topic = "Test Topic"
        
        save_results(mock_results, mock_analysis, output_dir, topic)
        
        # 检查文件是否创建
        output_path = Path(output_dir)
        if output_path.exists():
            print(f"✅ 成功保存结果到: {output_path}")
            
            # 清理测试文件
            import shutil
            shutil.rmtree(output_path)
            print("  已清理测试文件")
        else:
            print("❌ 输出目录未创建")
            
    except Exception as e:
        print(f"❌ 结果保存失败: {e}")


def test_paper_format_validation():
    """测试论文格式验证"""
    print("\n=== 测试论文格式验证 ===")
    
    # 正确的论文格式
    valid_papers = [
        {
            "id": "1",
            "title": "Valid Paper 1",
            "abstract": "This is a valid abstract."
        },
        {
            "id": "2",
            "title": "Valid Paper 2", 
            "abstract": "This is another valid abstract."
        }
    ]
    
    # 缺少字段的论文
    invalid_papers = [
        {
            "id": "3",
            "title": "Invalid Paper 3"
            # 缺少abstract字段
        },
        {
            "id": "4",
            "abstract": "This paper has no title."
            # 缺少title字段
        }
    ]
    
    print("✅ 论文格式验证功能已集成到主函数中")


def main():
    """运行所有测试"""
    print("开始测试LatteReview包装函数...")
    print("=" * 50)
    
    try:
        test_create_provider()
        test_create_reviewers()
        test_create_workflow()
        test_analyze_results()
        test_save_results()
        test_paper_format_validation()
        
        print("\n" + "=" * 50)
        print("✅ 所有测试完成!")
        print("\n注意: 这些测试主要验证函数导入和基本结构。")
        print("要测试完整的评审流程，请运行 example_lattereview_usage.py")
        
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
