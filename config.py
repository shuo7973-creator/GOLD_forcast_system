"""
宏观经济周期研判看板 — 全局配置
================================
定义美林时钟 & 美元潮汐模型的所有指标、权重、阈值。
"""

# ============================================================
# 美林时钟模型 — 指标配置
# ============================================================
MERRILL_LYNCH_CONFIG = {
    "growth_indicators": {
        "gdp_yoy": {
            "name": "GDP 同比增速 (%)",
            "weight": 0.35,
            "neutral_low": 0.0,
            "neutral_high": 3.0,
            "bullish_threshold": 5.0,
            "bearish_threshold": -1.0,
        },
        "industrial_production_yoy": {
            "name": "工业增加值同比 (%)",
            "weight": 0.25,
            "neutral_low": 0.0,
            "neutral_high": 5.0,
            "bullish_threshold": 8.0,
            "bearish_threshold": -2.0,
        },
        "oecd_cli": {
            "name": "OECD 综合领先指标",
            "weight": 0.25,
            "neutral_low": 99.0,
            "neutral_high": 101.0,
            "bullish_threshold": 102.0,
            "bearish_threshold": 98.0,
        },
        "ism_pmi": {
            "name": "ISM 制造业 PMI",
            "weight": 0.15,
            "neutral_low": 48.0,
            "neutral_high": 52.0,
            "bullish_threshold": 55.0,
            "bearish_threshold": 45.0,
        },
    },
    "inflation_indicators": {
        "cpi_yoy": {
            "name": "CPI 同比 (%)",
            "weight": 0.35,
            "neutral_low": 1.5,
            "neutral_high": 2.5,
            "bullish_threshold": 4.0,
            "bearish_threshold": 0.0,
        },
        "core_pce_yoy": {
            "name": "核心 PCE 同比 (%)",
            "weight": 0.30,
            "neutral_low": 1.5,
            "neutral_high": 2.0,
            "bullish_threshold": 3.0,
            "bearish_threshold": 0.5,
        },
        "ppi_yoy": {
            "name": "PPI 同比 (%)",
            "weight": 0.20,
            "neutral_low": 0.0,
            "neutral_high": 3.0,
            "bullish_threshold": 5.0,
            "bearish_threshold": -2.0,
        },
        "employment_cost_index": {
            "name": "雇佣成本指数 (ECI)",
            "weight": 0.15,
            "neutral_low": 2.0,
            "neutral_high": 3.5,
            "bullish_threshold": 5.0,
            "bearish_threshold": 1.0,
        },
    },
}

# ============================================================
# 美元潮汐模型 — 指标配置
# ============================================================
DOLLAR_TIDE_CONFIG = {
    "fed_policy_indicators": {
        "fed_funds_rate": {
            "name": "联邦基金利率 (%)",
            "weight": 0.30,
            "neutral_low": 2.5,
            "neutral_high": 4.0,
            "hawkish_threshold": 5.5,
            "dovish_threshold": 1.0,
        },
        "fed_balance_sheet": {
            "name": "美联储资产负债表 (万亿美元)",
            "weight": 0.25,
            "neutral_low": 7.0,
            "neutral_high": 8.5,
            "hawkish_threshold": 6.5,
            "dovish_threshold": 9.0,
        },
        "real_rate": {
            "name": "实际利率 (Tips 10Y, %)",
            "weight": 0.25,
            "neutral_low": 0.5,
            "neutral_high": 1.5,
            "hawkish_threshold": 2.0,
            "dovish_threshold": -0.5,
        },
        "fed_dot_plot": {
            "name": "点阵图中位数预期 (bps)",
            "weight": 0.20,
            "neutral_low": -25,
            "neutral_high": 25,
            "hawkish_threshold": 50,
            "dovish_threshold": -50,
        },
    },
    "us_strength_indicators": {
        "ism_pmi": {
            "name": "ISM 制造业 PMI",
            "weight": 0.30,
            "neutral_low": 48.0,
            "neutral_high": 52.0,
            "bullish_threshold": 55.0,
            "bearish_threshold": 45.0,
        },
        "gdp_now": {
            "name": "GDPNow 预测 (%)",
            "weight": 0.25,
            "neutral_low": 1.5,
            "neutral_high": 3.0,
            "bullish_threshold": 4.0,
            "bearish_threshold": 0.0,
        },
        "nonfarm_payrolls": {
            "name": "非农就业 (万人)",
            "weight": 0.25,
            "neutral_low": 10.0,
            "neutral_high": 25.0,
            "bullish_threshold": 30.0,
            "bearish_threshold": 5.0,
        },
        "retail_sales": {
            "name": "零售销售环比 (%)",
            "weight": 0.20,
            "neutral_low": -0.2,
            "neutral_high": 0.5,
            "bullish_threshold": 1.0,
            "bearish_threshold": -1.0,
        },
    },
    "global_risk_indicators": {
        "us10y_yield": {
            "name": "美债 10Y 收益率 (%)",
            "weight": 0.25,
            "neutral_low": 3.5,
            "neutral_high": 4.5,
            "risk_off_threshold": 5.0,
            "risk_on_threshold": 3.0,
        },
        "us2y_yield": {
            "name": "美债 2Y 收益率 (%)",
            "weight": 0.20,
            "neutral_low": 3.5,
            "neutral_high": 4.5,
            "risk_off_threshold": 5.0,
            "risk_on_threshold": 3.0,
        },
        "yield_curve": {
            "name": "收益率曲线 (10Y-2Y, bp)",
            "weight": 0.20,
            "neutral_low": -20,
            "neutral_high": 50,
            "risk_off_threshold": -50,
            "risk_on_threshold": 100,
        },
        "ted_spread": {
            "name": "TED 利差 (bp)",
            "weight": 0.20,
            "neutral_low": 10.0,
            "neutral_high": 30.0,
            "risk_off_threshold": 50.0,
            "risk_on_threshold": 5.0,
        },
        "dxy": {
            "name": "美元指数 (DXY)",
            "weight": 0.15,
            "neutral_low": 100.0,
            "neutral_high": 105.0,
            "risk_off_threshold": 108.0,
            "risk_on_threshold": 95.0,
        },
    },
}

