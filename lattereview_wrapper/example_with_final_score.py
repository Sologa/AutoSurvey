#!/usr/bin/env python3
"""
使用最终分数计算的LatteReview示例
展示如何获取按最终分数排序的前N篇论文
"""

from lattereview_wrapper import run_lattereview_evaluation_sync


def example_with_final_score():
    """使用最终分数计算的示例"""
    print("=== 使用最终分数计算的示例 ===")
    
    # 定义研究主题
    topic = "Large Language Models in Academic Research"
    
    # 定义三个评审者模型
    reviewer_models = [
        "gpt-4o-mini",      # Conservative Reviewer (Junior)
        "gpt-4.1-mini",     # Balanced Reviewer (Junior)
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
        },
        {
            "id": "paper_004",
            "title": "Machine Learning in Scientific Discovery",
            "abstract": "This paper discusses the application of machine learning techniques in scientific discovery processes, including drug discovery, materials science, and climate modeling."
        },
        {
            "id": "paper_005",
            "title": "Deep Learning for Research Automation",
            "abstract": "We present a comprehensive framework for automating research processes using deep learning techniques, including literature analysis, hypothesis generation, and experimental design."
        }
    ]
    
    print(f"主题: {topic}")
    print(f"评审模型: {reviewer_models}")
    print(f"论文数量: {len(papers)}")
    
    # 运行评审，获取前3篇论文
    print("\n开始评审，输出前3篇论文...")
    result = run_lattereview_evaluation_sync(
        topic=topic,
        reviewer_models=reviewer_models,
        papers=papers,
        top_n=3,  # 指定输出前3篇论文
        output_dir="./final_score_example_output"
    )
    
    # 处理结果
    if result["success"]:
        print(f"\n✅ 评审成功完成!")
        print(f"主题: {result['topic']}")
        print(f"论文数量: {result['total_papers']}")
        print(f"耗时: {result['duration_seconds']:.2f} 秒")
        print(f"总成本: ${result['total_cost']:.4f}")
        
        # 显示前3篇论文（按最终分数排序）
        top_papers = result['analysis']['top_papers']
        print(f"\n🏆 前3篇论文 (按最终分数排序):")
        for i, paper in enumerate(top_papers):
            print(f"  {i+1}. {paper['title']}")
            print(f"     最终分数: {paper['final_score']:.2f}")
            print(f"     所有分数: {paper['all_scores']}")
            print(f"     分数详情: {paper['score_details']}")
            print()
        
        # 显示高分论文统计
        high_score_papers = result['analysis']['high_score_papers']
        print(f"📊 高分论文统计 (≥4分): {len(high_score_papers)} 篇")
        
        # 显示评审轮次信息
        review_rounds = result['analysis']['review_rounds']
        print(f"\n📋 评审轮次信息:")
        for round_info in review_rounds:
            print(f"  轮次 {round_info['round']}:")
            for reviewer in round_info['reviewers']:
                print(f"    {reviewer['name']}: 评审 {reviewer['total_reviews']} 篇")
                if reviewer['mean_evaluation']:
                    print(f"      平均分: {reviewer['mean_evaluation']:.2f}")
        
    else:
        print(f"\n❌ 评审失败: {result['error']}")


def example_compare_different_top_n():
    """比较不同top_n参数的效果"""
    print("\n=== 比较不同top_n参数的效果 ===")
    
    topic = "Computer Vision Research"
    reviewer_models = ["gpt-4o-mini", "gpt-4.1-mini", "gpt-5-mini"]
    
    papers = [
        {
            "id": "cv_001",
            "title": "Deep Learning for Object Detection",
            "abstract": "We present a novel deep learning approach for object detection in computer vision applications."
        },
        {
            "id": "cv_002",
            "title": "Image Segmentation Using CNNs",
            "abstract": "This paper explores convolutional neural networks for image segmentation tasks."
        },
        {
            "id": "cv_003",
            "title": "Computer Vision in Autonomous Vehicles",
            "abstract": "We investigate computer vision techniques for autonomous vehicle navigation."
        },
        {
            "id": "cv_004",
            "title": "Medical Image Analysis with AI",
            "abstract": "This work presents AI-based methods for medical image analysis and diagnosis."
        },
        {
            "id": "cv_005",
            "title": "Real-time Video Processing",
            "abstract": "We develop real-time video processing algorithms for surveillance applications."
        }
    ]
    
    # 测试不同的top_n值
    for top_n in [2, 3, 5]:
        print(f"\n--- 输出前 {top_n} 篇论文 ---")
        
        result = run_lattereview_evaluation_sync(
            topic=topic,
            reviewer_models=reviewer_models,
            papers=papers,
            top_n=top_n,
            output_dir=f"./top_n_comparison/top_{top_n}"
        )
        
        if result["success"]:
            top_papers = result['analysis']['top_papers']
            print(f"成功获取前 {len(top_papers)} 篇论文:")
            
            for i, paper in enumerate(top_papers):
                print(f"  {i+1}. {paper['title']} (分数: {paper['final_score']:.2f})")
        else:
            print(f"失败: {result['error']}")


def explain_final_score_algorithm():
    """解释最终分数计算算法"""
    print("\n=== 最终分数计算算法说明 ===")
    
    print("""
最终分数 S_final 的计算规则：

1. 优先使用 round-B_Senior_Reviewer_evaluation
   - 这是Senior评审者在Round B中的评分
   - 只有当两个Junior评审者分歧≥2分时才会产生

2. 其次使用 round-A_Senior_Reviewer_evaluation  
   - 这是Senior评审者在Round A中的评分
   - 如果Senior评审者参与了Round A

3. 最后取两位Junior评审者的平均分
   - Conservative_Reviewer_evaluation
   - Balanced_Reviewer_evaluation
   - 计算: (conservative + balanced) / 2

4. 如果只有一个Junior的分数，直接使用该分数

评审流程：
- Round A: Conservative + Balanced 评审所有论文
- Round B: 只有当两个Junior评分差异≥2分时，Senior才评审
- 这样可以节省成本，只对分歧较大的论文进行Senior评审
    """)


if __name__ == "__main__":
    print("最终分数计算示例")
    print("=" * 50)
    
    try:
        # 解释算法
        explain_final_score_algorithm()
        
        # 运行基本示例
        example_with_final_score()
        
        # 比较不同top_n参数
        example_compare_different_top_n()
        
        print("\n" + "=" * 50)
        print("所有示例运行完成!")
        
    except Exception as e:
        print(f"运行示例时出错: {str(e)}")
        import traceback
        traceback.print_exc()
