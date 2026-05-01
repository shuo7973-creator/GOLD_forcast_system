"""
UI 组件模块
===========
周期徽章 / 资产红绿灯 / 数据清单 / 美元阶段
伦敦艺术风格 · 深色主题
"""
import streamlit as st
import pandas as pd
from typing import Dict
from config import CYCLE_DEFINITIONS, DOLLAR_PHASES, ASSET_CLASSES

GOLD = "#c8a45c"
CARD_BG = "#1a1a1a"
DARK_BG = "#111111"
TEXT = "#e8e4d9"
TEXT_DIM = "#8a8578"
BORDER = "#2a2a2a"
GREEN = "#7d9a5e"
RED = "#b55a4e"
AMBER = "#c4954a"


def _card(inner: str, accent: str = BORDER) -> str:
    return f"""
    <div style="
        background: {CARD_BG};
        border: 1px solid {accent};
        border-radius: 3px;
        padding: 20px 24px;
        margin: 12px 0;
    ">{inner}</div>"""


def cycle_badge(dominant: Dict) -> None:
    color = dominant.get("color", TEXT_DIM)
    prob = dominant.get("probability", 50)
    name = dominant.get("name", "—")
    key = dominant.get("key", "")

    key_label = {"recovery": "RECOVERY", "overheat": "OVERHEAT",
                 "stagflation": "STAGFLATION", "recession": "RECESSION"}.get(key, "")

    st.markdown(
        f"""
        <div style="
            background: {CARD_BG};
            border-left: 3px solid {color};
            border-radius: 2px;
            padding: 28px 32px;
            margin: 12px 0;
        ">
            <div style="
                font-size: 0.7rem;
                letter-spacing: 0.22em;
                color: {TEXT_DIM};
                margin-bottom: 12px;
                text-transform: uppercase;
            ">当前周期研判 · {key_label}</div>
            <div style="
                font-family: 'Playfair Display', serif;
                font-size: 3rem;
                font-weight: 600;
                color: {color};
                letter-spacing: 0.04em;
                line-height: 1.1;
            ">{name}</div>
            <div style="
                display: flex;
                align-items: baseline;
                gap: 6px;
                margin-top: 10px;
            ">
                <span style="
                    font-family: 'Playfair Display', serif;
                    font-size: 2rem;
                    color: {GOLD};
                ">{prob}%</span>
                <span style="
                    font-size: 0.8rem;
                    color: {TEXT_DIM};
                    letter-spacing: 0.08em;
                ">CONFIDENCE</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def dollar_phase_badge(phase: Dict) -> None:
    color = phase.get("color", TEXT_DIM)
    name = phase.get("name", "—")
    key = phase.get("key", "")
    composite = phase.get("composite_score", 50)
    desc = phase.get("description", "")

    emoji = {"tightening": "HAWKISH", "easing": "DOVISH", "plateau": "NEUTRAL"}.get(key, "")

    st.markdown(
        f"""
        <div style="
            background: {CARD_BG};
            border: 1px solid {BORDER};
            border-radius: 3px;
            padding: 20px 24px;
            margin: 12px 0;
        ">
            <div style="
                font-size: 0.7rem;
                letter-spacing: 0.22em;
                color: {TEXT_DIM};
                margin-bottom: 8px;
                text-transform: uppercase;
            ">美元潮汐 · {emoji}</div>
            <div style="
                font-size: 1.3rem;
                font-weight: 500;
                color: {color};
                letter-spacing: 0.04em;
            ">美元{name}</div>
            <div style="
                margin-top: 10px;
                height: 3px;
                background: {BORDER};
                border-radius: 2px;
                overflow: hidden;
            ">
                <div style="
                    width: {composite}%;
                    height: 100%;
                    background: {color};
                    border-radius: 2px;
                "></div>
            </div>
            <div style="
                font-size: 0.75rem;
                color: {TEXT_DIM};
                margin-top: 6px;
                font-style: italic;
            ">{desc}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def asset_traffic_lights(asset_signals: Dict[str, str]) -> None:
    signal_config = {
        "green": ("LONG", GREEN),
        "red": ("SHORT", RED),
        "yellow": ("NEUTRAL", AMBER),
    }

    cols = st.columns(len(asset_signals))
    for i, (asset_key, signal) in enumerate(asset_signals.items()):
        label, color = signal_config.get(signal, ("—", TEXT_DIM))
        asset_name = ASSET_CLASSES.get(asset_key, asset_key)

        _icon = {"green": "▲", "red": "▼", "yellow": "■"}.get(signal, "—")

        with cols[i]:
            st.markdown(
                f"""
                <div style="
                    background: {CARD_BG};
                    border: 1px solid {BORDER};
                    border-radius: 3px;
                    padding: 18px 12px;
                    text-align: center;
                ">
                    <div style="
                        font-size: 0.7rem;
                        letter-spacing: 0.1em;
                        color: {TEXT_DIM};
                        margin-bottom: 8px;
                        text-transform: uppercase;
                    ">{asset_name}</div>
                    <div style="
                        font-family: 'Playfair Display', serif;
                        font-size: 1.5rem;
                        font-weight: 600;
                        color: {color};
                    ">{_icon} {label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def data_table(analysis: Dict) -> None:
    indicators = analysis.get("indicators", {})
    ml = analysis.get("merrill_lynch", {})
    dt = analysis.get("dollar_tide", {})

    all_scores = {
        **ml.get("growth_detail", {}),
        **ml.get("inflation_detail", {}),
        **dt.get("fed_policy_detail", {}),
        **dt.get("us_strength_detail", {}),
        **dt.get("global_risk_detail", {}),
    }

    rows = []
    for key, info in indicators.items():
        value = info.get("value", "—")
        prev = info.get("prev_value", "—")
        trend_sym = "↑" if info.get("trend") == "up" else ("↓" if info.get("trend") == "down" else "→")
        score = all_scores.get(key, "—")
        signal = info.get("signal", "")

        if score != "—" and isinstance(score, (int, float)):
            alert = "▲" if score > 70 else ("▼" if score < 30 else "■")
        else:
            alert = "—"

        rows.append({
            "": alert,
            "指标名称": key,
            "当前": f"{value}",
            "前值": f"{prev}",
            "趋势": trend_sym,
            "得分": f"{score}" if score != "—" else "—",
            "信号": signal,
        })

    df = pd.DataFrame(rows)
    st.dataframe(
        df,
        width="stretch",
        hide_index=True,
    )
