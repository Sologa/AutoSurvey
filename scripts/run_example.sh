#!/bin/bash

# AutoSurvey 修改版本使用示例
# 使用预选的paper生成survey

echo "🚀 启动AutoSurvey修改版本..."
echo "使用预选的paper生成survey"
echo ""

# 设置参数
TOPIC="Large Language Models (LLMs) in Academic Research Applications: A Comprehensive Survey"
MODEL="gpt-4o-2024-05-13"
SAVING_PATH="./output/"
SECTION_NUM=7
SUBSECTION_LEN=700
RAG_NUM=60
OUTLINE_REFERENCE_NUM=1500
PAPER_JSON_PATH="/Users/xjp/Desktop/Survey with LLMs/Survey for survey:review with LLMs/LatteReview/evaluation_results/test/20250824/high_score_papers_20250824.json"

# 检查必要文件
if [ ! -f "$PAPER_JSON_PATH" ]; then
    echo "❌ 错误: 找不到paper JSON文件: $PAPER_JSON_PATH"
    echo "请检查文件路径是否正确"
    exit 1
fi

echo "📋 参数设置:"
echo "  主题: $TOPIC"
echo "  模型: $MODEL"
echo "  输出路径: $SAVING_PATH"
echo "  章节数: $SECTION_NUM"
echo "  子章节长度: $SUBSECTION_LEN"
echo "  RAG数量: $RAG_NUM"
echo "  大纲参考数: $OUTLINE_REFERENCE_NUM"
echo "  Paper JSON: $PAPER_JSON_PATH"
echo ""

# 创建输出目录
mkdir -p "$SAVING_PATH"

echo "🔍 检查环境..."
if [ ! -f "main.py" ]; then
    echo "❌ 错误: 找不到main.py文件"
    exit 1
fi

if [ ! -f "src/paper_provider.py" ]; then
    echo "❌ 错误: 找不到paper_provider.py文件"
    exit 1
fi

echo "✅ 环境检查通过"
echo ""

echo "📚 开始生成survey..."
echo "注意: 你需要设置OPENAI_API_KEY环境变量或使用--api_key参数"
echo ""

# 运行命令（你需要添加你的API key和organization ID）
echo "运行命令:"
echo "python main.py \\"
echo "  --topic \"$TOPIC\" \\"
echo "  --model \"$MODEL\" \\"
echo "  --saving_path \"$SAVING_PATH\" \\"
echo "  --section_num $SECTION_NUM \\"
echo "  --subsection_len $SUBSECTION_LEN \\"
echo "  --rag_num $RAG_NUM \\"
echo "  --outline_reference_num $OUTLINE_REFERENCE_NUM \\"
echo "  --paper_json_path \"$PAPER_JSON_PATH\" \\"
echo "  --api_key YOUR_API_KEY_HERE \\"
echo "  --organization_id YOUR_ORGANIZATION_ID_HERE"
echo ""

echo "💡 提示:"
echo "1. 将YOUR_API_KEY_HERE替换为你的实际API key"
echo "2. 将YOUR_ORGANIZATION_ID_HERE替换为你的OpenAI organization ID"
echo "3. 或者设置环境变量:"
echo "   export OPENAI_API_KEY=your_key_here"
echo "   export OPENAI_ORGANIZATION_ID=your_org_id_here"
echo "4. 生成完成后，结果将保存在 $SAVING_PATH 目录中"
echo "5. 如果遇到问题，可以查看README_MODIFIED.md获取详细说明"
