#!/usr/bin/env python3
"""
完整的LatteReview功能示例
展示所有新功能：门槛模式、理由提取、入选分析等
"""

from lattereview_wrapper import run_lattereview_evaluation_sync


def example_complete_lattereview():
    """完整的LatteReview功能示例"""
    print("=== 完整LatteReview功能示例 ===")
    
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
    
    # 测试不同的门槛模式
    threshold_modes = ["Sensitive", "Specific", "Balanced"]
    
    for mode in threshold_modes:
        print(f"\n{'='*60}")
        print(f"测试门槛模式: {mode}")
        print(f"{'='*60}")
        
        # 运行评审
        result = run_lattereview_evaluation_sync(
            topic=topic,
            reviewer_models=reviewer_models,
            papers=papers,
            top_n=3,  # 输出前3篇论文
            threshold_mode=mode,  # 使用指定的门槛模式
            output_dir=f"./complete_example_output/{mode.lower()}"
        )
        
        # 处理结果
        if result["success"]:
            print(f"✅ 评审成功完成!")
            print(f"主题: {result['topic']}")
            print(f"论文数量: {result['total_papers']}")
            print(f"耗时: {result['duration_seconds']:.2f} 秒")
            print(f"总成本: ${result['total_cost']:.4f}")
            
            # 显示入选分析
            inclusion_analysis = result['analysis']['inclusion_analysis']
            print(f"\n📊 入选分析 (模式: {mode}):")
            print(f"  门槛值: {inclusion_analysis['threshold_value']}")
            print(f"  入选论文: {len(inclusion_analysis['included_papers'])} 篇")
            print(f"  排除论文: {len(inclusion_analysis['excluded_papers'])} 篇")
            print(f"  入选率: {inclusion_analysis['inclusion_rate']:.1%}")
            
            # 显示前3篇论文（按最终分数排序）
            top_papers = result['analysis']['top_papers']
            print(f"\n🏆 前3篇论文 (按最终分数排序):")
            for i, paper in enumerate(top_papers):
                print(f"  {i+1}. {paper['title']}")
                print(f"     最终分数: {paper['final_score']:.2f}")
                print(f"     是否入选: {'✅' if paper['is_included'] else '❌'}")
                print(f"     所有分数: {paper['all_scores']}")
                
                # 显示理由（如果有的话）
                if paper['reasons']:
                    print(f"     评审理由:")
                    for reviewer, reason in paper['reasons'].items():
                        if reason:
                            print(f"       {reviewer}: {reason[:100]}...")
                print()
            
            # 显示评审轮次信息
            review_rounds = result['analysis']['review_rounds']
            print(f"\n📋 评审轮次信息:")
            for round_info in review_rounds:
                print(f"  轮次 {round_info['round']}:")
                for reviewer in round_info['reviewers']:
                    print(f"    {reviewer['name']}: 评审 {reviewer['total_reviews']} 篇")
                    if reviewer['mean_evaluation']:
                        print(f"      平均分: {reviewer['mean_evaluation']:.2f}")
            
            # 显示需要Senior评审的论文
            senior_reviewed = []
            for paper in result['analysis']['top_papers']:
                if 'round-B_Senior_Reviewer_evaluation' in paper['score_details']:
                    senior_reviewed.append(paper)
            
            if senior_reviewed:
                print(f"\n🔍 需要Senior评审的论文 ({len(senior_reviewed)} 篇):")
                for paper in senior_reviewed:
                    print(f"  • {paper['title']} (分数: {paper['final_score']:.2f})")
            else:
                print(f"\n✅ 所有论文都不需要Senior评审")
                
        else:
            print(f"❌ 评审失败: {result['error']}")


def explain_threshold_modes():
    """解释门槛模式"""
    print("\n=== 门槛模式说明 ===")
    
    print("""
LatteReview提供三种入选门槛模式：

1. 🟢 Sensitive (门槛: 1.5)
   - 召回优先，门槛较低
   - 适合需要广泛覆盖的研究
   - 可能包含一些质量较低的论文

2. 🟡 Specific (门槛: 3.0)  
   - 平衡模式，中等严格程度
   - 适合一般的研究筛选
   - 平衡了召回率和精确率

3. 🔴 Balanced (门槛: 4.5)
   - 精确优先，门槛较高
   - 适合需要高质量论文的研究
   - 可能遗漏一些相关但评分较低的论文

选择建议：
- 初步调研: 使用 Sensitive
- 一般筛选: 使用 Specific  
- 高质量要求: 使用 Balanced
    """)


def explain_workflow():
    """解释工作流程"""
    print("\n=== 工作流程说明 ===")
    
    print("""
LatteReview的完整评审流程：

1. 📋 前置设定
   - 评分任务/范围: 明确告诉评审代理要评什么
   - 评分集合: 固定使用1-5分量表
   - 评分规则: 包含/排除条件
   - 理由要求: 每个分数都要附理由

2. 🔄 Round-A: 两位Junior评审
   - Conservative_Reviewer: 严格遵循纳入标准
   - Balanced_Reviewer: 综合考虑多个因素
   - 输出: 分数(1-5) + 理由

3. 🔄 Round-B: Senior裁决（仅在需要时）
   - 触发条件:
     a) 两位Junior分数不一致
     b) 两位Junior都給3分（不確定）
   - Senior能看到Round-A的完整输出（含理由）
   - 输出: 最终分数 + 理由

4. 📊 最终分数计算 (S_final)
   - 若有Round-B: 使用Senior评分
   - 否则: 取两位Junior的平均分

5. ✅ 入选判定
   - 根据选择的门槛模式 (Sensitive/Specific/Balanced)
   - S_final ≥ 门槛值 → 入选
   - 否则 → 排除

6. 📤 输出与追溯
   - 包含各轮评审的完整输出
   - 最终分数和入选状态
   - 评审理由和分数详情
    """)


if __name__ == "__main__":
    print("完整LatteReview功能示例")
    print("=" * 60)
    
    try:
        # 解释功能
        explain_threshold_modes()
        explain_workflow()
        
        # 运行完整示例
        example_complete_lattereview()
        
        print("\n" + "=" * 60)
        print("所有示例运行完成!")
        
    except Exception as e:
        print(f"运行示例时出错: {str(e)}")
        import traceback
        traceback.print_exc()
