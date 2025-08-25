# 文件组织说明

本文档说明AutoSurvey项目重新组织后的文件结构，特别是关于执行脚本和测试文件的分类管理。

## 新的目录结构

```
AutoSurvey/
├── scripts/                    # 执行脚本目录
│   ├── with_keys/             # 包含API密钥的脚本（不要commit到git）
│   │   ├── run_example_with_keys.sh
│   │   └── run_research_survey_with_keys.sh
│   ├── without_keys/          # 无密钥的模板脚本（可以commit到git）
│   │   ├── run_example_template.sh
│   │   └── run_research_survey_template.sh
│   └── README.md              # 脚本使用说明
├── tests/                     # 测试文件目录
│   ├── test_paper_provider.py
│   ├── use_lattereview_wrapper.py
│   └── README.md              # 测试文件说明
├── .gitignore                 # 已更新，忽略包含密钥的脚本
└── ... (其他项目文件)
```

## 文件分类说明

### 1. 执行脚本 (`scripts/`)

#### `without_keys/` - 安全版本
- **用途**: 作为模板和示例，展示如何配置脚本
- **特点**: 不包含敏感信息，可以安全地commit到git
- **包含文件**: 
  - `run_example_template.sh` - 基础示例运行脚本模板
  - `run_research_survey_template.sh` - 研究主题生成脚本模板

#### `with_keys/` - 生产版本
- **用途**: 实际运行脚本，包含你的API密钥
- **特点**: 包含敏感信息，**绝对不能commit到git**
- **包含文件**:
  - `run_example_with_keys.sh` - 基础示例运行脚本（有密钥）
  - `run_research_survey_with_keys.sh` - 研究主题生成脚本（有密钥）

### 2. 测试文件 (`tests/`)
- **用途**: 存放各种测试和示例文件
- **特点**: 不包含敏感信息，可以commit到git
- **包含文件**:
  - `test_paper_provider.py` - Paper Provider模块测试
  - `use_lattereview_wrapper.py` - LatteReview包装器使用示例

## 安全措施

### .gitignore 更新
已更新`.gitignore`文件，添加了：
```
# Scripts with sensitive information
scripts/with_keys/
```

这确保包含API密钥的脚本永远不会被意外提交到git。

### 使用建议
1. **开发阶段**: 使用`without_keys/`目录中的模板脚本
2. **生产使用**: 复制模板到`with_keys/`目录，填入实际密钥
3. **版本控制**: 只commit`without_keys/`和`tests/`目录中的文件

## 使用方法

### 首次设置
```bash
# 1. 复制模板脚本
cp scripts/without_keys/run_example_template.sh scripts/with_keys/run_example_with_keys.sh
cp scripts/without_keys/run_research_survey_template.sh scripts/with_keys/run_research_survey_with_keys.sh

# 2. 编辑脚本，填入你的API密钥
# 编辑 scripts/with_keys/ 目录中的脚本文件
```

### 运行脚本
```bash
# 运行有密钥版本的脚本
bash scripts/with_keys/run_example_with_keys.sh
bash scripts/with_keys/run_research_survey_with_keys.sh

# 或者使用环境变量运行模板版本
export OPENAI_API_KEY="your_key"
export OPENAI_ORGANIZATION_ID="your_org_id"
bash scripts/without_keys/run_example_template.sh
```

## 优势

1. **安全性**: 敏感信息与可共享代码完全分离
2. **可维护性**: 清晰的目录结构，易于管理
3. **协作友好**: 团队成员可以安全地共享代码，不会意外泄露密钥
4. **版本控制**: 模板脚本可以版本化，便于跟踪配置变化

## 注意事项

⚠️ **重要提醒**:
- 永远不要将`scripts/with_keys/`目录中的文件commit到git
- 定期检查git状态，确保没有意外提交包含密钥的文件
- 如果需要在不同机器上使用，记得重新配置API密钥
- 建议使用环境变量作为替代方案，避免在脚本中硬编码密钥