# ============================================================
# 经济周期定义 — 四象限
# ============================================================
CYCLE_DEFINITIONS = {
    "recovery": {
        "name": "复苏期",
        "name_en": "Recovery",
        "growth_zone": (55, 100),
        "inflation_zone": (0, 45),
        "color": "#27AE60",
        "description": "经济增长加速，通胀温和。股票表现优异，利好周期性行业。",
        "asset_signals": {
            "stocks": "green",
            "bonds": "yellow",
            "commodities": "yellow",
            "cash": "red",
            "gold": "yellow",
        },
    },
    "overheat": {
        "name": "繁荣期/过热",
        "name_en": "Overheat",
        "growth_zone": (55, 100),
        "inflation_zone": (55, 100),
        "color": "#E74C3C",
        "description": "经济过热，通胀上升。大宗商品表现最佳，央行倾向收紧政策。",
        "asset_signals": {
            "stocks": "yellow",
            "bonds": "red",
            "commodities": "green",
            "cash": "yellow",
            "gold": "green",
        },
    },
    "stagflation": {
        "name": "滞胀期",
        "name_en": "Stagflation",
        "growth_zone": (0, 45),
        "inflation_zone": (55, 100),
        "color": "#8E44AD",
        "description": "增长放缓而通胀高企，现金与黄金为避风港。防御型资产占优。",
        "asset_signals": {
            "stocks": "red",
            "bonds": "red",
            "commodities": "yellow",
            "cash": "green",
            "gold": "green",
        },
    },
    "recession": {
        "name": "衰退期",
        "name_en": "Recession",
        "growth_zone": (0, 45),
        "inflation_zone": (0, 45),
        "color": "#2C3E50",
        "description": "经济收缩，通缩风险上升。债券为王，防御型策略占优。",
        "asset_signals": {
            "stocks": "red",
            "bonds": "green",
            "commodities": "red",
            "cash": "yellow",
            "gold": "yellow",
        },
    },
}

# ============================================================
# 美元潮汐阶段定义
# ============================================================
DOLLAR_PHASES = {
    "tightening": {
        "name": "美元紧缩期",
        "color": "#E74C3C",
        "description": "美联储收紧货币政策，美元走强，全球流动性收缩。",
        "em_signal": "red",
    },
    "plateau": {
        "name": "美元平台期",
        "color": "#F39C12",
        "description": "利率维持高位，缩表尾部阶段，市场等待转向信号。",
        "em_signal": "yellow",
    },
    "easing": {
        "name": "美元宽松期",
        "color": "#27AE60",
        "description": "美联储降息/扩表，美元走弱，全球流动性充裕。",
        "em_signal": "green",
    },
}

# ============================================================
# 资产类别 — 红绿灯映射
# ============================================================
ASSET_CLASSES = {
    "stocks": "股票 (S&P 500)",
    "bonds": "债券 (美债综合)",
    "commodities": "大宗商品 (CRB 指数)",
    "cash": "现金/货币基金",
    "gold": "黄金 (XAUUSD)",
}

# ============================================================
# 打分系统参数
# ============================================================
SCORING_PARAMS = {
    "score_min": 0,
    "score_max": 100,
    "neutral_zone": (40, 60),
    "sigmoid_steepness": 0.15,
    "probability_smoothing": 0.1,
}
