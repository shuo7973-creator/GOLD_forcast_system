"""
可视化图表模块
===============
雷达图 / 美林象限 / 概率柱状图 / 美元仪表
色调：伦敦暗色艺术风
"""
import plotly.graph_objects as go
from typing import Dict
from config import CYCLE_DEFINITIONS

GOLD = "#c8a45c"
GREEN_SAGE = "#7d9a5e"
RED_MUTED = "#b55a4e"
PURPLE_MUTED = "#8b6b9e"
SLATE = "#4a5568"
DARK_PLOT = "#111111"
CARD_PLOT = "#1a1a1a"
TEXT_DIM = "#8a8578"
BORDER = "#2a2a2a"

PLOTLY_DARK = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=TEXT_DIM, size=12, family="Inter, sans-serif"),
    title_font=dict(color=GOLD, family="Playfair Display, serif"),
    xaxis=dict(gridcolor=BORDER, zerolinecolor=BORDER, linecolor=BORDER),
    yaxis=dict(gridcolor=BORDER, zerolinecolor=BORDER, linecolor=BORDER),
    margin=dict(l=20, r=20, t=20, b=20),
)


def radar_chart(analysis: Dict) -> go.Figure:
    ml = analysis["merrill_lynch"]
    dt = analysis["dollar_tide"]

    categories = ["经济增长", "通胀压力", "货币宽松度", "美国强度", "风险偏好"]
    scores = [
        ml["growth_score"],
        ml["inflation_score"],
        100 - dt["fed_policy_score"],
        dt["us_strength_score"],
        100 - dt["global_risk_score"],
    ]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=scores + [scores[0]],
        theta=categories + [categories[0]],
        fill="toself",
        name="当前",
        line_color=GOLD,
        fillcolor="rgba(200,164,92,0.15)",
        line=dict(width=1.5),
    ))
    fig.add_trace(go.Scatterpolar(
        r=[50, 50, 50, 50, 50, 50],
        theta=categories + [categories[0]],
        fill="toself",
        name="中性",
        line_color=TEXT_DIM,
        fillcolor="rgba(138,133,120,0.04)",
        line=dict(dash="dot", width=0.8),
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=9, color=TEXT_DIM), gridcolor=BORDER),
            angularaxis=dict(tickfont=dict(size=10, color=TEXT_DIM)),
            bgcolor="rgba(0,0,0,0)",
        ),
        showlegend=True,
        legend=dict(x=0.82, y=1.08, orientation="h", font=dict(size=10, color=TEXT_DIM)),
        paper_bgcolor="rgba(0,0,0,0)",
        height=380,
        margin=dict(l=30, r=30, t=20, b=20),
    )
    return fig


