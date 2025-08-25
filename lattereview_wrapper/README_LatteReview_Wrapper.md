# LatteReview Wrapper for AutoSurvey

这个文件封装了LatteReview的评审流程，提供了一个简单的函数接口，让您可以轻松地在AutoSurvey项目中使用LatteReview进行论文评审。

## 功能特性

- 🎯 **简单易用**: 一个函数调用即可完成完整的评审流程
- 🤖 **多模型支持**: 支持OpenAI、Claude、Gemini等多种LLM模型
- 📊 **智能评审**: 三个评审者分别从不同角度评估论文
- ⚡ **自动参数配置**: 根据模型类型自动设置最优参数
- 💰 **成本追踪**: 实时监控API调用成本
- 📁 **结果保存**: 自动保存评审结果和分析报告

## 安装要求

确保您的环境中已安装以下依赖：

```bash
pip install pandas openai google-generativeai anthropic
```

## 基本用法

### 1. 导入函数

```python
from lattereview_wrapper import run_lattereview_evaluation_sync
```

### 2. 准备数据

```python
# 定义研究主题
topic = "Large Language Models in Academic Research"

# 定义三个评审者模型
reviewer_models = [
    "gpt-4o-mini",      # Conservative Reviewer
    "gpt-4.1-mini",     # Balanced Reviewer  
    "gpt-5-mini"        # Senior Reviewer
]

# 准备要评审的论文
papers = [
    {
        "id": "paper_001",
        "title": "Large Language Models for Automated Literature Review",
        "abstract": "This paper presents a novel approach to using large language models..."
    },
    # ... 更多论文
]
```

### 3. 运行评审

```python
result = run_lattereview_evaluation_sync(
    topic=topic,
    reviewer_models=reviewer_models,
    papers=papers,
    output_dir="./output"
)
```

## 函数参数说明

### `run_lattereview_evaluation_sync()`

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `topic` | str | ✅ | 研究主题，用于生成评审标准 |
| `reviewer_models` | List[str] | ✅ | 三个评审者使用的模型名称列表 |
| `papers` | List[Dict] | ✅ | 论文列表，每篇论文需包含`title`和`abstract`字段 |
| `inclusion_criteria` | str | ❌ | 自定义纳入标准（可选） |
| `exclusion_criteria` | str | ❌ | 自定义排除标准（可选） |
| `output_dir` | str | ❌ | 输出目录路径（可选） |

## 模型参数自动配置

系统会根据模型类型自动设置最优参数：

- **GPT-5系列模型**: `temperature = 1.0`（锁定）
- **其他模型**: `temperature = 0.2`

### 支持的模型类型

- **OpenAI**: `gpt-4o-mini`, `gpt-4.1-mini`, `gpt-5-mini`, `gpt-5`
- **Claude**: `claude-3-sonnet`, `claude-3-opus`
- **Gemini**: `gemini-1.5-pro`, `gemini-1.5-flash`
- **Ollama**: `llama-3.1-8b`, `mistral-7b`

## 输出结果

函数返回一个包含以下信息的字典：

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

## 评审标准

### 默认纳入标准
- 与研究主题相关
- 有明确的研究贡献
- 方法学清晰
- 具有学术质量和严谨性

### 默认排除标准
- 非英文论文
- 非同行评议论文
- 与研究主题无关
- 纯理论研究且无实际应用
- 重复论文
- 非学术内容

### 评分标准
- **1分**: 绝对排除
- **2分**: 倾向于排除
- **3分**: 不确定是否纳入
- **4分**: 倾向于纳入
- **5分**: 绝对纳入

## 高级用法

### 1. 自定义评审标准

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

### 2. 批量处理

```python
# 处理大量论文
large_paper_list = [...]  # 100+ 论文

result = run_lattereview_evaluation_sync(
    topic="AI in Healthcare",
    reviewer_models=["gpt-4o-mini", "gpt-4.1-mini", "gpt-5-mini"],
    papers=large_paper_list,
    output_dir="./healthcare_review"
)
```

### 3. 不同模型组合

```python
# 混合使用不同厂商的模型
mixed_models = [
    "claude-3-sonnet",    # Anthropic
    "gemini-1.5-pro",     # Google
    "gpt-5-mini"          # OpenAI
]

result = run_lattereview_evaluation_sync(
    topic="Computer Vision",
    reviewer_models=mixed_models,
    papers=papers
)
```

## 环境变量配置

确保设置以下环境变量：

```bash
# OpenAI API
export OPENAI_API_KEY="your-openai-api-key"

# Claude API (如果需要)
export ANTHROPIC_API_KEY="your-anthropic-api-key"

# Gemini API (如果需要)
export GOOGLE_API_KEY="your-google-api-key"
```

## 错误处理

函数包含完善的错误处理机制：

- **输入验证**: 检查论文格式和必需字段
- **模型验证**: 验证模型名称和可用性
- **API错误**: 处理网络和API调用错误
- **结果验证**: 验证评审结果的完整性

## 性能优化

- **并发处理**: 支持并发评审多篇论文
- **成本控制**: 实时监控API调用成本
- **缓存机制**: 避免重复调用相同内容
- **批量处理**: 优化大量论文的处理效率

## 示例文件

- `lattereview_wrapper.py`: 主要的封装函数
- `example_lattereview_usage.py`: 详细的使用示例
- `README_LatteReview_Wrapper.md`: 本文档

## 运行示例

```bash
cd AutoSurvey
python example_lattereview_usage.py
```

## 注意事项

1. **API限制**: 注意各模型的API调用限制和速率
2. **成本控制**: 大量论文评审可能产生较高成本
3. **模型可用性**: 确保指定的模型在您的API账户中可用
4. **网络稳定性**: 评审过程需要稳定的网络连接

## 故障排除

### 常见问题

1. **模型不可用**: 检查模型名称和API密钥
2. **网络错误**: 检查网络连接和防火墙设置
3. **API限制**: 检查API调用配额和速率限制
4. **内存不足**: 大量论文处理时可能需要更多内存

### 调试模式

启用详细日志输出：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 更新日志

- **v1.0.0**: 初始版本，支持基本评审功能
- **v1.1.0**: 添加自定义评审标准支持
- **v1.2.0**: 优化模型参数自动配置
- **v1.3.0**: 增强错误处理和结果分析

## 贡献

欢迎提交问题报告和功能建议！

## 许可证

本项目遵循与AutoSurvey项目相同的许可证。
