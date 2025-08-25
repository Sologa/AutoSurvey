# LatteReview Wrapper 集成说明

本文档说明LatteReview Wrapper包如何集成到AutoSurvey项目中，以及如何使用它进行论文评审。

## 📁 项目结构

```
AutoSurvey/
├── README_LatteReview_Integration.md    # 本文档
├── use_lattereview_wrapper.py           # 包使用示例
└── lattereview_wrapper/                 # LatteReview包装包
    ├── __init__.py                      # 包初始化
    ├── README.md                        # 包说明
    ├── lattereview_wrapper.py           # 核心函数
    ├── example_lattereview_usage.py     # 详细示例
    ├── simple_example.py                # 简单示例
    ├── test_lattereview_wrapper.py      # 功能测试
    ├── requirements_lattereview.txt     # 依赖列表
    ├── README_LatteReview_Wrapper.md    # 详细文档
    └── QUICKSTART_LatteReview.md       # 快速开始
```

## 🚀 快速集成

### 1. 安装依赖

```bash
cd AutoSurvey/lattereview_wrapper
pip install -r requirements_lattereview.txt
```

### 2. 设置环境变量

```bash
# OpenAI API
export OPENAI_API_KEY="your-openai-api-key"

# 或者创建.env文件
echo "OPENAI_API_KEY=your-openai-api-key" > .env
```

### 3. 测试集成

```bash
# 在AutoSurvey根目录
python use_lattereview_wrapper.py

# 或者在包目录中
cd lattereview_wrapper
python test_lattereview_wrapper.py
```

## 💻 在代码中使用

### 基本导入

```python
# 方法1: 从包导入（推荐）
from lattereview_wrapper import run_lattereview_evaluation_sync

# 方法2: 直接导入
from lattereview_wrapper.lattereview_wrapper import run_lattereview_evaluation_sync
```

### 基本使用

```python
from lattereview_wrapper import run_lattereview_evaluation_sync

# 运行论文评审
result = run_lattereview_evaluation_sync(
    topic="Large Language Models in Academic Research",
    reviewer_models=["gpt-4o-mini", "gpt-4.1-mini", "gpt-5-mini"],
    papers=[
        {
            "id": "paper_001",
            "title": "Paper Title",
            "abstract": "Paper abstract..."
        }
    ],
    output_dir="./review_results"
)

# 处理结果
if result["success"]:
    print(f"评审完成! 高分论文: {len(result['analysis']['high_score_papers'])} 篇")
else:
    print(f"评审失败: {result['error']}")
```

## 🔧 集成到现有工作流

### 1. 在AutoSurvey主程序中集成

```python
# 在AutoSurvey的主程序中
from lattereview_wrapper import run_lattereview_evaluation_sync

def integrate_lattereview_review(papers, topic):
    """集成LatteReview评审到AutoSurvey工作流"""
    
    # 运行评审
    review_result = run_lattereview_evaluation_sync(
        topic=topic,
        reviewer_models=["gpt-4o-mini", "gpt-4.1-mini", "gpt-5-mini"],
        papers=papers,
        output_dir=f"./lattereview_reviews/{topic.replace(' ', '_')}"
    )
    
    if review_result["success"]:
        # 处理评审结果
        high_score_papers = review_result['analysis']['high_score_papers']
        print(f"发现 {len(high_score_papers)} 篇高分论文")
        
        # 将结果集成到AutoSurvey的后续流程
        return high_score_papers
    else:
        print(f"评审失败: {review_result['error']}")
        return []
```

### 2. 批量处理论文

```python
def batch_review_papers(papers, topic, batch_size=50):
    """分批评审大量论文"""
    
    all_results = []
    
    for i in range(0, len(papers), batch_size):
        batch = papers[i:i+batch_size]
        print(f"处理第 {i//batch_size + 1} 批 ({len(batch)} 篇论文)")
        
        result = run_lattereview_evaluation_sync(
            topic=topic,
            reviewer_models=["gpt-4o-mini", "gpt-4.1-mini", "gpt-5-mini"],
            papers=batch,
            output_dir=f"./batch_reviews/batch_{i//batch_size + 1}"
        )
        
        if result["success"]:
            all_results.extend(result['analysis']['high_score_papers'])
            print(f"✅ 批次完成! 成本: ${result['total_cost']:.4f}")
        else:
            print(f"❌ 批次失败: {result['error']}")
    
    return all_results
```

## 📊 输出结果格式

### 评审结果结构

```python
{
    "success": True,                    # 是否成功
    "topic": "研究主题",                # 研究主题
    "reviewer_models": ["模型列表"],     # 使用的模型
    "total_papers": 10,                # 论文总数
    "duration_seconds": 45.2,          # 耗时（秒）
    "total_cost": 0.1234,              # 总成本（美元）
    "results": [...],                  # 详细评审结果
    "analysis": {                      # 分析报告
        "high_score_papers": [...],    # 高分论文
        "review_rounds": [...],        # 评审轮次信息
        "score_distribution": {...}    # 评分分布
    }
}
```

### 文件输出

- **评审结果**: `lattereview_results_{topic}.json`
- **分析报告**: `lattereview_analysis_{topic}.json`
- **摘要报告**: `summary.txt`

## ⚙️ 配置选项

### 模型参数自动配置

- **GPT-5系列**: `temperature = 1.0`（锁定）
- **其他模型**: `temperature = 0.2`

### 自定义评审标准

```python
inclusion_criteria = """
Research must demonstrate:
1. Novel methodology
2. Comprehensive evaluation
3. Real-world application
"""

exclusion_criteria = """
Exclude research that:
1. Lacks innovation
2. Has insufficient data
3. No practical impact
"""

result = run_lattereview_evaluation_sync(
    topic=topic,
    reviewer_models=reviewer_models,
    papers=papers,
    inclusion_criteria=inclusion_criteria,
    exclusion_criteria=exclusion_criteria
)
```

## 🧪 测试和验证

### 1. 功能测试

```bash
cd lattereview_wrapper
python test_lattereview_wrapper.py
```

### 2. 集成测试

```bash
# 在AutoSurvey根目录
python use_lattereview_wrapper.py
```

### 3. 示例运行

```bash
cd lattereview_wrapper
python simple_example.py
python example_lattereview_usage.py
```

## 🔍 故障排除

### 常见问题

1. **导入错误**: 检查Python路径和包安装
2. **API错误**: 验证API密钥和环境变量
3. **模型错误**: 确认模型名称和账户权限
4. **网络错误**: 检查网络连接和防火墙

### 调试模式

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# 运行评审时会显示详细日志
result = run_lattereview_evaluation_sync(...)
```

## 📚 更多资源

- **快速开始**: `lattereview_wrapper/QUICKSTART_LatteReview.md`
- **详细文档**: `lattereview_wrapper/README_LatteReview_Wrapper.md`
- **使用示例**: `lattereview_wrapper/example_lattereview_usage.py`
- **功能测试**: `lattereview_wrapper/test_lattereview_wrapper.py`

## 🎯 下一步

1. 安装依赖包
2. 设置API密钥
3. 运行测试脚本
4. 集成到现有工作流
5. 自定义评审标准
6. 批量处理论文

---

**开始集成**: 查看 `lattereview_wrapper/QUICKSTART_LatteReview.md` 获取快速上手指南！
