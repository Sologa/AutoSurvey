#!/usr/bin/env python3
"""
LatteReview Wrapper 简单使用示例
展示如何从包中导入和使用主要函数
"""

# 方法1: 从包中导入
try:
    from lattereview_wrapper import run_lattereview_evaluation_sync
    print("✅ 成功从包中导入函数")
except ImportError as e:
    print(f"❌ 从包导入失败: {e}")
    print("尝试直接导入...")
    
    # 方法2: 直接导入（如果包导入失败）
    try:
        from .lattereview_wrapper import run_lattereview_evaluation_sync
        print("✅ 成功直接导入函数")
    except ImportError as e2:
        print(f"❌ 直接导入也失败: {e2}")
        print("请检查文件路径和依赖安装")
        exit(1)


def simple_review_example():
    """简单的评审示例"""
    print("\n=== 简单评审示例 ===")
    
    # 定义研究主题
    topic = "Machine Learning Research"
    
    # 选择评审模型
    reviewer_models = ["gpt-4o-mini", "gpt-4.1-mini", "gpt-5-mini"]
    
    # 准备论文数据
    papers = [
        {
            "id": "ml_001",
            "title": "Deep Learning for Computer Vision",
            "abstract": "This paper presents a novel deep learning approach for computer vision tasks. We demonstrate significant improvements in accuracy and efficiency."
        },
        {
            "id": "ml_002",
            "title": "Reinforcement Learning in Robotics",
            "abstract": "We investigate reinforcement learning techniques for robotic control and navigation, showing promising results in real-world applications."
        }
    ]
    
    print(f"主题: {topic}")
    print(f"评审模型: {reviewer_models}")
    print(f"论文数量: {len(papers)}")
    
    # 运行评审
    print("\n开始评审...")
    result = run_lattereview_evaluation_sync(
        topic=topic,
        reviewer_models=reviewer_models,
        papers=papers,
        output_dir="./simple_review_output"
    )
    
    # 显示结果
    if result["success"]:
        print(f"\n✅ 评审成功完成!")
        print(f"📊 处理论文: {result['total_papers']} 篇")
        print(f"⏱️  耗时: {result['duration_seconds']:.2f} 秒")
        print(f"💰 总成本: ${result['total_cost']:.4f}")
        
        # 显示高分论文
        high_score_papers = result['analysis']['high_score_papers']
        if high_score_papers:
            print(f"\n🏆 高分论文 (≥4分): {len(high_score_papers)} 篇")
            for paper in high_score_papers:
                print(f"  • {paper['title']} (最高分: {paper['max_score']})")
        else:
            print("\n📝 没有高分论文")
            
    else:
        print(f"\n❌ 评审失败: {result['error']}")


def check_package_info():
    """检查包信息"""
    print("\n=== 包信息检查 ===")
    
    try:
        import lattereview_wrapper
        print(f"包版本: {lattereview_wrapper.__version__}")
        print(f"作者: {lattereview_wrapper.__author__}")
        print(f"可用函数: {lattereview_wrapper.__all__}")
    except Exception as e:
        print(f"无法获取包信息: {e}")


if __name__ == "__main__":
    print("LatteReview Wrapper 简单使用示例")
    print("=" * 50)
    
    # 检查包信息
    check_package_info()
    
    # 运行简单示例
    simple_review_example()
    
    print("\n" + "=" * 50)
    print("示例运行完成!")
    print("\n提示:")
    print("1. 确保已设置正确的API密钥")
    print("2. 检查网络连接")
    print("3. 验证模型可用性")
