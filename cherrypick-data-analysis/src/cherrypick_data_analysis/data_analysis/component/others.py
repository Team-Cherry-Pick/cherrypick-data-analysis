from datetime import date

import streamlit as st
from streamlit_option_menu import option_menu
from cherrypick_data_analysis.shared.util.redis_util import cache_init, get_cache
from cherrypick_data_analysis.shared.enum.cachekey import CacheKey
from cherrypick_data_analysis.shared.enum.site import Site
from streamlit_option_menu import option_menu

def main_title(title:str, caption:str) :
    col1, col2 = st.columns([8, 1])
    with col1:
        st.title(title)
        st.caption(caption)
    with col2:
        if st.button("🔄 캐시 초기화"):
            cache_init()
    with st.expander("### Guidelines") :
        st.write("헤헤헤")

def data_status_card() :
    deal_count_dict = get_cache(CacheKey.SITE_DEAL_COUNT)
    comment_count_dict = get_cache(CacheKey.SITE_COMMENT_COUNT)

    st.markdown("### 🗂️ 보유 데이터 현황")
    col1, col2, col3 = st.columns([3, 3, 4])
    with col1:
        st.markdown("#### 🟣 FMKOREA")
        st.metric("딜 수", f"{deal_count_dict.get(Site.FMKOREA, 0):,} 건")
        st.metric("댓글 수", f"{comment_count_dict.get(Site.FMKOREA, 0):,} 건")

    with col2:
        st.markdown("#### 🔵 PPOMPPU")
        st.metric("딜 수", f"{deal_count_dict.get(Site.PPOMPPU, 0):,} 건")
        st.metric("댓글 수", f"{comment_count_dict.get(Site.PPOMPPU, 0):,} 건")

def sidebar_filter() :
    with st.sidebar:
        st.markdown("### 🎛️ 필터")

        start_date = st.date_input("시작 날짜", value=date(2018, 1, 1))
        end_date = st.date_input("종료 날짜", value=date.today())

        selected_sites = st.multiselect(
            "사이트 선택",
            options=["FMKOREA", "PPOMPPU"],
            default=["FMKOREA", "PPOMPPU"]
        )

        if start_date > end_date:
            st.error("⚠️ 시작 날짜는 종료 날짜보다 앞서야 합니다.")

    return start_date, end_date, selected_sites

def sidebar_page_selector() :
    # 1. as sidebar menu
    with st.sidebar:
      selected = option_menu(
        "datalab",
        ["Dashboard", "Statistics", "Admin"] ,
        icons=["compass-fill", "bar-chart-line-fill", "file-person-fill"],
        default_index=0
      )
    return selected
