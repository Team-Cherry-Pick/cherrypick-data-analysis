from datetime import date, timedelta

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

def data_inventory_status_card(site:Site) :
    deal_count_dict = get_cache(CacheKey.SITE_DEAL_COUNT)
    comment_count_dict = get_cache(CacheKey.SITE_COMMENT_COUNT)
    container = st.container(border=True)
    with container:
        st.markdown(f"#### 🟣 {site.name}")
        st.metric("딜 수", f"{deal_count_dict.get(site, 0):,} 건")
        st.metric("댓글 수", f"{comment_count_dict.get(site, 0):,} 건")


def sidebar_filter() :
    with st.sidebar:
        toggle = st.toggle("selector", value=True)
        st.title("🎛️ 필터")

        if toggle :
            start_date , end_date = st.slider("date range", date(2018, 1, 1), date.today(), (date(2018, 1, 1), date.today()), step=timedelta(days=1), format="y.M.D")
        else :
            c1, c2 = st.columns(2)
            with c1 :
                start_date = st.date_input("시작일", value=date(2018, 1, 1))
            with c2:
                end_date = st.date_input("종료일", value=date.today())

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
