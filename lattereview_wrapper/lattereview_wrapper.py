#!/usr/bin/env python3
"""
LatteReview Wrapper for AutoSurvey
封装LatteReview的评审流程，提供简单的函数接口
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
import pandas as pd

# 添加LatteReview路径
latte_review_path = Path(__file__).parent.parent / "LatteReview"
sys.path.append(str(latte_review_path))

from lattereview.providers import OpenAIProvider, GoogleProvider, OllamaProvider, LiteLLMProvider
from lattereview.agents import TitleAbstractReviewer
from lattereview.workflows import ReviewWorkflow


def create_provider(model_name: str):
    """创建模型提供者"""
    if model_name.startswith("gpt-"):
        return OpenAIProvider(model=model_name)
    elif model_name.startswith("claude-"):
        return GoogleProvider(model=model_name)
    elif model_name.startswith("gemini-"):
        return GoogleProvider(model=model_name)
    elif model_name.startswith("o4-") or model_name.startswith("o3-"):
        return OpenAIProvider(model=model_name)
    elif model_name.startswith("llama-") or model_name.startswith("mistral-"):
        return OllamaProvider(model=model_name)
    else:
        # 默认使用LiteLLM
        return LiteLLMProvider(model=model_name)


def create_reviewers(
    reviewer_models: List[str],
    topic: str,
    inclusion_criteria: Optional[str] = None,
    exclusion_criteria: Optional[str] = None
) -> List[TitleAbstractReviewer]:
    """创建评审者"""
    reviewers = []
    
    # 默认评审标准
    if inclusion_criteria is None:
        inclusion_criteria = f"""
        Research must be related to the following topic:
        {topic}
        
        The paper should demonstrate:
        1. Clear research contribution
        2. Well-defined methodology
        3. Relevant to the specified topic area
        4. Academic quality and rigor
        """
    
    if exclusion_criteria is None:
        exclusion_criteria = """
        Exclude the following research:
        1. Non-English papers
        2. Non-peer-reviewed papers
        3. Research unrelated to the specified topic
        4. Pure theoretical research without practical application
        5. Duplicate papers
        6. Non-academic content
        """
    
    # 评审者配置
    reviewer_configs = [
        {
            "name": "Conservative_Reviewer",
            "backstory": "Conservative review expert who strictly follows inclusion criteria",
            "reasoning": "brief",
            "model": reviewer_models[0] if len(reviewer_models) > 0 else "gpt-4o-mini"
        },
        {
            "name": "Balanced_Reviewer", 
            "backstory": "Balanced review expert who considers multiple factors comprehensively",
            "reasoning": "cot",
            "model": reviewer_models[1] if len(reviewer_models) > 1 else "gpt-4.1-mini"
        },
        {
            "name": "Senior_Reviewer",
            "backstory": "Senior AI research expert with extensive experience in the field",
            "reasoning": "cot", 
            "model": reviewer_models[2] if len(reviewer_models) > 2 else "gpt-5-mini"
        }
    ]
    
    for i, config in enumerate(reviewer_configs[:len(reviewer_models)]):
        # 为每个评审者创建专门的provider
        provider = create_provider(config["model"])
        
        # 设置temperature参数
        model_args = {}
        if config["model"].startswith("gpt-5"):
            model_args["temperature"] = 1.0  # gpt-5开头的模型锁定temperature为1.0
        else:
            model_args["temperature"] = 0.2  # 其他非reasoning LLM设置为0.2
        
        reviewer = TitleAbstractReviewer(
            provider=provider,
            name=config["name"],
            backstory=config["backstory"],
            inclusion_criteria=inclusion_criteria,
            exclusion_criteria=exclusion_criteria,
            reasoning=config["reasoning"],
            model_args=model_args
        )
        
        reviewers.append(reviewer)
        print(f"Created reviewer {i+1}: {config['name']} (using model: {config['model']})")
    
    return reviewers


def create_workflow(reviewers: List[TitleAbstractReviewer]) -> ReviewWorkflow:
    """创建评审工作流"""
    if len(reviewers) >= 3:
        # 实现正确的两阶段评审逻辑
        workflow_schema = [
            {
                "round": "A",
                "reviewers": reviewers[:2],  # 前两个评审者（Conservative + Balanced）
                "text_inputs": ["title", "abstract"],
                "filter": lambda x: True,
            },
            {
                "round": "B", 
                "reviewers": [reviewers[2]],  # 第三个评审者（Senior）
                "text_inputs": ["title", "abstract"],
                "filter": lambda x: _has_disagreement(x),  # 只有当有分歧时才评审
            }
        ]
    else:
        # 如果评审者少于3个，使用单轮评审
        workflow_schema = [
            {
                "round": "A",
                "reviewers": reviewers,  # 所有评审者
                "text_inputs": ["title", "abstract"],
                "filter": lambda x: True,
            }
        ]
    
    return ReviewWorkflow(workflow_schema=workflow_schema, verbose=True)


def _has_disagreement(row: pd.Series) -> bool:
    """检查两个junior评审者是否需要升级到Round-B
    
    升级条件（符合LatteReview要求）：
    1. 两位junior分数不一致
    2. 两位junior都給3分（不確定）
    """
    conservative_col = "round-A_Conservative_Reviewer_evaluation"
    balanced_col = "round-A_Balanced_Reviewer_evaluation"
    
    if conservative_col in row and balanced_col in row:
        try:
            conservative_score = _extract_score(row[conservative_col])
            balanced_score = _extract_score(row[balanced_col])
            
            if conservative_score is not None and balanced_score is not None:
                # 条件1: 分数不一致
                if abs(conservative_score - balanced_score) >= 1:
                    return True
                
                # 条件2: 都給3分（不確定）
                if conservative_score == 3 and balanced_score == 3:
                    return True
                
        except:
            pass
    
    return False


def _extract_score(value) -> Optional[float]:
    """从评审结果中提取评分"""
    if pd.isna(value):
        return None
    
    try:
        if isinstance(value, str):
            parsed = json.loads(value)
            if 'evaluation' in parsed:
                return float(parsed['evaluation'])
            else:
                return float(parsed)
        else:
            return float(value)
    except:
        return None


async def run_lattereview_evaluation(
    topic: str,
    reviewer_models: List[str],
    papers: List[Dict[str, Any]],
    inclusion_criteria: Optional[str] = None,
    exclusion_criteria: Optional[str] = None,
    output_dir: Optional[str] = None,
    top_n: Optional[int] = None,
    threshold_mode: str = "Balanced"
) -> Dict[str, Any]:
    """
    运行LatteReview评审流程
    
    Args:
        topic: 研究主题
        reviewer_models: 三个评审者使用的模型名称列表
        papers: 论文列表，每篇论文应包含title和abstract字段
        inclusion_criteria: 可选的纳入标准
        exclusion_criteria: 可选的排除标准
        output_dir: 可选的输出目录
        top_n: 可选的，输出前N篇论文（按最终分数排序）
        threshold_mode: 可选的，入选门槛模式 ("Sensitive", "Specific", "Balanced")
    
    Returns:
        包含评审结果的字典
    """
    try:
        print(f"开始LatteReview评审流程")
        print(f"主题: {topic}")
        print(f"评审者模型: {reviewer_models}")
        print(f"论文数量: {len(papers)}")
        if top_n:
            print(f"输出前 {top_n} 篇论文")
        print(f"入选门槛模式: {threshold_mode}")
        
        # 验证输入
        if len(reviewer_models) < 1:
            raise ValueError("至少需要1个评审者模型")
        
        if len(papers) == 0:
            raise ValueError("论文列表不能为空")
        
        # 检查论文格式
        for i, paper in enumerate(papers):
            if 'title' not in paper:
                raise ValueError(f"第{i+1}篇论文缺少title字段")
            if 'abstract' not in paper:
                raise ValueError(f"第{i+1}篇论文缺少abstract字段")
        
        # 转换为DataFrame
        df = pd.DataFrame(papers)
        
        # 创建评审者
        print("\n创建评审者...")
        reviewers = create_reviewers(
            reviewer_models=reviewer_models,
            topic=topic,
            inclusion_criteria=inclusion_criteria,
            exclusion_criteria=exclusion_criteria
        )
        
        # 创建工作流
        print("创建评审工作流...")
        workflow = create_workflow(reviewers)
        
        # 运行评审
        print(f"\n开始评审 {len(df)} 篇论文...")
        start_time = asyncio.get_event_loop().time()
        
        results = await workflow(df)
        
        end_time = asyncio.get_event_loop().time()
        duration = end_time - start_time
        
        # 获取成本信息
        total_cost = workflow.get_total_cost()
        
        print(f"评审完成! 耗时: {duration:.2f} 秒")
        print(f"总成本: ${total_cost:.4f}")
        
        # 分析结果
        analysis = analyze_results(results, topic, reviewer_models, top_n, threshold_mode)
        
        # 保存结果（如果指定了输出目录）
        if output_dir:
            save_results(results, analysis, output_dir, topic)
        
        return {
            "success": True,
            "topic": topic,
            "reviewer_models": reviewer_models,
            "total_papers": len(results),
            "duration_seconds": duration,
            "total_cost": total_cost,
            "results": results.to_dict('records'),
            "analysis": analysis
        }
        
    except Exception as e:
        print(f"评审过程中出错: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "topic": topic,
            "reviewer_models": reviewer_models
        }


def analyze_results(results: pd.DataFrame, topic: str, reviewer_models: List[str], top_n: Optional[int] = None, threshold_mode: str = "Balanced") -> Dict[str, Any]:
    """分析评审结果
    
    Args:
        results: 评审结果DataFrame
        topic: 研究主题
        reviewer_models: 评审者模型列表
        top_n: 输出前N篇论文
        threshold_mode: 入选门槛模式 ("Sensitive", "Specific", "Balanced")
    """
    # 定义入选门槛（符合LatteReview要求）
    threshold_values = {
        "Sensitive": 1.5,    # 召回优先，门槛较低
        "Specific": 3.0,     # 平衡模式
        "Balanced": 4.5      # 精确优先，门槛较高
    }
    
    if threshold_mode not in threshold_values:
        raise ValueError(f"无效的threshold_mode: {threshold_mode}。支持的模式: {list(threshold_values.keys())}")
    
    threshold = threshold_values[threshold_mode]
    
    analysis = {
        "topic": topic,
        "reviewer_models": reviewer_models,
        "total_papers": len(results),
        "review_rounds": [],
        "score_distribution": {},
        "high_score_papers": [],
        "top_papers": [],  # 按最终分数排序的前N篇论文
        "inclusion_analysis": {  # 🆕 新增：入选分析
            "threshold_mode": threshold_mode,
            "threshold_value": threshold,
            "included_papers": [],
            "excluded_papers": [],
            "inclusion_rate": 0.0
        }
    }
    
    # 分析每轮评审
    for col in results.columns:
        if col.startswith('round-') and col.endswith('_evaluation'):
            round_name = col.split('_')[0]
            reviewer_name = '_'.join(col.split('_')[1:-1])
            
            if round_name not in [r["round"] for r in analysis["review_rounds"]]:
                analysis["review_rounds"].append({
                    "round": round_name,
                    "reviewers": []
                })
            
            round_data = next(r for r in analysis["review_rounds"] if r["round"] == round_name)
            evaluations = results[col].dropna()
            
            # 转换numpy类型为Python原生类型
            eval_dist = evaluations.value_counts().to_dict()
            eval_dist = {str(k): int(v) for k, v in eval_dist.items()}
            
            round_data["reviewers"].append({
                "name": reviewer_name,
                "total_reviews": int(len(evaluations)),
                "evaluation_distribution": eval_dist,
                "mean_evaluation": float(evaluations.mean()) if not pd.isna(evaluations.mean()) else None,
                "std_evaluation": float(evaluations.std()) if not pd.isna(evaluations.std()) else None
            })
    
    # 计算每篇论文的最终分数并分析
    papers_with_final_scores = []
    included_count = 0
    
    for _, row in results.iterrows():
        # 计算最终分数 S_final
        final_score = _calculate_final_score(row)
        
        if final_score is not None:
            paper_info = {
                "id": row.get('id', ''),
                "title": row.get('title', ''),
                "final_score": final_score,
                "all_scores": _extract_all_scores(row),
                "score_details": _get_score_details(row),
                "reasons": _extract_reasons(row),  # 🆕 新增：提取理由
                "is_included": final_score >= threshold  # 🆕 新增：是否入选
            }
            
            papers_with_final_scores.append(paper_info)
            
            # 检查是否入选
            if paper_info["is_included"]:
                included_count += 1
                analysis["inclusion_analysis"]["included_papers"].append(paper_info)
            else:
                analysis["inclusion_analysis"]["excluded_papers"].append(paper_info)
            
            # 检查是否为高分论文（≥4分）
            if final_score >= 4:
                analysis["high_score_papers"].append(paper_info)
    
    # 计算入选率
    if papers_with_final_scores:
        analysis["inclusion_analysis"]["inclusion_rate"] = included_count / len(papers_with_final_scores)
    
    # 按最终分数排序
    papers_with_final_scores.sort(key=lambda x: x['final_score'], reverse=True)
    
    # 设置top_n的默认值
    if top_n is None:
        top_n = len(papers_with_final_scores)
    
    # 获取前N篇论文
    analysis["top_papers"] = papers_with_final_scores[:top_n]
    
    # 按最高分排序高分论文
    analysis["high_score_papers"].sort(key=lambda x: x['final_score'], reverse=True)
    
    return analysis


def _calculate_final_score(row: pd.Series) -> Optional[float]:
    """按照paper算法计算最终分数 S_final"""
    try:
        # 1. 若有 round-B_Senior_Reviewer_evaluation → 用它当 S_final
        senior_b_col = "round-B_Senior_Reviewer_evaluation"
        if senior_b_col in row and pd.notna(row[senior_b_col]):
            score = _extract_score(row[senior_b_col])
            if score is not None:
                return score
        
        # 2. 否则若有 round-A_Senior_Reviewer_evaluation → 用它
        senior_a_col = "round-A_Senior_Reviewer_evaluation"
        if senior_a_col in row and pd.notna(row[senior_a_col]):
            score = _extract_score(row[senior_a_col])
            if score is not None:
                return score
        
        # 3. 否则取两位 junior 的平均
        conservative_col = "round-A_Conservative_Reviewer_evaluation"
        balanced_col = "round-A_Balanced_Reviewer_evaluation"
        
        conservative_score = _extract_score(row.get(conservative_col))
        balanced_score = _extract_score(row.get(balanced_col))
        
        if conservative_score is not None and balanced_score is not None:
            return (conservative_score + balanced_score) / 2
        
        # 如果只有一个junior的分数，使用它
        if conservative_score is not None:
            return conservative_score
        if balanced_score is not None:
            return balanced_score
        
        return None
        
    except Exception as e:
        print(f"计算最终分数时出错: {e}")
        return None


def _extract_all_scores(row: pd.Series) -> List[float]:
    """提取所有评审分数"""
    scores = []
    for col in row.index:
        if col.endswith('_evaluation'):
            try:
                value = row[col]
                if pd.notna(value):
                    score = _extract_score(value)
                    if score is not None:
                        scores.append(score)
            except:
                continue
    return scores


def _extract_reasons(row: pd.Series) -> Dict[str, str]:
    """提取评审理由（符合LatteReview要求：每个分数都要附理由）"""
    reasons = {}
    
    # 提取各轮评审的理由
    for col in row.index:
        if col.endswith('_output') or col.endswith('_reasoning'):
            try:
                value = row[col]
                if pd.notna(value):
                    if isinstance(value, str):
                        try:
                            # 尝试解析JSON格式的输出
                            parsed = json.loads(value)
                            if 'reasoning' in parsed:
                                reasons[col] = parsed['reasoning']
                            elif 'reason' in parsed:
                                reasons[col] = parsed['reason']
                            else:
                                # 如果没有找到reasoning字段，使用整个输出
                                reasons[col] = str(parsed)
                        except:
                            # 如果不是JSON，直接使用字符串
                            reasons[col] = value
                    else:
                        reasons[col] = str(value)
            except:
                continue
    
    return reasons


def _get_score_details(row: pd.Series) -> Dict[str, Any]:
    """获取详细的评分信息"""
    details = {}
    
    # 提取各轮评审的分数
    for col in row.index:
        if col.endswith('_evaluation'):
            try:
                value = row[col]
                if pd.notna(value):
                    score = _extract_score(value)
                    if score is not None:
                        details[col] = score
            except:
                continue
    
    return details


def save_results(results: pd.DataFrame, analysis: Dict[str, Any], output_dir: str, topic: str):
    """保存评审结果"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 保存原始结果
    results_file = output_path / f"lattereview_results_{topic.replace(' ', '_')}.json"
    results.to_json(results_file, orient='records', indent=2, force_ascii=False)
    
    # 保存分析结果
    analysis_file = output_path / f"lattereview_analysis_{topic.replace(' ', '_')}.json"
    with open(analysis_file, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    
    print(f"结果已保存到: {output_path}")
    print(f"  - 评审结果: {results_file.name}")
    print(f"  - 分析结果: {analysis_file.name}")


# 同步版本的包装函数
def run_lattereview_evaluation_sync(
    topic: str,
    reviewer_models: List[str],
    papers: List[Dict[str, Any]],
    inclusion_criteria: Optional[str] = None,
    exclusion_criteria: Optional[str] = None,
    output_dir: Optional[str] = None,
    top_n: Optional[int] = None,
    threshold_mode: str = "Balanced"
) -> Dict[str, Any]:
    """
    同步版本的LatteReview评审函数
    
    Args:
        topic: 研究主题
        reviewer_models: 三个评审者使用的模型名称列表
        papers: 论文列表，每篇论文应包含title和abstract字段
        inclusion_criteria: 可选的纳入标准
        exclusion_criteria: 可选的排除标准
        output_dir: 可选的输出目录
        top_n: 可选的，输出前N篇论文（按最终分数排序）
        threshold_mode: 可选的，入选门槛模式 ("Sensitive", "Specific", "Balanced")
    
    Returns:
        包含评审结果的字典
    """
    return asyncio.run(run_lattereview_evaluation(
        topic=topic,
        reviewer_models=reviewer_models,
        papers=papers,
        inclusion_criteria=inclusion_criteria,
        exclusion_criteria=exclusion_criteria,
        output_dir=output_dir,
        top_n=top_n,
        threshold_mode=threshold_mode
    ))


# 示例使用
if __name__ == "__main__":
    # 示例数据
    example_topic = "Large Language Models in Academic Research"
    example_reviewers = ["gpt-4o-mini", "gpt-4.1-mini", "gpt-5-mini"]
    example_papers = [
        {
            "id": "1",
            "title": "Example Paper 1",
            "abstract": "This is an example abstract for paper 1."
        },
        {
            "id": "2", 
            "title": "Example Paper 2",
            "abstract": "This is an example abstract for paper 2."
        }
    ]
    
    # 运行评审
    result = run_lattereview_evaluation_sync(
        topic=example_topic,
        reviewer_models=example_reviewers,
        papers=example_papers,
        output_dir="./output"
    )
    
    print("评审结果:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
