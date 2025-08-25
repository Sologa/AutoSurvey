# LatteReview Wrapper 快速开始指南

## 🚀 5分钟快速上手

### 1. 安装依赖

```bash
cd AutoSurvey
pip install -r requirements_lattereview.txt
```

### 2. 设置API密钥

```bash
# OpenAI API
export OPENAI_API_KEY="your-openai-api-key"

# 或者创建 .env 文件
echo "OPENAI_API_KEY=your-openai-api-key" > .env
```

### 3. 创建第一个评审

```python
from lattereview_wrapper import run_lattereview_evaluation_sync

# 定义研究主题
topic = "AI in Healthcare"

# 选择模型
reviewer_models = ["gpt-4o-mini", "gpt-4.1-mini", "gpt-5-mini"]

# 准备论文
papers = [
    {
        "id": "1",
        "title": "Deep Learning for Medical Diagnosis",
        "abstract": "We present a deep learning approach for automated medical diagnosis..."
    }
]

# 运行评审
result = run_lattereview_evaluation_sync(
    topic=topic,
    reviewer_models=reviewer_models,
    papers=papers
)

print(f"评审完成! 高分论文: {len(result['analysis']['high_score_papers'])} 篇")
```

## 📋 完整示例

### 基本评审流程

```python
from lattereview_wrapper import run_lattereview_evaluation_sync

def review_papers():
    # 1. 准备数据
    topic = "Machine Learning Applications"
    reviewer_models = ["gpt-4o-mini", "gpt-4.1-mini", "gpt-5-mini"]
    
    papers = [
        {
            "id": "ml_001",
            "title": "Neural Networks for Image Recognition",
            "abstract": "This paper explores the use of neural networks..."
        },
        {
            "id": "ml_002", 
            "title": "Reinforcement Learning in Robotics",
            "abstract": "We investigate reinforcement learning approaches..."
        }
    ]
    
    # 2. 运行评审
    result = run_lattereview_evaluation_sync(
        topic=topic,
        reviewer_models=reviewer_models,
        papers=papers,
        output_dir="./ml_review_results"
    )
    
    # 3. 处理结果
    if result["success"]:
        print(f"✅ 评审成功!")
        print(f"📊 论文数量: {result['total_papers']}")
        print(f"💰 总成本: ${result['total_cost']:.4f}")
        print(f"⏱️  耗时: {result['duration_seconds']:.2f} 秒")
        
        # 显示高分论文
        high_score_papers = result['analysis']['high_score_papers']
        if high_score_papers:
            print(f"\n🏆 高分论文 (≥4分):")
            for paper in high_score_papers:
                print(f"  • {paper['title']} (最高分: {paper['max_score']})")
    else:
        print(f"❌ 评审失败: {result['error']}")

if __name__ == "__main__":
    review_papers()
```

### 自定义评审标准

```python
# 定义特定的纳入和排除标准
inclusion_criteria = """
Research must demonstrate:
1. Novel methodology or significant improvement
2. Comprehensive evaluation with real data
3. Clear practical applications
4. Proper statistical analysis
"""

exclusion_criteria = """
Exclude research that:
1. Only presents theoretical concepts
2. Lacks experimental validation
3. Uses outdated techniques
4. Has insufficient sample sizes
"""

result = run_lattereview_evaluation_sync(
    topic="Computer Vision Research",
    reviewer_models=["gpt-4o-mini", "gpt-4.1-mini", "gpt-5-mini"],
    papers=papers,
    inclusion_criteria=inclusion_criteria,
    exclusion_criteria=exclusion_criteria
)
```

### 批量处理大量论文

```python
import json

# 从文件加载论文
with open("papers.json", "r") as f:
    papers = json.load(f)

print(f"加载了 {len(papers)} 篇论文")

# 分批处理
batch_size = 50
for i in range(0, len(papers), batch_size):
    batch = papers[i:i+batch_size]
    print(f"\n处理第 {i//batch_size + 1} 批 ({len(batch)} 篇论文)")
    
    result = run_lattereview_evaluation_sync(
        topic="AI Research Survey",
        reviewer_models=["gpt-4o-mini", "gpt-4.1-mini", "gpt-5-mini"],
        papers=batch,
        output_dir=f"./batch_results/batch_{i//batch_size + 1}"
    )
    
    if result["success"]:
        print(f"✅ 批次完成! 成本: ${result['total_cost']:.4f}")
    else:
        print(f"❌ 批次失败: {result['error']}")
```

## 🔧 常见配置

### 模型选择

```python
# OpenAI 系列
openai_models = ["gpt-4o-mini", "gpt-4.1-mini", "gpt-5-mini"]

# Claude 系列
claude_models = ["claude-3-sonnet", "claude-3-opus", "gpt-5-mini"]

# 混合模型
mixed_models = ["gpt-4o-mini", "claude-3-sonnet", "gpt-5-mini"]
```

### 输出目录结构

```
output_dir/
├── lattereview_results_AI_in_Healthcare.json  # 评审结果
├── lattereview_analysis_AI_in_Healthcare.json # 分析报告
└── summary.txt                                # 摘要报告
```

## ⚠️ 注意事项

1. **API限制**: 注意各模型的调用限制
2. **成本控制**: 大量论文评审可能产生高成本
3. **网络稳定性**: 确保网络连接稳定
4. **模型可用性**: 验证模型在您的账户中可用

## 🆘 故障排除

### 常见错误

```python
# 1. API密钥错误
# 错误: "OPENAI_API_KEY environment variable is not set"
# 解决: 设置正确的环境变量

# 2. 模型不可用
# 错误: "Model not found"
# 解决: 检查模型名称和账户权限

# 3. 网络错误
# 错误: "Connection timeout"
# 解决: 检查网络连接和防火墙设置
```

### 调试模式

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# 运行评审时会显示详细日志
result = run_lattereview_evaluation_sync(...)
```

## 📚 下一步

- 查看完整文档: `README_LatteReview_Wrapper.md`
- 运行示例: `python example_lattereview_usage.py`
- 运行测试: `python test_lattereview_wrapper.py`

## 💡 提示

- 从小批量开始测试
- 监控API调用成本
- 保存重要的评审结果
- 根据反馈调整评审标准

---

**需要帮助?** 查看完整文档或运行测试脚本！
