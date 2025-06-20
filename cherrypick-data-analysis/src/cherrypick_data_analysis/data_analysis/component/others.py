from datetime import date, timedelta
from email.policy import default

import streamlit as st
from streamlit_option_menu import option_menu
from cherrypick_data_analysis.shared.util.redis_util import cache_init, get_cache
from cherrypick_data_analysis.shared.enum.cachekey import CacheKey
from cherrypick_data_analysis.shared.enum.site import Site
from streamlit_option_menu import option_menu

# 'authorization'의 'auth' 딕셔너리 가져오기
auth = st.secrets["authorization"]["auth"]

def main_title(title:str, caption:str) :
    col1, col2 = st.columns([8, 1])
    with col1:
        st.title(title)
        st.caption(caption)
    with col2:
        if st.button("🔄 캐시 초기화"):
            cache_init()
    with st.expander("### Guidelines") :
        st.caption(f"""
Dashboard  : 데이터 현황 확인 &nbsp;&nbsp;&nbsp;
Statistics : 상세 통계 확인 &nbsp;&nbsp;&nbsp;
Admin      : 관리자 전용 유틸리티 &nbsp;&nbsp;&nbsp;
데이터는 뽐뿌 / 에펨코리아에서 크롤링해왔으며 추후 자사 데이터도 추가할 예정.
""")

def data_inventory_status_card(site:Site) :
    deal_count_dict = get_cache(CacheKey.SITE_DEAL_COUNT)
    comment_count_dict = get_cache(CacheKey.SITE_COMMENT_COUNT)
    container = st.container(border=True)
    with container:
        st.markdown(f"#### 🟣 {site.name}")
        st.metric("DEAL", f"{deal_count_dict.get(site, 0):,} 건")
        st.metric("COMMENT", f"{comment_count_dict.get(site, 0):,} 건")

def sidebar_login() :

    with st.sidebar :
        # 'key'가 없으면 None으로 초기화
        if "key" not in st.session_state:
            st.session_state["key"] = None

        with st.sidebar:
            if st.session_state["key"] is None:
                key = st.text_input("login", placeholder="Enter your key",  label_visibility="hidden")
                if st.button("login"):
                    if key:  # 로그인할 때 key 값이 비어있지 않으면
                        if key not in auth.values() :
                            if key in list(auth):
                                key = auth[key]
                            st.session_state["key"] = key
                            st.toast("로그인 성공 !")

                        else : st.toast("다른 key로 로그인해주세요 !")
                    else : st.toast("key를 입력해주세요 !")
            else:
                st.write(f"hello ! {st.session_state['key']}")

def sidebar_filter() :
    with st.sidebar:
        toggle = st.toggle("selector", value=True)
        st.title("🎛️ 필터")

        today = date.today()
        if toggle :
            start_date , end_date = st.slider("date range", value = (today.replace(today.year-3, 1, 1), today), step=timedelta(days=1), format="y.M.D")

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
