#!/usr/bin/env python3
"""
LatteReview Wrapper 使用示例
展示如何使用封装的LatteReview评审函数
"""

import json
from lattereview_wrapper import run_lattereview_evaluation_sync


def example_basic_usage():
    """基本使用示例"""
    print("=== 基本使用示例 ===")
    
    # 定义研究主题
    topic = "Large Language Models in Academic Research"
    
    # 定义三个评审者模型
    reviewer_models = [
        "gpt-4o-mini",      # Conservative Reviewer
        "gpt-4.1-mini",     # Balanced Reviewer  
        "gpt-5-mini"        # Senior Reviewer
    ]
    
    # 定义要评审的论文
    papers = [
        {
            "id": "paper_001",
            "title": "Large Language Models for Automated Literature Review",
            "abstract": "This paper presents a novel approach to using large language models for automated literature review processes. We demonstrate how GPT-based models can effectively analyze academic papers and generate comprehensive summaries."
        },
        {
            "id": "paper_002", 
            "title": "AI-Assisted Research: A Survey of Current Applications",
            "abstract": "We survey the current state of AI-assisted research tools and methodologies. Our analysis covers various domains including natural language processing, computer vision, and scientific discovery."
        },
        {
            "id": "paper_003",
            "title": "Automated Survey Generation Using Transformer Models",
            "abstract": "This work explores the use of transformer-based models for automatically generating comprehensive literature surveys. We evaluate the quality and accuracy of generated surveys compared to human-written ones."
        }
    ]
    
    # 运行评审
    result = run_lattereview_evaluation_sync(
        topic=topic,
        reviewer_models=reviewer_models,
        papers=papers,
        output_dir="./lattereview_output"
    )
    
    # 打印结果
    if result["success"]:
        print(f"评审成功完成!")
        print(f"主题: {result['topic']}")
        print(f"论文数量: {result['total_papers']}")
        print(f"耗时: {result['duration_seconds']:.2f} 秒")
        print(f"总成本: ${result['total_cost']:.4f}")
        
        # 打印高分论文
        high_score_papers = result['analysis']['high_score_papers']
        if high_score_papers:
            print(f"\n高分论文 (≥4分): {len(high_score_papers)} 篇")
            for i, paper in enumerate(high_score_papers[:3]):  # 显示前3篇
                print(f"  {i+1}. {paper['title']}")
                print(f"     最高分: {paper['max_score']}")
        else:
            print("\n没有高分论文")
    else:
        print(f"评审失败: {result['error']}")


def example_custom_criteria():
    """自定义评审标准示例"""
    print("\n=== 自定义评审标准示例 ===")
    
    topic = "Machine Learning in Healthcare"
    
    # 自定义纳入标准
    inclusion_criteria = """
    Research must be related to Machine Learning in Healthcare and demonstrate:
    1. Clear application of ML techniques to healthcare problems
    2. Clinical validation or real-world testing
    3. Novel methodology or significant improvement over existing approaches
    4. Relevance to patient care or medical decision making
    5. Proper evaluation metrics and statistical analysis
    """
    
    # 自定义排除标准
    exclusion_criteria = """
    Exclude research that:
    1. Only discusses theoretical concepts without practical implementation
    2. Lacks clinical validation or real-world testing
    3. Uses outdated ML techniques (pre-2015)
    4. Focuses on non-healthcare applications
    5. Has insufficient sample sizes (<100 patients)
    6. Lacks proper statistical analysis
    """
    
    reviewer_models = ["gpt-4o-mini", "gpt-4.1-mini", "gpt-5-mini"]
    
    papers = [
        {
            "id": "health_001",
            "title": "Deep Learning for Early Cancer Detection",
            "abstract": "We present a deep learning model for early detection of breast cancer using mammography images. Our model achieves 95% accuracy on a dataset of 10,000 patients and has been validated in clinical trials."
        },
        {
            "id": "health_002",
            "title": "Machine Learning in Drug Discovery",
            "abstract": "This paper reviews current applications of machine learning in pharmaceutical research, focusing on drug discovery and development processes."
        }
    ]
    
    result = run_lattereview_evaluation_sync(
        topic=topic,
        reviewer_models=reviewer_models,
        papers=papers,
        inclusion_criteria=inclusion_criteria,
        exclusion_criteria=exclusion_criteria,
        output_dir="./lattereview_healthcare"
    )
    
    if result["success"]:
        print(f"医疗健康ML评审完成!")
        print(f"论文数量: {result['total_papers']}")
        print(f"高分论文: {len(result['analysis']['high_score_papers'])} 篇")


