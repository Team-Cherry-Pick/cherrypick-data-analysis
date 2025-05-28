import streamlit as st
from cherrypick_data_analysis.shared.enum.crawler_status import Status, DataKey
from cherrypick_data_analysis.shared.enum.site import Site
from cherrypick_data_analysis.shared.util.redis_util import set_crawler_status, get_crawler_data, get_crawler_status, \
    calculate_average_duration, set_crawler_data
from cherrypick_data_analysis.shared.query.deal_query import get_all_deals_show
from cherrypick_data_analysis.shared.config.env import MASTER_PASSWORD
from cherrypick_data_analysis.shared.query.category_query import get_all_category_dataframe

# 설정
ADMIN_PASSWORD = MASTER_PASSWORD # ✅ 비밀번호 설정

def _calculate_success_rate() -> float:
    total = get_crawler_data(Site.FMKOREA, DataKey.TOTAL_COUNT)
    fail = get_crawler_data(Site.FMKOREA, DataKey.FAILURE_COUNT)

    if not total or int(total) == 0:
        return 100.0

    return round(100 * (1 - int(fail) / int(total)), 2)

# 페이지 레이아웃
st.set_page_config(layout="wide")
st.title("📊 FMKOREA CRAWLER DASHBOARD")

# ✅ 비밀번호 게이트
with st.container():
    st.markdown("#### 🔐 관리자 전용 페이지입니다.")
    password = st.text_input("", type="password")
    if password != ADMIN_PASSWORD:
        st.warning("접근 권한이 없습니다.")
        st.stop()

# ✅ 대시보드 본문
status = get_crawler_status(Site.FMKOREA)
st.markdown(f"### 🛰️ 현재 상태: `{status.name}`")

st.divider()

col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("▶️ START", use_container_width=True):
        set_crawler_status(Site.FMKOREA, Status.RUNNING)
with col2:
    if st.button("⏹ STOP", use_container_width=True):
        set_crawler_status(Site.FMKOREA, Status.STOPPED)

# BREAK 버튼 + 확인 로직
if "break_confirm" not in st.session_state:
    st.session_state.break_confirm = False

with col3:
    if not st.session_state.break_confirm:
        if st.button("⛔ BREAK", use_container_width=True):
            st.session_state.break_confirm = True
    else:
        st.warning("정말 중단하시겠습니까?")
        confirm_col1, confirm_col2 = st.columns([1, 1])
        with confirm_col1:
            if st.button("✅ 예, 중단합니다"):
                set_crawler_status(Site.FMKOREA, Status.BREAK)
                st.session_state.break_confirm = False
        with confirm_col2:
            if st.button("❎ 취소"):
                st.session_state.break_confirm = False

# 현재 저장된 딜레이 불러오기
current_delay = get_crawler_data(Site.FMKOREA, DataKey.DELAY_TIME)

with st.container():
    st.markdown(f"⏳ 현재 딜레이: **{current_delay if current_delay else '설정 안 됨'}초**")
    delay_col1, delay_col2 = st.columns([3, 1])
    with delay_col1:
        delay_input = st.text_input("⏳ 딜레이 설정 (초)", value="", placeholder="예: 3", key="delay_input")
    with delay_col2:
        if st.button("💾 딜레이 적용", use_container_width=True):
            try:
                delay_seconds = float(delay_input)
                set_crawler_data(Site.FMKOREA, DataKey.DELAY_TIME, delay_input)
                st.success(f"딜레이가 {delay_seconds}초로 설정되었습니다.")
            except ValueError:
                st.error("올바른 숫자를 입력하세요.")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📅 시작 시간", get_crawler_data(Site.FMKOREA, DataKey.START_TIME))
with col2:
    avg = calculate_average_duration(Site.FMKOREA)
    st.metric("⚡ 평균 소요 시간", f"{avg:.2f}s" if avg else "N/A")
with col3:
    st.metric("📦 총 수집 데이터", get_crawler_data(Site.FMKOREA, DataKey.TOTAL_COUNT))

col4, col5, col6 = st.columns([1, 1, 1])

with col4:
    st.metric("❌ 실패한 데이터", get_crawler_data(Site.FMKOREA, DataKey.FAILURE_COUNT))
with col5:
    st.metric("✅ 현재 페이지", f"{get_crawler_data(Site.FMKOREA, DataKey.NOW_CRAWLING)}p")
with col6:
    st.metric("😎 마지막 수집 : ", f"{get_crawler_data(Site.FMKOREA, DataKey.LAST_SAVED_TIME)}")

st.markdown("### 📋 수집된 딜 목록")
df = get_all_deals_show()

if df is not None and not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.info("표시할 수 있는 데이터가 없습니다.")
