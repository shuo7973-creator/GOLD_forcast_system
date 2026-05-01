"""
数据抓取模块
============
提供模拟数据（默认）和真实数据源接口。

模拟数据基于 2024-2025 年典型宏观场景：
- 美国经济软着陆叙事
- 美联储渐进降息周期
- 通胀从高位回落但仍有粘性
"""
import os
import json
from typing import Dict, Optional
from datetime import datetime


MOCK_INDICATORS: Dict[str, Dict] = {
    "gdp_yoy": {
        "value": 2.5,
        "prev_value": 3.0,
        "trend": "down",
        "last_updated": "2025-Q1",
        "signal": "经济温和增长",
    },
    "industrial_production_yoy": {
        "value": 0.8,
        "prev_value": 1.2,
        "trend": "down",
        "last_updated": "2025-03",
        "signal": "制造业动能减弱",
    },
    "oecd_cli": {
        "value": 99.8,
        "prev_value": 100.1,
        "trend": "down",
        "last_updated": "2025-03",
        "signal": "领先指标略低于趋势",
    },
    "ism_pmi": {
        "value": 49.2,
        "prev_value": 50.3,
        "trend": "down",
        "last_updated": "2025-04",
        "signal": "PMI 跌破荣枯线",
    },
    "cpi_yoy": {
        "value": 2.8,
        "prev_value": 3.1,
        "trend": "down",
        "last_updated": "2025-03",
        "signal": "通胀缓慢回落",
    },
    "core_pce_yoy": {
        "value": 2.6,
        "prev_value": 2.7,
        "trend": "down",
        "last_updated": "2025-03",
        "signal": "核心通胀仍高于目标",
    },
    "ppi_yoy": {
        "value": 2.2,
        "prev_value": 2.5,
        "trend": "down",
        "last_updated": "2025-03",
        "signal": "生产者价格降温",
    },
    "employment_cost_index": {
        "value": 3.5,
        "prev_value": 3.8,
        "trend": "down",
        "last_updated": "2025-Q1",
        "signal": "工资增长放缓",
    },
    "fed_funds_rate": {
        "value": 4.25,
        "prev_value": 4.5,
        "trend": "down",
        "last_updated": str(datetime.now().date()),
        "signal": "美联储处于降息周期",
    },
    "fed_balance_sheet": {
        "value": 7.1,
        "prev_value": 7.3,
        "trend": "down",
        "last_updated": str(datetime.now().date()),
        "signal": "缩表持续进行中",
    },
    "real_rate": {
        "value": 1.8,
        "prev_value": 2.0,
        "trend": "down",
        "last_updated": str(datetime.now().date()),
        "signal": "实际利率偏高",
    },
    "fed_dot_plot": {
        "value": -50,
        "prev_value": 0,
        "trend": "down",
        "last_updated": "2025-03 FOMC",
        "signal": "点阵图预期降息50bp",
    },
    "gdp_now": {
        "value": 1.8,
        "prev_value": 2.3,
        "trend": "down",
        "last_updated": str(datetime.now().date()),
        "signal": "GDPNow 下修",
    },
    "nonfarm_payrolls": {
        "value": 15.1,
        "prev_value": 18.5,
        "trend": "down",
        "last_updated": "2025-03",
        "signal": "就业增长放缓",
    },
    "retail_sales": {
        "value": 0.2,
        "prev_value": 0.3,
        "trend": "down",
        "last_updated": "2025-03",
        "signal": "消费增速温和",
    },
    "us10y_yield": {
        "value": 4.15,
        "prev_value": 4.35,
        "trend": "down",
        "last_updated": str(datetime.now().date()),
        "signal": "长端利率回落",
    },
    "us2y_yield": {
        "value": 3.85,
        "prev_value": 4.05,
        "trend": "down",
        "last_updated": str(datetime.now().date()),
        "signal": "短端利率跟随降息预期",
    },
    "yield_curve": {
        "value": 30,
        "prev_value": 30,
        "trend": "up",
        "last_updated": str(datetime.now().date()),
        "signal": "收益率曲线正常化",
    },
    "ted_spread": {
        "value": 15,
        "prev_value": 20,
        "trend": "down",
        "last_updated": str(datetime.now().date()),
        "signal": "信用市场稳定",
    },
    "dxy": {
        "value": 103.5,
        "prev_value": 104.8,
        "trend": "down",
        "last_updated": str(datetime.now().date()),
        "signal": "美元温和走弱",
    },
}


def fetch_mock_data() -> Dict[str, Dict]:
    """返回模拟宏观指标数据"""
    return MOCK_INDICATORS.copy()


def fetch_data(source: str = "mock") -> Dict[str, Dict]:
    """
    统一数据获取入口。

    source:
        - "mock": 使用内置模拟数据
        - "fred": 从 FRED API 获取 (需 FRED_API_KEY 环境变量)
        - "custom": 从本地 JSON 文件加载
    """
    if source == "mock":
        return fetch_mock_data()

    elif source == "custom":
        data_path = os.environ.get("MACRO_DATA_PATH", "data/custom_indicators.json")
        if os.path.exists(data_path):
            with open(data_path, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            print(f"警告: 未找到自定义数据文件 {data_path}，回退到模拟数据")
            return fetch_mock_data()

    elif source == "fred":
        return _fetch_from_fred()

    else:
        print(f"警告: 未知数据源 '{source}'，回退到模拟数据")
        return fetch_mock_data()


def _fetch_from_fred() -> Dict[str, Dict]:
    """从 FRED API 获取真实数据 (需网络和 API Key)"""
    try:
        import requests
    except ImportError:
        print("警告: requests 库未安装，回退到模拟数据")
        return fetch_mock_data()

    api_key = os.environ.get("FRED_API_KEY", "")
    if not api_key:
        print("警告: FRED_API_KEY 未设置，回退到模拟数据")
        return fetch_mock_data()

    fred_series = {
        "gdp_yoy": "GDPC1",
        "cpi_yoy": "CPIAUCSL",
        "core_pce_yoy": "PCEPILFE",
        "fed_funds_rate": "FEDFUNDS",
        "us10y_yield": "DGS10",
        "us2y_yield": "DGS2",
        "ted_spread": "TEDRATE",
        "dxy": "DTWEXBGS",
        "industrial_production_yoy": "INDPRO",
        "nonfarm_payrolls": "PAYEMS",
    }

    result = MOCK_INDICATORS.copy()
    base_url = "https://api.stlouisfed.org/fred/series/observations"

    for indicator_key, series_id in fred_series.items():
        try:
            params = {
                "series_id": series_id,
                "api_key": api_key,
                "file_type": "json",
                "sort_order": "desc",
                "limit": 2,
            }
            resp = requests.get(base_url, params=params, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                obs = data.get("observations", [])
                if len(obs) >= 1:
                    val = float(obs[0]["value"])
                    prev = float(obs[1]["value"]) if len(obs) >= 2 else val
                    result[indicator_key] = {
                        "value": val,
                        "prev_value": prev,
                        "trend": "up" if val > prev else "down",
                        "last_updated": obs[0]["date"],
                        "signal": "",
                    }
        except Exception:
            continue

    return result
