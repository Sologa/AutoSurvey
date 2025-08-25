# AutoSurvey 修改版本 - 使用预选Paper

这个修改版本允许你使用自己预先选择的paper，而不是使用原有的embedding-based检索方法。

## 主要修改

1. **新增 `PaperProvider` 类** (`src/paper_provider.py`)
   - 从JSON文件读取预选的paper信息
   - 保持与原有数据库接口的兼容性
   - 支持你已有的paper选择结果

2. **修改了主要组件**
   - `outline_writer.py` - 支持使用paper provider
   - `writer.py` - 支持使用paper provider  
   - `main.py` - 添加了新的命令行参数

3. **新增功能支持**
   - 支持OpenAI organization ID
   - 基于研究配置的主题定义
   - 更灵活的参数配置

## 使用方法

### 1. 准备Paper JSON文件

你的JSON文件应该包含以下字段的paper信息：
- `id`: paper的唯一标识符
- `title`: paper标题
- `abstract`: paper摘要
- `authors`: 作者（可选）
- `venue`: 发表场所（可选）
- `year`: 发表年份（可选）
- `arxiv_id`: arXiv ID（可选）
- `url_pdf`: PDF链接（可选）
- `url_landing`: 论文页面链接（可选）

### 2. 运行命令

使用新的 `--paper_json_path` 参数指定你的JSON文件：

```bash
python main.py --topic "Large Language Models (LLMs) in Academic Research Applications: A Comprehensive Survey" 
               --gpu 0
               --saving_path ./output/
               --model gpt-4o-2024-05-13
               --section_num 7
               --subsection_len 700
               --rag_num 60
               --outline_reference_num 1500
               --db_path ./database
               --embedding_model nomic-ai/nomic-embed-text-v1
               --api_url https://api.openai.com/v1/chat/completions
               --api_key sk-xxxxxx
               --organization_id org-xxxxxx
               --paper_json_path "/Users/xjp/Desktop/Survey with LLMs/Survey for survey:review with LLMs/LatteReview/evaluation_results/test/20250824/high_score_papers_20250824.json"
```

### 3. 兼容性

- 如果不提供 `--paper_json_path` 参数，系统会回退到原有的embedding-based检索方法
- 如果提供了JSON文件但加载失败，系统会显示警告并回退到原有方法
- 所有原有的功能都保持不变

## 工作原理

1. **Paper加载**: 系统启动时加载你提供的JSON文件中的所有paper
2. **查询处理**: 当需要检索相关paper时，系统会返回你预选的所有paper（因为已经过筛选）
3. **Survey生成**: 使用预选的paper生成survey，保持原有的生成逻辑

## 优势

1. **完全控制**: 你可以使用自己的LLM-based方法选择最相关的paper
2. **性能提升**: 避免了embedding计算和检索的开销
3. **质量保证**: 使用你精心筛选的高质量paper
4. **灵活性**: 可以随时切换回原有的检索方法

## 注意事项

1. 确保JSON文件格式正确，包含必要的字段
2. 如果paper数量很多，可能会影响内存使用
3. 建议在生成survey之前，确保你的paper选择覆盖了目标主题的各个方面

## 故障排除

如果遇到问题：

1. 检查JSON文件路径是否正确
2. 确认JSON文件格式是否符合要求
3. 查看控制台输出的错误信息
4. 如果不确定，可以暂时移除 `--paper_json_path` 参数，使用原有方法

## 示例输出

使用paper provider时，你会看到类似这样的输出：

```
Loaded 1324 papers from /Users/xjp/Desktop/Survey with LLMs/Survey for survey:review with LLMs/LatteReview/evaluation_results/test/20250824/high_score_papers_20250824.json
Using paper provider with 1324 papers
```

这表明系统成功加载了你的预选paper，并将使用它们来生成survey。

## 新增参数说明

### OpenAI Organization ID
如果你的OpenAI账户需要organization ID，可以使用 `--organization_id` 参数：

```bash
--organization_id org-xxxxxx
```

### 研究主题配置
系统现在包含了一个基于你的研究配置的主题定义文件 `research_topic_config.py`，其中包含了：

- 详细的研究主题描述
- 关键词组合
- 研究领域要求
- 应用领域范围

你可以直接使用这个预定义的主题，或者根据需要修改它。

### 环境变量支持
你也可以通过环境变量设置API密钥和organization ID：

```bash
export OPENAI_API_KEY=your_key_here
export OPENAI_ORGANIZATION_ID=your_org_id_here
```

这样就不需要在命令行中重复输入这些参数了。