def merrill_lynch_quadrant(growth: float, inflation: float, probs: Dict[str, float]) -> go.Figure:
    quadrants = [
        ("recovery", (55, 100), (0, 45), "rgba(125,154,94,0.08)"),
        ("overheat", (55, 100), (55, 100), "rgba(181,90,78,0.08)"),
        ("stagflation", (0, 45), (55, 100), "rgba(139,107,158,0.08)"),
        ("recession", (0, 45), (0, 45), "rgba(74,85,104,0.08)"),
    ]
    labels = {
        "recovery": "复苏<br><i>Growth ↑ Infl ↓</i>",
        "overheat": "繁荣<br><i>Growth ↑ Infl ↑</i>",
        "stagflation": "滞胀<br><i>Growth ↓ Infl ↑</i>",
        "recession": "衰退<br><i>Growth ↓ Infl ↓</i>",
    }

    fig = go.Figure()
    for phase, g_r, i_r, fill in quadrants:
        fig.add_shape(type="rect", x0=g_r[0], y0=i_r[0], x1=g_r[1], y1=i_r[1],
                      fillcolor=fill, line=dict(color=CYCLE_DEFINITIONS[phase]["color"], width=1),
                      layer="below")
        fig.add_annotation(x=(g_r[0] + g_r[1]) / 2, y=(i_r[0] + i_r[1]) / 2,
                           text=labels[phase], showarrow=False,
                           font=dict(size=10, color=CYCLE_DEFINITIONS[phase]["color"]),
                           opacity=0.6)

    fig.add_trace(go.Scatter(
        x=[growth], y=[inflation], mode="markers+text",
        marker=dict(size=16, color=GOLD, line=dict(color="#fff", width=1.5)),
        text=["  Now"], textposition="middle right",
        textfont=dict(size=13, color=GOLD, family="Playfair Display"),
        name="当前",
    ))
    fig.add_hline(y=50, line_dash="dot", line_color=BORDER, opacity=0.6)
    fig.add_vline(x=50, line_dash="dot", line_color=BORDER, opacity=0.6)
    fig.update_layout(
        xaxis=dict(title="经济增长因子 →", range=[-5, 105], tickmode="linear", dtick=20, gridcolor=BORDER, zeroline=False),
        yaxis=dict(title="通货膨胀因子 →", range=[-5, 105], tickmode="linear", dtick=20, gridcolor=BORDER, zeroline=False),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        height=420, margin=dict(l=50, r=20, t=20, b=50),
        font=dict(color=TEXT_DIM, size=11),
    )
    return fig


def cycle_probability_bars(probs: Dict[str, float]) -> go.Figure:
    labels_map = {"recovery": "复苏", "overheat": "过热", "stagflation": "滞胀", "recession": "衰退"}
    colors_map = {"recovery": GREEN_SAGE, "overheat": RED_MUTED, "stagflation": PURPLE_MUTED, "recession": SLATE}
    phases = list(probs.keys())

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[probs[p] for p in phases],
        y=[labels_map.get(p, p) for p in phases],
        orientation="h",
        marker_color=[colors_map.get(p, TEXT_DIM) for p in phases],
        text=[f" {probs[p]:.0f}%" for p in phases],
        textposition="outside",
        textfont=dict(size=13, color=TEXT_DIM, family="Inter"),
        marker=dict(line=dict(width=0), cornerradius=3),
    ))
    fig.update_layout(
        xaxis=dict(range=[0, 105], showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(autorange="reversed", showgrid=False, tickfont=dict(size=13, color=TEXT_DIM)),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        height=280, margin=dict(l=10, r=30, t=10, b=10),
        bargap=0.25,
    )
    return fig


def dollar_tide_gauge(fed_score: float, us_score: float, risk_score: float) -> go.Figure:
    indicators = [
        ("美联储政策", fed_score),
        ("美国经济强度", us_score),
        ("全球风险偏好", risk_score),
    ]

    fig = go.Figure()
    for i, (label, score) in enumerate(indicators):
        c = RED_MUTED if score > 60 else (GREEN_SAGE if score < 40 else GOLD)
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=score,
            title={"text": label, "font": {"size": 12, "color": TEXT_DIM}},
            number={"font": {"size": 24, "color": c, "family": "Playfair Display"}, "suffix": ""},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 0.5, "tickcolor": BORDER},
                "bar": {"color": c, "thickness": 0.12},
                "steps": [
                    {"range": [0, 40], "color": "rgba(125,154,94,0.06)"},
                    {"range": [40, 60], "color": "rgba(200,164,92,0.06)"},
                    {"range": [60, 100], "color": "rgba(181,90,78,0.06)"},
                ],
                "threshold": {"line": {"color": TEXT_DIM, "width": 1}, "thickness": 0.6, "value": 50},
                "bgcolor": "rgba(0,0,0,0)",
            },
            domain={"row": 0, "column": i},
        ))
    fig.update_layout(
        grid={"rows": 1, "columns": 3, "pattern": "independent"},
        paper_bgcolor="rgba(0,0,0,0)",
        height=230, margin=dict(l=10, r=10, t=40, b=10),
        font=dict(color=TEXT_DIM),
    )
    return fig
