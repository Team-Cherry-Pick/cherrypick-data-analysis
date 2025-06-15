import streamlit as st
from cherrypick_data_analysis.data_analysis.analysis.eda_analysis import *
from cherrypick_data_analysis.shared.util.redis_util import *
from cherrypick_data_analysis.shared.database.query.deal_query import get_all_deals_dataframe

st.set_page_config(layout="wide")
st.title("🍒CHERRYPICK DATA ANALYSIS🍒")

if st.button("캐시 초기화") :
    set_cache(CacheKey.DEAL_ALL, get_all_deals_dataframe())


monthly = get_monthly_deal_post_trend([Site.FMKOREA.name, Site.PPOMPPU.name])
st.markdown("### 🗓️ 월별 딜 게시글 수 추이")
st.line_chart(monthly)

size = get_marcket_value_over_time()
st.markdown("### 💹 월별 시장 규모 추이")
st.line_chart(size)

category = get_post_count_by_category()
st.markdown("### 📊 카테고리별 딜 수")
st.bar_chart(category)


