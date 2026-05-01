"""
宏观经济周期研判看板 — 主入口
=============================
基于美林时钟 + 美元潮汐双模型的量化周期研判工具。
"""
import os, sys

try:
    _home = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".streamlit")
    os.environ.setdefault("STREAMLIT_HOME", _home)
    os.makedirs(_home, exist_ok=True)
except (OSError, PermissionError):
    pass

import streamlit as st

st.set_page_config(
    page_title="宏观周期 · 研判看板",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from src.data.fetcher import fetch_data
from src.models.engine import run_full_analysis
from src.ui.dashboard import render_dashboard

GOLD = "#c8a45c"
DARK_BG = "#111111"
CARD_BG = "#1a1a1a"
TEXT = "#e8e4d9"
TEXT_DIM = "#8a8578"
BORDER = "#2a2a2a"

CSS = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');

    * {{ font-family: 'Inter', sans-serif; }}

    .stApp {{
        background: {DARK_BG};
    }}

    .main .block-container {{
        padding: 1.5rem 3rem 3rem 3rem;
        max-width: 1400px;
    }}

    h1 {{
        font-family: 'Playfair Display', serif !important;
        font-weight: 600 !important;
        font-size: 2.2rem !important;
        color: {GOLD} !important;
        letter-spacing: 0.03em;
        margin-bottom: 0.2rem;
    }}

    h2, h3, h4 {{
        font-family: 'Inter', sans-serif !important;
        font-weight: 400 !important;
        color: {TEXT} !important;
        letter-spacing: 0.02em;
    }}

    p, div, label, span, small, caption {{
        color: {TEXT_DIM} !important;
    }}

    .stCaption {{
        font-style: italic;
        letter-spacing: 0.04em;
        opacity: 0.6;
    }}

    section[data-testid="stSidebar"] {{
        background: {CARD_BG};
        border-right: 1px solid {BORDER};
    }}

    section[data-testid="stSidebar"] h2 {{
        color: {GOLD} !important;
        font-size: 1.1rem !important;
        letter-spacing: 0.06em;
    }}

    .stTabs [data-baseweb="tab-list"] {{
        gap: 2px;
        background: transparent;
        border-bottom: 1px solid {BORDER};
    }}

    .stTabs [data-baseweb="tab"] {{
        padding: 10px 24px;
        border-radius: 4px 4px 0 0;
        color: {TEXT_DIM} !important;
        font-size: 0.9rem;
        letter-spacing: 0.04em;
        font-weight: 400;
        background: transparent;
        border: none;
        transition: all 0.3s ease;
    }}

    .stTabs [data-baseweb="tab"]:hover {{
        color: {GOLD} !important;
    }}

    .stTabs [aria-selected="true"] {{
        color: {GOLD} !important;
        border-bottom: 2px solid {GOLD} !important;
        background: transparent !important;
    }}

    div[data-testid="stMetricValue"] {{
        font-family: 'Playfair Display', serif !important;
        font-size: 2rem !important;
        color: {TEXT} !important;
    }}

    div[data-testid="stMetricLabel"] {{
        font-size: 0.75rem !important;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }}

    .stDataFrame {{
        background: {CARD_BG} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 6px;
    }}

    .stDataFrame th {{
        background: {DARK_BG} !important;
        color: {GOLD} !important;
        font-weight: 500 !important;
        letter-spacing: 0.04em;
        font-size: 0.8rem !important;
    }}

    .stDataFrame td {{
        color: {TEXT_DIM} !important;
        font-size: 0.85rem !important;
    }}

    div[data-testid="stSpinner"] {{
        color: {GOLD} !important;
    }}

    hr {{
        border-color: {BORDER} !important;
        margin: 1.5rem 0;
    }}

    .stAlert {{
        background: {CARD_BG} !important;
        border: 1px solid {BORDER} !important;
        color: {TEXT_DIM} !important;
    }}

    footer {{ visibility: hidden; }}
</style>
"""


def main():
    st.markdown(CSS, unsafe_allow_html=True)

    with st.spinner("正在抓取宏观数据 & 运行研判模型..."):
        indicators = fetch_data(source="mock")
        analysis = run_full_analysis(indicators)

    render_dashboard(analysis)

    with st.sidebar:
        st.markdown("## ⚙ 设置")
        data_source = st.selectbox(
            "数据源",
            options=["mock", "custom", "fred"],
            index=0,
            help="mock=模拟数据 | custom=本地JSON | fred=FRED API",
        )
        st.caption(f"当前数据源: {data_source}")

        st.markdown("---")
        st.markdown("### 模型说明")
        st.markdown(
            f"""
            <span style="color:{GOLD};">美林时钟</span>  
            经济增长 & 通胀因子  
            复苏 → 繁荣 → 滞胀 → 衰退  

            <span style="color:{GOLD};">美元潮汐</span>  
            货币政策 & 经济强度  
            全球风险偏好与利差
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")
        st.caption("本工具仅供研究参考，不构成投资建议。")
        st.caption("v 1.1 · London Edit")


if __name__ == "__main__":
    main()
