from datetime import date, timedelta, datetime
from cherrypick_data_analysis.shared.util.redis_util import cache_init, get_cache
from cherrypick_data_analysis.shared.enum.cachekey import CacheKey
from cherrypick_data_analysis.shared.enum.site import Site
from streamlit_option_menu import option_menu
from cherrypick_data_analysis.shared.util.redis_util import get_memo_list, push_memo
from cherrypick_data_analysis.data_analysis.util.auth_util import *
from cherrypick_data_analysis.shared.util.redis_util import delete_memo

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

        if get_key() is None:
            key = st.text_input("login", placeholder="Enter your key",  label_visibility="hidden")
            if st.button("login"):
                if key:
                    if not is_admin_name(key) :
                        if key in list(auth):
                            key = auth[key]
                        st.session_state["key"] = key
                        st.toast("로그인 성공 !")
                        st.balloons()
                    else : st.toast("다른 key로 로그인해주세요 !")
                else : st.toast("key를 입력해주세요 !")
        else:
            st.write(f"hello ! {get_key()}, nice to meet you!")

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
        menu_icon="bookmark-star-fill",
        icons=["compass-fill", "bar-chart-line-fill", "file-person-fill"],
        default_index=0
      )
    return selected

# 인증된 유저만 보이는 메모
def auth_memo_component(key : str, height:int) :
    if get_key() : memo_component(key, height)

# 메모 컴포넌트
def memo_component(key : str, height:int) :
    con = st.container(height=height)

    with con :
        memo_list = get_memo_list(key)
        messages = st.container(height= height-100)
        if not memo_list :
            messages.write("첫 메모를 남겨보세요 !")
        idx = 0
        for memo in memo_list :
            with messages.chat_message("user") :
                col1, col2 = st.columns([8, 2])
                with col1 : st.write(f"{memo['writer']} | {memo['created_at']}")
                with col2 :
                    if is_admin_name(get_key()) :
                        if st.button(f"delete", key=f"del{idx}") :
                            delete_memo(key, idx)

                st.write(f"{memo['content']}")
            idx += 1

        if get_key() is not None :
            if prompt := st.chat_input("Say something"):
                memo = {"writer" : get_key(), "content" : prompt, "created_at" : datetime.now().strftime("%Y.%m.%d %H:%M")}
                push_memo(key, memo)
                with messages.chat_message("user"):
                    st.write(f"{memo['writer']} | {memo['created_at']}")
                    st.write(f"{memo['content']}")