def example_different_models():
    """使用不同模型组合的示例"""
    print("\n=== 不同模型组合示例 ===")
    
    topic = "Natural Language Processing Research"
    
    # 不同的模型组合
    model_combinations = [
        ["gpt-4o-mini", "gpt-4.1-mini", "gpt-5-mini"],           # OpenAI系列
        ["claude-3-sonnet", "claude-3-opus", "gpt-5-mini"],       # Claude + GPT-5
        ["gemini-1.5-pro", "gpt-4o-mini", "gpt-5-mini"],          # Gemini + OpenAI
    ]
    
    papers = [
        {
            "id": "nlp_001",
            "title": "Transformer Models for Text Generation",
            "abstract": "We investigate the effectiveness of transformer-based models for text generation tasks. Our experiments show significant improvements in quality and coherence."
        }
    ]
    
    for i, models in enumerate(model_combinations):
        print(f"\n测试模型组合 {i+1}: {models}")
        
        result = run_lattereview_evaluation_sync(
            topic=topic,
            reviewer_models=models,
            papers=papers,
            output_dir=f"./lattereview_nlp_models_{i+1}"
        )
        
        if result["success"]:
            print(f"  成功! 成本: ${result['total_cost']:.4f}")
        else:
            print(f"  失败: {result['error']}")


def example_batch_processing():
    """批量处理示例"""
    print("\n=== 批量处理示例 ===")
    
    topic = "Computer Vision Applications"
    
    # 生成大量示例论文
    papers = []
    for i in range(10):
        papers.append({
            "id": f"cv_{i+1:03d}",
            "title": f"Computer Vision Paper {i+1}: {['Object Detection', 'Image Segmentation', 'Face Recognition', 'Medical Imaging', 'Autonomous Driving'][i % 5]}",
            "abstract": f"This is a sample abstract for computer vision paper {i+1}. It discusses various aspects of computer vision including algorithms, applications, and performance evaluation."
        })
    
    reviewer_models = ["gpt-4o-mini", "gpt-4.1-mini", "gpt-5-mini"]
    
    print(f"开始批量评审 {len(papers)} 篇论文...")
    
    result = run_lattereview_evaluation_sync(
        topic=topic,
        reviewer_models=reviewer_models,
        papers=papers,
        output_dir="./lattereview_batch"
    )
    
    if result["success"]:
        print(f"批量评审完成!")
        print(f"处理论文: {result['total_papers']} 篇")
        print(f"总耗时: {result['duration_seconds']:.2f} 秒")
        print(f"平均每篇: {result['duration_seconds']/result['total_papers']:.2f} 秒")
        print(f"总成本: ${result['total_cost']:.4f}")
        print(f"每篇成本: ${result['total_cost']/result['total_papers']:.4f}")
        
        # 显示评分分布
        for round_info in result['analysis']['review_rounds']:
            for reviewer in round_info['reviewers']:
                print(f"\n{reviewer['name']} 评分分布:")
                for score, count in reviewer['evaluation_distribution'].items():
                    print(f"  {score}分: {count} 篇")
                print(f"  平均分: {reviewer['mean_evaluation']:.2f}")


if __name__ == "__main__":
    print("LatteReview Wrapper 使用示例")
    print("=" * 50)
    
    try:
        # 运行各种示例
        example_basic_usage()
        example_custom_criteria()
        example_different_models()
        example_batch_processing()
        
        print("\n所有示例运行完成!")
        
    except Exception as e:
        print(f"运行示例时出错: {str(e)}")
        import traceback
        traceback.print_exc()
