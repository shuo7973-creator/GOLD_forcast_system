"""
可视化图表模块
===============
雷达图、美林时钟象限图、美元潮汐仪表、概率柱状图
"""
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List
from config import CYCLE_DEFINITIONS


def radar_chart(analysis: Dict) -> go.Figure:
    """
    经济维度雷达图 — 展示五大核心维度得分。
    维度: 经济增长 / 通胀压力 / 货币政策 / 美国强度 / 全球风险
    """
    ml = analysis["merrill_lynch"]
    dt = analysis["dollar_tide"]

    categories = ["经济增长", "通胀压力", "货币政策(紧→松)", "美国经济强度", "全球风险偏好"]
    scores_reversed = [
        ml["growth_score"],
        ml["inflation_score"],
        100 - dt["fed_policy_score"],
        dt["us_strength_score"],
        100 - dt["global_risk_score"],
    ]

    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=scores_reversed + [scores_reversed[0]],
            theta=categories + [categories[0]],
            fill="toself",
            name="当前周期",
            line_color="#3498DB",
            fillcolor="rgba(52,152,219,0.3)",
            line=dict(width=2),
        )
    )
    fig.add_trace(
        go.Scatterpolar(
            r=[50, 50, 50, 50, 50, 50],
            theta=categories + [categories[0]],
            fill="toself",
            name="中性基准线",
            line_color="#BDC3C7",
            fillcolor="rgba(189,195,199,0.1)",
            line=dict(dash="dash"),
        )
    )
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=10)),
            angularaxis=dict(tickfont=dict(size=11)),
            bgcolor="rgba(0,0,0,0.02)",
        ),
        showlegend=True,
        legend=dict(x=0.85, y=1.1, orientation="h"),
        margin=dict(l=40, r=40, t=30, b=30),
        height=400,
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def merrill_lynch_quadrant(growth: float, inflation: float, probs: Dict[str, float]) -> go.Figure:
    """
    美林时钟四象限散点图 — 展示当前周期位置。
    """
    quadrant_colors = {
        "recovery": "rgba(39,174,96,0.15)",
        "overheat": "rgba(231,76,60,0.15)",
        "stagflation": "rgba(142,68,173,0.15)",
        "recession": "rgba(44,62,80,0.15)",
    }
    quadrant_labels = {
        "recovery": "复苏期<br>Growth ↑ Inflation ↓",
        "overheat": "繁荣期<br>Growth ↑ Inflation ↑",
        "stagflation": "滞胀期<br>Growth ↓ Inflation ↑",
        "recession": "衰退期<br>Growth ↓ Inflation ↓",
    }

    fig = go.Figure()

    for phase, (g_range, i_range) in [
        ("recovery", ((55, 100), (0, 45))),
        ("overheat", ((55, 100), (55, 100))),
        ("stagflation", ((0, 45), (55, 100))),
        ("recession", ((0, 45), (0, 45))),
    ]:
        fig.add_shape(
            type="rect",
            x0=g_range[0],
            y0=i_range[0],
            x1=g_range[1],
            y1=i_range[1],
            fillcolor=quadrant_colors[phase],
            line=dict(color=CYCLE_DEFINITIONS[phase]["color"], width=1.5),
            layer="below",
        )
        fig.add_annotation(
            x=(g_range[0] + g_range[1]) / 2,
            y=(i_range[0] + i_range[1]) / 2,
            text=quadrant_labels[phase],
            showarrow=False,
            font=dict(size=11, color=CYCLE_DEFINITIONS[phase]["color"]),
            opacity=0.7,
        )

    fig.add_trace(
        go.Scatter(
            x=[growth],
            y=[inflation],
            mode="markers+text",
            marker=dict(
                size=22,
                color="#F39C12",
                line=dict(color="#E67E22", width=2),
                symbol="circle",
            ),
            text=[" 当前位置"],
            textposition="top center",
            textfont=dict(size=12, color="#F39C12", family="Arial Bold"),
            name="当前周期位置",
        )
    )

    fig.add_hline(y=50, line_dash="dash", line_color="gray", opacity=0.5)
    fig.add_vline(x=50, line_dash="dash", line_color="gray", opacity=0.5)

    fig.update_layout(
        xaxis=dict(title="经济增长因子 (0→弱 → 强→100)", range=[-5, 105], tickmode="linear", tick0=0, dtick=20),
        yaxis=dict(title="通货膨胀因子 (0→低 → 高→100)", range=[-5, 105], tickmode="linear", tick0=0, dtick=20),
        height=450,
        margin=dict(l=50, r=30, t=30, b=50),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0.02)",
    )
    return fig


def cycle_probability_bars(probs: Dict[str, float]) -> go.Figure:
    """周期概率柱状图"""
    labels_map = {
        "recovery": "复苏期",
        "overheat": "繁荣期/过热",
        "stagflation": "滞胀期",
        "recession": "衰退期",
    }
    colors_map = {
        "recovery": "#27AE60",
        "overheat": "#E74C3C",
        "stagflation": "#8E44AD",
        "recession": "#2C3E50",
    }

    phases = list(probs.keys())
    labels = [labels_map.get(p, p) for p in phases]
    values = [probs[p] for p in phases]
    colors = [colors_map.get(p, "#95A5A6") for p in phases]

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=labels,
            y=values,
            marker_color=colors,
            text=[f"{v}%" for v in values],
            textposition="outside",
            textfont=dict(size=14, family="Arial Bold"),
            marker=dict(
                line=dict(width=1, color="rgba(0,0,0,0.2)"),
                cornerradius=6,
            ),
        )
    )
    fig.update_layout(
        yaxis=dict(title="匹配概率 (%)", range=[0, 100], tickmode="linear", dtick=20),
        xaxis=dict(title=""),
        height=320,
        margin=dict(l=30, r=30, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0.02)",
        bargap=0.35,
    )
    return fig


def dollar_tide_gauge(fed_score: float, us_score: float, risk_score: float) -> go.Figure:
    """
    美元潮汐仪表 — 三列指标卡风格的仪表。
    """
    indicators = [
        {"label": "美联储政策", "score": fed_score, "interpretation": "鹰派 ↔ 鸽派"},
        {"label": "美国经济强度", "score": us_score, "interpretation": "弱 ↔ 强"},
        {"label": "全球风险偏好", "score": risk_score, "interpretation": "Risk On ↔ Risk Off"},
    ]

    fig = go.Figure()
    for i, ind in enumerate(indicators):
        color = (
            "#E74C3C" if ind["score"] > 60
            else "#27AE60" if ind["score"] < 40
            else "#F39C12"
        )
        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=ind["score"],
                title={"text": ind["label"], "font": {"size": 13}},
                number={"font": {"size": 28, "color": color}, "suffix": ""},
                gauge={
                    "axis": {"range": [0, 100], "tickwidth": 1},
                    "bar": {"color": color},
                    "steps": [
                        {"range": [0, 40], "color": "rgba(39,174,96,0.15)"},
                        {"range": [40, 60], "color": "rgba(243,156,18,0.15)"},
                        {"range": [60, 100], "color": "rgba(231,76,60,0.15)"},
                    ],
                    "threshold": {
                        "line": {"color": "black", "width": 2},
                        "thickness": 0.8,
                        "value": 50,
                    },
                },
                domain={"row": 0, "column": i},
            )
        )
    fig.update_layout(
        grid={"rows": 1, "columns": 3, "pattern": "independent"},
        height=250,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig
