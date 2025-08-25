# LatteReview Wrapper Package

这是一个专为AutoSurvey项目设计的LatteReview包装包，将复杂的论文评审流程封装为简单的函数接口。

## 📁 包结构

```
lattereview_wrapper/
├── __init__.py                      # 包初始化文件
├── README.md                        # 本文件
├── PACKAGE_SUMMARY.md               # 包的整体总结
├── lattereview_wrapper.py           # 核心包装函数
├── example_lattereview_usage.py     # 详细使用示例
├── example_with_final_score.py      # 最终分数计算示例
├── simple_example.py                # 简单使用示例
├── test_lattereview_wrapper.py      # 功能测试
├── requirements_lattereview.txt     # 依赖包列表
├── README_LatteReview_Wrapper.md    # 详细功能说明
└── QUICKSTART_LatteReview.md       # 快速开始指南
```

## 🚀 快速开始

### 1. 安装依赖

```bash
cd AutoSurvey/lattereview_wrapper
pip install -r requirements_lattereview.txt
```

### 2. 基本使用

```python
from lattereview_wrapper import run_lattereview_evaluation_sync

result = run_lattereview_evaluation_sync(
    topic="AI Research",
    reviewer_models=["gpt-4o-mini", "gpt-4.1-mini", "gpt-5-mini"],
    papers=[
        {
            "id": "1",
            "title": "Paper Title",
            "abstract": "Paper abstract..."
        }
    ],
    top_n=3  # 输出前3篇论文
)
```

## 🔧 主要功能

### 智能评审流程
- **Round A**: Conservative + Balanced 评审者评审所有论文
- **Round B**: 只有当两个Junior评分差异≥2分时，Senior评审者才评审
- **成本优化**: 避免不必要的Senior评审，节省API调用成本

### 最终分数计算算法
按照paper中的算法计算每篇论文的最终分数 S_final：

1. **优先**: `round-B_Senior_Reviewer_evaluation` (Senior在Round B的评分)
2. **其次**: `round-A_Senior_Reviewer_evaluation` (Senior在Round A的评分)  
3. **最后**: 两位Junior评审者的平均分
   - `(Conservative_Reviewer_evaluation + Balanced_Reviewer_evaluation) / 2`

### 智能参数配置
- **GPT-5系列模型**: `temperature = 1.0`（锁定）
- **其他模型**: `temperature = 0.2`

## 📊 输出结果

### 新增字段
```python
{
    "success": True,
    "topic": "研究主题",
    "reviewer_models": ["模型列表"],
    "total_papers": 10,
    "duration_seconds": 45.2,
    "total_cost": 0.1234,
    "results": [...],
    "analysis": {
        "topic": "研究主题",
        "reviewer_models": ["模型列表"],
        "total_papers": 10,
        "review_rounds": [...],
        "score_distribution": {...},
        "high_score_papers": [...],     # 高分论文 (≥4分)
        "top_papers": [...]            # 🆕 按最终分数排序的前N篇论文
    }
}
```

### top_papers 结构
```python
[
    {
        "id": "paper_001",
        "title": "论文标题",
        "final_score": 4.5,           # 最终分数
        "all_scores": [4, 5, 4.5],   # 所有评审分数
        "score_details": {             # 详细分数信息
            "round-A_Conservative_Reviewer_evaluation": 4,
            "round-A_Balanced_Reviewer_evaluation": 5,
            "round-B_Senior_Reviewer_evaluation": 4.5
        }
    }
]
```

## 🎯 使用场景

### 1. 获取前N篇论文
```python
# 获取前5篇论文
result = run_lattereview_evaluation_sync(
    topic="Machine Learning",
    reviewer_models=["gpt-4o-mini", "gpt-4.1-mini", "gpt-5-mini"],
    papers=papers,
    top_n=5  # 指定输出前5篇
)

# 获取前N篇论文
top_papers = result['analysis']['top_papers']
for paper in top_papers:
    print(f"{paper['title']}: {paper['final_score']:.2f}")
```

### 2. 分析评审分歧
```python
# 查看哪些论文需要Senior评审
for paper in result['analysis']['top_papers']:
    if 'round-B_Senior_Reviewer_evaluation' in paper['score_details']:
        print(f"需要Senior评审: {paper['title']}")
```

### 3. 成本分析
```python
print(f"总成本: ${result['total_cost']:.4f}")
print(f"每篇论文成本: ${result['total_cost']/result['total_papers']:.4f}")
```

## 📚 文档导航

- **快速开始**: `QUICKSTART_LatteReview.md` - 5分钟上手指南
- **详细文档**: `README_LatteReview_Wrapper.md` - 完整功能说明
- **最终分数示例**: `example_with_final_score.py` - 新功能使用示例
- **使用示例**: `example_lattereview_usage.py` - 各种使用场景
- **功能测试**: `test_lattereview_wrapper.py` - 验证功能正常性

## 🔧 主要函数

### `run_lattereview_evaluation_sync()`
```python
def run_lattereview_evaluation_sync(
    topic: str,                    # 研究主题
    reviewer_models: List[str],    # 评审者模型列表
    papers: List[Dict],           # 论文列表
    inclusion_criteria: str = None,    # 纳入标准
    exclusion_criteria: str = None,    # 排除标准
    output_dir: str = None,           # 输出目录
    top_n: int = None                # 🆕 输出前N篇论文
) -> Dict[str, Any]
```

## 💡 使用建议

1. **先阅读快速开始指南**，了解基本用法
2. **使用top_n参数**，获取指定数量的高分论文
3. **监控API成本**，利用智能评审流程节省费用
4. **分析评审分歧**，了解哪些论文需要额外关注

## 🆘 获取帮助

- 运行测试脚本检查环境配置
- 查看详细文档了解具体用法
- 参考示例代码学习最佳实践
- 运行 `example_with_final_score.py` 了解新功能

---

**开始使用**: 查看 `QUICKSTART_LatteReview.md` 获取快速上手指南！
