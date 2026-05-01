"""
宏观经济周期研判引擎
====================
打分标准化 → 因子合成 → 周期概率映射
"""
import math
from typing import Dict, Tuple, List, Optional
from config import (
    MERRILL_LYNCH_CONFIG,
    DOLLAR_TIDE_CONFIG,
    CYCLE_DEFINITIONS,
    DOLLAR_PHASES,
    SCORING_PARAMS,
)


def normalize_score(
    value: float,
    neutral_low: float,
    neutral_high: float,
    bearish_threshold: Optional[float] = None,
    bullish_threshold: Optional[float] = None,
    hawkish_threshold: Optional[float] = None,
    dovish_threshold: Optional[float] = None,
    risk_off_threshold: Optional[float] = None,
    risk_on_threshold: Optional[float] = None,
) -> float:
    """
    将原始指标值映射到 0—100 标准分。

    核心逻辑：
    - 在中性区间内 → 50 分
    - 超出中性区间 → 根据距离线性/非线性映射
    - 越偏离中性越接近极端分数（0 或 100）

    参数支持多种阈值命名 (bullish/bearish, hawkish/dovish, risk_on/risk_off)
    """
    low_threshold = bearish_threshold or dovish_threshold or risk_on_threshold
    high_threshold = bullish_threshold or hawkish_threshold or risk_off_threshold

    if low_threshold is None:
        low_threshold = neutral_low - (neutral_high - neutral_low) * 1.5
    if high_threshold is None:
        high_threshold = neutral_high + (neutral_high - neutral_low) * 1.5

    if neutral_low <= value <= neutral_high:
        return 50.0

    if value > neutral_high:
        over_range = max(high_threshold - neutral_high, 0.01)
        ratio = min((value - neutral_high) / over_range, 1.0)
        return 50.0 + ratio * 50.0

    else:
        under_range = max(neutral_low - low_threshold, 0.01)
        ratio = min((neutral_low - value) / under_range, 1.0)
        return 50.0 - ratio * 50.0


def compute_factor_score(
    indicators: Dict[str, Dict[str, float]],
    config: Dict[str, Dict],
) -> Tuple[float, Dict[str, float]]:
    """
    计算某一大类因子的加权得分。

    参数
    ----
    indicators : {indicator_key: {"value": float, ...}, ...}
    config     : 来自 MERRILL_LYNCH_CONFIG / DOLLAR_TIDE_CONFIG 的对应分组

    返回
    ----
    (weighted_score, individual_scores)
    """
    total_weight = 0.0
    weighted_sum = 0.0
    individual = {}

    for key, cfg in config.items():
        if key not in indicators:
            continue
        raw_value = indicators[key]["value"]
        weight = cfg["weight"]

        score = normalize_score(
            raw_value,
            neutral_low=cfg["neutral_low"],
            neutral_high=cfg["neutral_high"],
            bearish_threshold=cfg.get("bearish_threshold"),
            bullish_threshold=cfg.get("bullish_threshold"),
            hawkish_threshold=cfg.get("hawkish_threshold"),
            dovish_threshold=cfg.get("dovish_threshold"),
            risk_off_threshold=cfg.get("risk_off_threshold"),
            risk_on_threshold=cfg.get("risk_on_threshold"),
        )

        weighted_sum += score * weight
        total_weight += weight
        individual[key] = score

    if total_weight == 0:
        return 50.0, individual

    return weighted_sum / total_weight, individual


def compute_merrill_lynch_scores(
    indicators: Dict[str, Dict[str, float]]
) -> Dict:
    """
    美林时钟 — 计算增长因子 & 通胀因子得分。

    返回
    ----
    {
        "growth_score": float,
        "inflation_score": float,
        "growth_detail": {...},
        "inflation_detail": {...},
    }
    """
    growth_score, growth_detail = compute_factor_score(
        indicators, MERRILL_LYNCH_CONFIG["growth_indicators"]
    )
    inflation_score, inflation_detail = compute_factor_score(
        indicators, MERRILL_LYNCH_CONFIG["inflation_indicators"]
    )

    return {
        "growth_score": round(growth_score, 1),
        "inflation_score": round(inflation_score, 1),
        "growth_detail": {k: round(v, 1) for k, v in growth_detail.items()},
        "inflation_detail": {k: round(v, 1) for k, v in inflation_detail.items()},
    }


