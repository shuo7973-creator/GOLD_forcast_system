"""
宏观经济周期研判看板 — 主入口
=============================
基于美林时钟 + 美元潮汐双模型的量化周期研判工具。

运行方式:
    streamlit run app.py
"""
import streamlit as st

st.set_page_config(
    page_title="宏观经济周期研判看板",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from src.data.fetcher import fetch_data
from src.models.engine import run_full_analysis
from src.ui.dashboard import render_dashboard


def main():
    st.markdown(
        """
        <style>
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 12px 20px;
            border-radius: 8px;
        }
        div[data-testid="stMetricValue"] {
            font-size: 28px;
        }
        .main .block-container {
            padding-top: 2rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.spinner("正在抓取宏观数据 & 运行研判模型..."):
        indicators = fetch_data(source="mock")
        analysis = run_full_analysis(indicators)

    render_dashboard(analysis)

    with st.sidebar:
        st.markdown("## ⚙️ 设置")
        st.markdown("---")
        data_source = st.selectbox(
            "数据源",
            options=["mock", "custom", "fred"],
            index=0,
            help="mock=模拟数据 | custom=本地JSON | fred=FRED API",
        )
        st.caption(f"当前数据源: **{data_source}**")

        st.markdown("---")
        st.markdown("### 📖 模型说明")
        st.markdown(
            """
            **美林时钟模型**
            - 经济增长因子 (GDP, PMI, CLI)
            - 通货膨胀因子 (CPI, PCE, PPI)
            - 四周期: 复苏→繁荣→滞胀→衰退

            **美元潮汐模型**
            - 美联储货币政策 (利率, 缩表)
            - 美国经济强度 (GDPNow, 非农)
            - 全球风险偏好 (利差, DXY)
            """
        )

        st.markdown("---")
        st.markdown(
            "<small>⚠️ 本工具仅供研究参考，不构成任何投资建议。</small>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<small>版本 1.0.0 · 算法内核 v2</small>",
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
