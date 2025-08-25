#!/bin/bash

# AutoSurvey 研究主题专用运行脚本 - 无密钥模板版本
# 基于用户的研究配置生成survey

echo "🚀 启动AutoSurvey研究主题生成..."
echo "主题: Large Language Models (LLMs) in Academic Research Applications"
echo ""

# 检查必要文件
PAPER_JSON_PATH="/Users/xjp/Desktop/Survey with LLMs/Survey for survey:review with LLMs/LatteReview/evaluation_results/test/20250824/high_score_papers_20250824.json"

if [ ! -f "$PAPER_JSON_PATH" ]; then
    echo "❌ 错误: 找不到paper JSON文件: $PAPER_JSON_PATH"
    exit 1
fi

# 创建输出目录
OUTPUT_DIR="./output/research_survey_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUTPUT_DIR"

echo "📋 配置信息:"
echo "  输出目录: $OUTPUT_DIR"
echo "  Paper数量: $(jq length "$PAPER_JSON_PATH")"
echo ""

# 检查环境变量
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  警告: 未设置OPENAI_API_KEY环境变量"
    echo "   请运行: export OPENAI_API_KEY=your_key_here"
    echo ""
fi

if [ -z "$OPENAI_ORGANIZATION_ID" ]; then
    echo "⚠️  警告: 未设置OPENAI_ORGANIZATION_ID环境变量"
    echo "   请运行: export OPENAI_ORGANIZATION_ID=your_org_id_here"
    echo ""
fi

echo "📚 开始生成研究survey..."
echo ""

# 运行命令
echo "执行命令:"
echo "python main.py \\"
echo "  --topic \"Large Language Models (LLMs) in Academic Research Applications: A Comprehensive Survey\" \\"
echo "  --saving_path \"$OUTPUT_DIR\" \\"
echo "  --model \"gpt-4o-2024-05-13\" \\"
echo "  --section_num 7 \\"
echo "  --subsection_len 700 \\"
echo "  --rag_num 60 \\"
echo "  --outline_reference_num 1500 \\"
echo "  --paper_json_path \"$PAPER_JSON_PATH\" \\"
echo "  --api_key \"\${OPENAI_API_KEY:-YOUR_API_KEY_HERE}\" \\"
echo "  --organization_id \"\${OPENAI_ORGANIZATION_ID:-YOUR_ORG_ID_HERE}\""
echo ""

# 询问是否继续
read -p "是否现在运行? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🚀 开始运行..."
    
    # 检查API密钥
    if [ -z "$OPENAI_API_KEY" ]; then
        echo "❌ 错误: 请先设置OPENAI_API_KEY环境变量"
        echo "💡 提示: 这是模板版本，请复制到scripts/with_keys/目录并填入你的实际密钥"
        exit 1
    fi
    
    # 运行命令
    python main.py \
        --topic "Large Language Models (LLMs) in Academic Research Applications: A Comprehensive Survey" \
        --saving_path "$OUTPUT_DIR" \
        --model "gpt-4o-2024-05-13" \
        --section_num 7 \
        --subsection_len 700 \
        --rag_num 60 \
        --outline_reference_num 1500 \
        --paper_json_path "$PAPER_JSON_PATH" \
        --api_key "$OPENAI_API_KEY" \
        --organization_id "${OPENAI_ORGANIZATION_ID:-}" \
        2>&1 | tee "$OUTPUT_DIR/run_log.txt"
    
    echo ""
    echo "✅ 完成! 结果保存在: $OUTPUT_DIR"
    echo "📄 查看日志: $OUTPUT_DIR/run_log.txt"
else
    echo "⏸️  已取消运行"
    echo ""
    echo "💡 提示:"
    echo "1. 设置环境变量:"
    echo "   export OPENAI_API_KEY=your_key_here"
    echo "   export OPENAI_ORGANIZATION_ID=your_org_id_here"
    echo "2. 然后重新运行此脚本"
    echo ""
    echo "⚠️  注意: 这是模板版本，请复制到scripts/with_keys/目录并填入你的实际密钥"
fi
