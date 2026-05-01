"""
UI 组件模块
===========
资产红绿灯、数据清单表格、周期标签等可复用组件。
"""
import streamlit as st
import pandas as pd
from typing import Dict
from config import (
    CYCLE_DEFINITIONS,
    DOLLAR_PHASES,
    ASSET_CLASSES,
)


def cycle_badge(dominant_cycle: Dict) -> None:
    """主周期判定徽章"""
    color = dominant_cycle.get("color", "#95A5A6")
    prob = dominant_cycle.get("probability", 50)
    name = dominant_cycle.get("name", "未知")

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, {color}22, {color}44);
            border: 2px solid {color};
            border-radius: 16px;
            padding: 24px 20px;
            text-align: center;
            margin: 10px 0;
        ">
            <div style="font-size: 14px; color: #7F8C8D; margin-bottom: 4px;">
                当前经济周期研判
            </div>
            <div style="font-size: 36px; font-weight: 800; color: {color}; letter-spacing: 2px;">
                {name}
            </div>
            <div style="font-size: 16px; color: {color}; margin-top: 6px;">
                置信度 {prob}%
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def asset_traffic_lights(asset_signals: Dict[str, str]) -> None:
    """资产配置红绿灯"""
    signal_map = {
        "green": ("🟢 利好", "#27AE60"),
        "red": ("🔴 利空", "#E74C3C"),
        "yellow": ("🟡 中性", "#F39C12"),
    }

    cols = st.columns(len(asset_signals))
    for i, (asset_key, signal) in enumerate(asset_signals.items()):
        label, color = signal_map.get(signal, ("⚪ 未知", "#95A5A6"))
        asset_name = ASSET_CLASSES.get(asset_key, asset_key)
        with cols[i]:
            st.markdown(
                f"""
                <div style="
                    background: {color}15;
                    border: 1.5px solid {color}55;
                    border-radius: 12px;
                    padding: 14px 8px;
                    text-align: center;
                ">
                    <div style="font-size: 13px; color: #7F8C8D; margin-bottom: 6px;">
                        {asset_name}
                    </div>
                    <div style="font-size: 18px; font-weight: 700; color: {color};">
                        {label}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def data_table(analysis: Dict) -> None:
    """底层数据清单 — 关键指标数值及预警信号"""
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
        value = info.get("value", "-")
        prev = info.get("prev_value", "-")
        trend_icon = "🔺" if info.get("trend") == "up" else ("🔻" if info.get("trend") == "down" else "➖")
        score = all_scores.get(key, "-")
        signal = info.get("signal", "")

        if score != "-" and isinstance(score, (int, float)):
            if score > 70:
                alert = "🔴"
            elif score < 30:
                alert = "🟢"
            else:
                alert = "🟡"
        else:
            alert = "➖"

        rows.append({
            "预警": alert,
            "指标": key,
            "当前值": f"{value}",
            "前值": f"{prev}",
            "趋势": trend_icon,
            "标准得分": f"{score}" if score != "-" else "-",
            "信号解读": signal,
        })

    df = pd.DataFrame(rows)
    st.dataframe(
        df,
        width="stretch",
        hide_index=True,
        column_config={
            "预警": st.column_config.TextColumn(width="small"),
            "指标": st.column_config.TextColumn(width="medium"),
            "当前值": st.column_config.TextColumn(width="small"),
            "前值": st.column_config.TextColumn(width="small"),
            "趋势": st.column_config.TextColumn(width="small"),
            "标准得分": st.column_config.TextColumn(width="small"),
            "信号解读": st.column_config.TextColumn(width="large"),
        },
    )


def dollar_phase_badge(phase: Dict) -> None:
    """美元周期阶段徽章"""
    color = phase.get("color", "#95A5A6")
    name = phase.get("name", "未知")
    emoji = {
        "tightening": "🦅",
        "easing": "🕊️",
        "plateau": "⏸️",
    }.get(phase.get("key", ""), "❓")
    signal_map = {
        "red": ("新兴市场承压", "#E74C3C"),
        "green": ("新兴市场利好", "#27AE60"),
        "yellow": ("新兴市场中性", "#F39C12"),
    }
    em_signal = phase.get("em_signal", "yellow")
    em_label, em_color = signal_map.get(em_signal, ("", "#95A5A6"))

    st.markdown(
        f"""
        <div style="
            background: {color}15;
            border: 1.5px solid {color}55;
            border-radius: 12px;
            padding: 16px;
            text-align: center;
            margin: 8px 0;
        ">
            <div style="font-size: 28px; margin-bottom: 4px;">{emoji}</div>
            <div style="font-size: 18px; font-weight: 700; color: {color};">
                美元{name}
            </div>
            <div style="font-size: 13px; color: {em_color}; margin-top: 4px;">
                {em_label}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
