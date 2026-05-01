"""
美林时钟模型 — 独立模块
========================
提供美林时钟的专项分析接口。
"""
from typing import Dict
from .engine import compute_merrill_lynch_scores, cycle_probability
from config import CYCLE_DEFINITIONS


def analyze_merrill_lynch(indicators: Dict[str, Dict[str, float]]) -> Dict:
    """
    运行美林时钟分析并返回结构化结果。

    返回包含:
    - 增长/通胀得分
    - 各指标明细
    - 周期概率
    - 当前象限判定
    """
    scores = compute_merrill_lynch_scores(indicators)
    probs = cycle_probability(
        scores["growth_score"], scores["inflation_score"]
    )

    dominant = max(probs, key=probs.get)

    return {
        "model": "merrill_lynch_clock",
        "growth_score": scores["growth_score"],
        "inflation_score": scores["inflation_score"],
        "growth_detail": scores["growth_detail"],
        "inflation_detail": scores["inflation_detail"],
        "cycle_probabilities": probs,
        "dominant_cycle": {
            "key": dominant,
            **CYCLE_DEFINITIONS[dominant],
            "probability": probs[dominant],
        },
        "coordinates": {
            "x": scores["growth_score"],
            "y": scores["inflation_score"],
        },
    }
