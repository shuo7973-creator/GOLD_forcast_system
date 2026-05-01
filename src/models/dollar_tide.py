"""
美元潮汐模型 — 独立模块
========================
提供美元潮汐周期的专项分析接口。
"""
from typing import Dict
from .engine import compute_dollar_tide_scores, dollar_tide_phase


def analyze_dollar_tide(indicators: Dict[str, Dict[str, float]]) -> Dict:
    """
    运行美元潮汐分析并返回结构化结果。

    返回包含:
    - 三大维度得分（美联储政策 / 美国经济强度 / 全球风险）
    - 当前美元周期阶段判定
    - 对新兴市场的影响信号
    """
    scores = compute_dollar_tide_scores(indicators)
    phase = dollar_tide_phase(
        scores["fed_policy_score"], scores["global_risk_score"]
    )

    return {
        "model": "dollar_tide",
        "fed_policy_score": scores["fed_policy_score"],
        "us_strength_score": scores["us_strength_score"],
        "global_risk_score": scores["global_risk_score"],
        "fed_policy_detail": scores["fed_policy_detail"],
        "us_strength_detail": scores["us_strength_detail"],
        "global_risk_detail": scores["global_risk_detail"],
        "phase": phase,
        "liquidity_signal": "abundant" if phase["key"] == "easing" else (
            "tight" if phase["key"] == "tightening" else "neutral"
        ),
    }
