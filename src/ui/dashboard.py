"""
全景仪表盘 — 页面编排
======================
伦敦暗色艺术风格 · 极简布局
四大板块：全景 / 周期图 / 红绿灯 / 数据表
"""
import streamlit as st
from typing import Dict
from .charts import radar_chart, merrill_lynch_quadrant, cycle_probability_bars, dollar_tide_gauge
from .components import cycle_badge, asset_traffic_lights, data_table, dollar_phase_badge

GOLD = "#c8a45c"
TEXT = "#e8e4d9"
TEXT_DIM = "#8a8578"
GREEN_SAGE = "#7d9a5e"
RED_MUTED = "#b55a4e"
AMBER = "#c4954a"


def render_dashboard(analysis: Dict) -> None:
    ml = analysis["merrill_lynch"]
    dt = analysis["dollar_tide"]
    probs = analysis["cycle_probabilities"]
    dominant = analysis["dominant_cycle"]
    phase = analysis["dollar_phase"]

    st.title("Macro Cycle · Dashboard")
    st.caption("Merrill Lynch Clock & Dollar Tide · Real-time Quantitative Assessment")

    tab1, tab2, tab3, tab4 = st.tabs([
        "Overview",
        "Cycle Map",
        "Allocations",
        "Data",
    ])

    # ── Tab 1: Overview ──
    with tab1:
        left, right = st.columns([0.34, 0.66])

        with left:
            cycle_badge(dominant)
            dollar_phase_badge(phase)

            st.markdown("---")
            st.markdown(f"<div style='font-size:0.7rem;letter-spacing:0.16em;color:{TEXT_DIM};text-transform:uppercase;margin-bottom:10px;'>Key Scores</div>", unsafe_allow_html=True)
            m1, m2 = st.columns(2)
            m1.metric("经济增长", f"{ml['growth_score']}")
            m2.metric("通胀压力", f"{ml['inflation_score']}")
            m3, m4 = st.columns(2)
            m3.metric("美联储", f"{dt['fed_policy_score']}")
            m4.metric("风险偏好", f"{100 - dt['global_risk_score']}")

        with right:
            st.markdown(f"<div style='font-size:0.7rem;letter-spacing:0.16em;color:{TEXT_DIM};text-transform:uppercase;margin-bottom:6px;'>Dimension Radar</div>", unsafe_allow_html=True)
            st.plotly_chart(radar_chart(analysis), width="stretch", config={"displayModeBar": False})

    # ── Tab 2: Cycle Map ──
    with tab2:
        st.markdown(f"<div style='font-size:0.7rem;letter-spacing:0.16em;color:{TEXT_DIM};text-transform:uppercase;margin-bottom:10px;'>Merrill Lynch Clock — Current Position</div>", unsafe_allow_html=True)

        ql, qr = st.columns([0.55, 0.45])
        with ql:
            st.plotly_chart(merrill_lynch_quadrant(ml["growth_score"], ml["inflation_score"], probs),
                            width="stretch", config={"displayModeBar": False})
        with qr:
            st.markdown(f"<div style='font-size:0.7rem;letter-spacing:0.12em;color:{TEXT_DIM};margin-bottom:6px;'>PROBABILITY</div>", unsafe_allow_html=True)
            st.plotly_chart(cycle_probability_bars(probs), width="stretch", config={"displayModeBar": False})

        st.markdown("---")
        st.markdown(f"<div style='font-size:0.7rem;letter-spacing:0.16em;color:{TEXT_DIM};text-transform:uppercase;margin-bottom:10px;'>Dollar Tide · Gauge</div>", unsafe_allow_html=True)
        st.plotly_chart(dollar_tide_gauge(dt["fed_policy_score"], dt["us_strength_score"], dt["global_risk_score"]),
                        width="stretch", config={"displayModeBar": False})

    # ── Tab 3: Allocations ──
    with tab3:
        st.markdown(f"<div style='font-size:0.7rem;letter-spacing:0.16em;color:{TEXT_DIM};text-transform:uppercase;margin-bottom:10px;'>Asset Allocation · Traffic Light</div>", unsafe_allow_html=True)

        asset_signals = dominant.get("asset_signals", {})
        asset_traffic_lights(asset_signals)

        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        c1.markdown(
            f"""<div style="padding:12px 10px;text-align:center;background:{GREEN_SAGE}0a;border:1px solid {GREEN_SAGE}22;border-radius:3px;">
            <span style="font-size:1.2rem;color:{GREEN_SAGE};">▲ LONG</span><br>
            <span style="font-size:0.7rem;color:{TEXT_DIM};">周期有利 · 建议超配</span></div>""",
            unsafe_allow_html=True,
        )
        c2.markdown(
            f"""<div style="padding:12px 10px;text-align:center;background:{AMBER}0a;border:1px solid {AMBER}22;border-radius:3px;">
            <span style="font-size:1.2rem;color:{AMBER};">■ NEUTRAL</span><br>
            <span style="font-size:0.7rem;color:{TEXT_DIM};">标准配置 · 观望为主</span></div>""",
            unsafe_allow_html=True,
        )
        c3.markdown(
            f"""<div style="padding:12px 10px;text-align:center;background:{RED_MUTED}0a;border:1px solid {RED_MUTED}22;border-radius:3px;">
            <span style="font-size:1.2rem;color:{RED_MUTED};">▼ SHORT</span><br>
            <span style="font-size:0.7rem;color:{TEXT_DIM};">周期不利 · 建议低配</span></div>""",
            unsafe_allow_html=True,
        )

        st.markdown("---")
        st.markdown(f"<div style='color:{TEXT_DIM};font-size:0.85rem;font-style:italic;'>{dominant.get('description', '')}</div>", unsafe_allow_html=True)

    # ── Tab 4: Data ──
    with tab4:
        st.markdown(f"<div style='font-size:0.7rem;letter-spacing:0.16em;color:{TEXT_DIM};text-transform:uppercase;margin-bottom:10px;'>Indicator Data</div>", unsafe_allow_html=True)
        data_table(analysis)
