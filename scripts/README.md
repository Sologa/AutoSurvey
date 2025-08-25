# 执行脚本目录

本目录包含AutoSurvey项目的各种执行脚本，按是否包含敏感信息进行分类。

## 目录结构

```
scripts/
├── with_keys/           # 包含API密钥的脚本（不要commit到git）
├── without_keys/        # 无密钥的模板脚本（可以commit到git）
└── README.md           # 本说明文件
```

## 脚本分类

### 1. `without_keys/` - 无密钥模板版本
- **用途**: 作为模板，展示如何配置和运行脚本
- **特点**: 不包含敏感信息，可以安全地commit到git
- **使用方法**: 复制到`with_keys/`目录，然后填入你的实际API密钥

**包含脚本**:
- `run_example_template.sh` - 基础示例运行脚本模板
- `run_research_survey_template.sh` - 研究主题生成脚本模板

### 2. `with_keys/` - 有密钥版本
- **用途**: 实际运行脚本，包含你的API密钥
- **特点**: 包含敏感信息，**绝对不能commit到git**
- **使用方法**: 直接运行，但需要先编辑脚本填入你的API密钥

**包含脚本**:
- `run_example_with_keys.sh` - 基础示例运行脚本（有密钥）
- `run_research_survey_with_keys.sh` - 研究主题生成脚本（有密钥）

## 使用方法

### 首次设置
1. 复制模板脚本到`with_keys/`目录：
   ```bash
   cp scripts/without_keys/run_example_template.sh scripts/with_keys/run_example_with_keys.sh
   cp scripts/without_keys/run_research_survey_template.sh scripts/with_keys/run_research_survey_with_keys.sh
   ```

2. 编辑`with_keys/`目录中的脚本，填入你的实际API密钥：
   ```bash
   # 将以下行中的占位符替换为实际值
   API_KEY="YOUR_ACTUAL_API_KEY_HERE"
   ORGANIZATION_ID="YOUR_ACTUAL_ORGANIZATION_ID_HERE"
   ```

### 运行脚本
```bash
# 运行示例脚本
bash scripts/with_keys/run_example_with_keys.sh

# 运行研究主题生成脚本
bash scripts/with_keys/run_research_survey_with_keys.sh
```

## 安全注意事项

⚠️ **重要**: 
- `with_keys/`目录中的脚本包含敏感信息，**永远不要commit到git**
- 建议将`scripts/with_keys/`添加到`.gitignore`文件中
- 定期检查git状态，确保没有意外提交包含密钥的文件

## 环境变量替代方案

如果你不想在脚本中硬编码API密钥，也可以使用环境变量：

```bash
# 设置环境变量
export OPENAI_API_KEY="your_actual_api_key"
export OPENAI_ORGANIZATION_ID="your_actual_org_id"

# 然后运行模板脚本（会自动使用环境变量）
bash scripts/without_keys/run_example_template.sh
```

## 故障排除

如果遇到问题：
1. 检查API密钥是否正确设置
2. 确认paper JSON文件路径是否正确
3. 查看README_MODIFIED.md获取详细说明
4. 检查Python环境和依赖是否正确安装