def compute_dollar_tide_scores(
    indicators: Dict[str, Dict[str, float]]
) -> Dict:
    """
    美元潮汐 — 计算三个维度的得分。

    返回
    ----
    {
        "fed_policy_score": float,   # 高=鹰派/紧缩
        "us_strength_score": float,  # 高=美国经济强
        "global_risk_score": float,  # 高=避险情绪浓
        ...
    }
    """
    fed_policy, fed_detail = compute_factor_score(
        indicators, DOLLAR_TIDE_CONFIG["fed_policy_indicators"]
    )
    us_strength, us_detail = compute_factor_score(
        indicators, DOLLAR_TIDE_CONFIG["us_strength_indicators"]
    )
    global_risk, risk_detail = compute_factor_score(
        indicators, DOLLAR_TIDE_CONFIG["global_risk_indicators"]
    )

    return {
        "fed_policy_score": round(fed_policy, 1),
        "us_strength_score": round(us_strength, 1),
        "global_risk_score": round(global_risk, 1),
        "fed_policy_detail": {k: round(v, 1) for k, v in fed_detail.items()},
        "us_strength_detail": {k: round(v, 1) for k, v in us_detail.items()},
        "global_risk_detail": {k: round(v, 1) for k, v in risk_detail.items()},
    }


def cycle_probability(
    growth_score: float, inflation_score: float
) -> Dict[str, float]:
    """
    根据增长 & 通胀得分，计算落入四个周期的概率。

    使用二维高斯核密度/距离映射：
    - 四个周期的中心点定义
    - 当前点与各中心点的距离 → softmax → 概率
    """
    centers = {
        "recovery": (80.0, 20.0),
        "overheat": (80.0, 80.0),
        "stagflation": (20.0, 80.0),
        "recession": (20.0, 20.0),
    }

    distances = {}
    for phase, (g_center, i_center) in centers.items():
        d_g = (growth_score - g_center) / 30.0
        d_i = (inflation_score - i_center) / 30.0
        distances[phase] = math.sqrt(d_g**2 + d_i**2)

    min_dist = min(distances.values())
    raw_probs = {}
    for phase, dist in distances.items():
        closeness = max(min_dist, 0.01) / max(dist, 0.01)
        raw_probs[phase] = closeness

    total = sum(raw_probs.values())
    if total == 0:
        return {p: 25.0 for p in centers}

    probs = {p: round(v / total * 100, 1) for p, v in raw_probs.items()}

    smoothed = {}
    for p in probs:
        smoothed[p] = round(
            probs[p] * (1 - SCORING_PARAMS["probability_smoothing"])
            + 25.0 * SCORING_PARAMS["probability_smoothing"],
            1,
        )

    return smoothed


def dollar_tide_phase(fed_policy_score: float, global_risk_score: float) -> Dict:
    """
    判断美元潮汐所处的阶段 (紧缩 / 平台 / 宽松)。

    逻辑：
    - fed_policy_score > 65 → 紧缩倾向
    - fed_policy_score < 35 → 宽松倾向
    - 中间 → 平台期
    - global_risk_score 作为辅助调节 (高避险 → 美元偏强)
    """
    composite = fed_policy_score * 0.7 + global_risk_score * 0.3

    if composite > 65:
        phase_key = "tightening"
    elif composite < 35:
        phase_key = "easing"
    else:
        phase_key = "plateau"

    phase = DOLLAR_PHASES[phase_key].copy()
    phase["key"] = phase_key
    phase["composite_score"] = round(composite, 1)
    return phase


def compute_sector_rotation_signal(growth_score: float) -> Dict[str, str]:
    """
    根据经济增长位置，输出行业轮动信号。

    复苏 → 周期性 (科技、可选消费)
    繁荣 → 能源、材料
    滞胀 → 防御 (公用事业、医疗)
    衰退 → 防御 + 国债
    """
    if growth_score > 55 and growth_score > 55:
        return {"signal": "cyclical", "sectors": "科技、可选消费、工业"}
    elif growth_score < 45:
        return {"signal": "defensive", "sectors": "公用事业、医疗、必选消费"}
    else:
        return {"signal": "neutral", "sectors": "均衡配置，关注金融、能源"}


def run_full_analysis(
    indicators: Dict[str, Dict[str, float]]
) -> Dict:
    """
    主入口：运行全部研判逻辑。

    参数
    ----
    indicators : 从 data.fetcher 获取的指标字典

    返回
    ----
    完整的研判报告 dict
    """
    ml = compute_merrill_lynch_scores(indicators)
    dt = compute_dollar_tide_scores(indicators)
    probs = cycle_probability(ml["growth_score"], ml["inflation_score"])
    tide_phase = dollar_tide_phase(
        dt["fed_policy_score"], dt["global_risk_score"]
    )
    sector = compute_sector_rotation_signal(ml["growth_score"])

    dominant = max(probs, key=probs.get)
    confidence = probs[dominant]
    dominant_cycle = CYCLE_DEFINITIONS[dominant].copy()
    dominant_cycle["key"] = dominant
    dominant_cycle["probability"] = confidence

    return {
        "merrill_lynch": ml,
        "dollar_tide": dt,
        "cycle_probabilities": probs,
        "dominant_cycle": dominant_cycle,
        "dollar_phase": tide_phase,
        "sector_rotation": sector,
        "indicators": indicators,
    }
