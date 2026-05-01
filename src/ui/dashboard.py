"""
全景仪表盘 — 页面编排
======================
组合所有 UI 模块，形成四大板块：
1. 全景仪表盘 (核心结论 + 雷达图)
2. 动态周期图 (美林时钟 + 美元潮汐)
3. 资产红绿灯 (大类资产配置)
4. 底层数据清单 (指标数值表)
"""
import streamlit as st
from typing import Dict
from .charts import (
    radar_chart,
    merrill_lynch_quadrant,
    cycle_probability_bars,
    dollar_tide_gauge,
)
from .components import (
    cycle_badge,
    asset_traffic_lights,
    data_table,
    dollar_phase_badge,
)


def render_dashboard(analysis: Dict) -> None:
    """渲染完整仪表盘"""
    ml = analysis["merrill_lynch"]
    dt = analysis["dollar_tide"]
    probs = analysis["cycle_probabilities"]
    dominant = analysis["dominant_cycle"]
    phase = analysis["dollar_phase"]

    st.title("📊 宏观经济周期研判看板")
    st.caption(f"基于美林时钟 & 美元潮汐双模型 · 实时量化研判")

    # ========== Tab 1: 全景仪表盘 ==========
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎯 全景仪表盘",
        "🔄 动态周期图",
        "🚦 资产红绿灯",
        "📋 底层数据清单",
    ])

    with tab1:
        col_left, col_right = st.columns([0.38, 0.62])

        with col_left:
            cycle_badge(dominant)

            st.markdown("---")

            st.markdown("### 🏦 美元潮汐阶段")
            dollar_phase_badge(phase)

            st.markdown("---")

            st.markdown("### 📈 核心指标得分")
            metric_cols = st.columns(2)
            with metric_cols[0]:
                st.metric("经济增长因子", f"{ml['growth_score']}", help="0-100, 越高增长越强")
            with metric_cols[1]:
                st.metric("通胀压力因子", f"{ml['inflation_score']}", help="0-100, 越高通胀越强")
            metric_cols2 = st.columns(2)
            with metric_cols2[0]:
                st.metric("美联储政策", f"{dt['fed_policy_score']}", help="高=鹰派, 低=鸽派")
            with metric_cols2[1]:
                st.metric("全球风险偏好", f"{100 - dt['global_risk_score']}", help="高=Risk On, 低=Risk Off")

            st.caption(dominant.get("description", ""))

        with col_right:
            st.markdown("### 🎯 经济维度雷达图")
            st.plotly_chart(radar_chart(analysis), width="stretch")

    # ========== Tab 2: 动态周期图 ==========
    with tab2:
        st.markdown("### 🔄 美林时钟 — 当前周期位置")
        st.caption("横轴=经济增长因子 | 纵轴=通货膨胀因子 | 圆点=当前经济位置")

        col_quad, col_bars = st.columns([0.55, 0.45])

        with col_quad:
            fig_quad = merrill_lynch_quadrant(
                ml["growth_score"], ml["inflation_score"], probs
            )
            st.plotly_chart(fig_quad, width="stretch")

        with col_bars:
            st.markdown("#### 各周期匹配度概率")
            fig_bars = cycle_probability_bars(probs)
            st.plotly_chart(fig_bars, width="stretch")

        st.markdown("---")
        st.markdown("### 🌊 美元潮汐 — 三大维度仪表盘")
        fig_gauge = dollar_tide_gauge(
            dt["fed_policy_score"],
            dt["us_strength_score"],
            dt["global_risk_score"],
        )
        st.plotly_chart(fig_gauge, width="stretch")

    # ========== Tab 3: 资产红绿灯 ==========
    with tab3:
        st.markdown("### 🚦 大类资产配置建议")
        st.caption("基于当前经济周期的量化研判，仅供参考，不构成投资建议。")

        asset_signals = dominant.get("asset_signals", {})
        asset_traffic_lights(asset_signals)

        st.markdown("---")
        st.markdown("#### 📖 信号说明")
        signal_cols = st.columns(3)
        with signal_cols[0]:
            st.markdown(
                """
                <div style="text-align:center; padding:10px; background:#27AE6020; border-radius:8px;">
                <span style="font-size:20px;">🟢 利好</span><br>
                <small>周期有利，建议超配</small>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with signal_cols[1]:
            st.markdown(
                """
                <div style="text-align:center; padding:10px; background:#F39C1220; border-radius:8px;">
                <span style="font-size:20px;">🟡 中性</span><br>
                <small>标准配置，观望为主</small>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with signal_cols[2]:
            st.markdown(
                """
                <div style="text-align:center; padding:10px; background:#E74C3C20; border-radius:8px;">
                <span style="font-size:20px;">🔴 利空</span><br>
                <small>周期不利，建议低配</small>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(f"#### 📝 当前研判逻辑")
        st.info(dominant.get("description", "—"))

    # ========== Tab 4: 底层数据清单 ==========
    with tab4:
        st.markdown("### 📋 关键指标数据清单")
        st.caption("预警: 🔴=偏高(>70分)  🟡=中性  🟢=偏低(<30分)")
        data_table(analysis)
