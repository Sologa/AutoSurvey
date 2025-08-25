"""
LatteReview Wrapper Package for AutoSurvey

这个包封装了LatteReview的评审流程，提供简单的函数接口。
"""

from .lattereview_wrapper import (
    run_lattereview_evaluation,
    run_lattereview_evaluation_sync,
    create_provider,
    create_reviewers,
    create_workflow,
    analyze_results,
    save_results,
    _calculate_final_score,
    _extract_score,
    _has_disagreement,
    _extract_reasons
)

__version__ = "1.2.0"
__author__ = "AutoSurvey Team"

__all__ = [
    "run_lattereview_evaluation",
    "run_lattereview_evaluation_sync", 
    "create_provider",
    "create_reviewers",
    "create_workflow",
    "analyze_results",
    "save_results",
    "_calculate_final_score",
    "_extract_score",
    "_has_disagreement",
    "_extract_reasons"
]

# 便捷导入
__main_functions__ = [
    "run_lattereview_evaluation_sync"  # 主要的同步函数
]
