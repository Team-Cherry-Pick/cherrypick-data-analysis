from datetime import date

import streamlit as st
from cherrypick_data_analysis.data_analysis.analysis.eda_analysis import *
from cherrypick_data_analysis.shared.util.redis_util import *
from cherrypick_data_analysis.shared.database.query.deal_query import get_all_deals_dataframe, get_deal_count
from cherrypick_data_analysis.shared.database.query.comment_query import get_all_comment_dataframe, get_comment_count

st.set_page_config(layout="wide")
def caching() :
    deals = get_all_deals_dataframe()
    deal_count = get_deal_count()
    comment_count = get_comment_count()
    set_cache(CacheKey.DEAL_ALL, deals)
    set_cache(CacheKey.SITE_DEAL_COUNT, deal_count)
    set_cache(CacheKey.SITE_COMMENT_COUNT, comment_count)



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


col1, col2 = st.columns([8, 1])
with col1:
    st.title("🍒 CHERRYPICK DATALAB")
    st.caption("데이터로 결정하는 팀 체리픽의 인사이트 허브")
with col2:
    if st.button("🔄 캐시 초기화"):
        caching()


deal_count_dict = get_cache(CacheKey.SITE_DEAL_COUNT)
comment_count_dict = get_cache(CacheKey.SITE_COMMENT_COUNT)

st.markdown("### ✨ 보유 데이터 일람")

col1, col2, col3 = st.columns([3,3,4])
with col1:
    st.markdown("#### 🟣 FMKOREA")
    st.metric("딜 수", f"{deal_count_dict.get(Site.FMKOREA, 0):,}")
    st.metric("댓글 수", f"{comment_count_dict.get(Site.FMKOREA, 0):,}")

with col2:
    st.markdown("#### 🔵 PPOMPPU")
    st.metric("딜 수", f"{deal_count_dict.get(Site.PPOMPPU, 0):,}")
    st.metric("댓글 수", f"{comment_count_dict.get(Site.PPOMPPU, 0):,}")


monthly = get_monthly_deal_post_trend(selected_sites, start_date, end_date)
st.markdown("### 🗓️ 딜 콘텐츠 월간 발생량 추이")
st.line_chart(monthly)

monthly_view = get_monthly_deal_view_trend(selected_sites, start_date, end_date)
st.markdown("### 🗓️ 월별 총 딜 조회수 수 추이")
st.line_chart(monthly_view)

size = get_marcket_value_over_time()
st.markdown("### 💹 월별 시장 규모 추이")
st.line_chart(size)

category = get_post_count_by_category()
st.markdown("### 📊 카테고리별 딜 수")
st.bar_chart(category)


