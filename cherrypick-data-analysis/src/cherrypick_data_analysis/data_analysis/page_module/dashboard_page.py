import site

import streamlit as st

from cherrypick_data_analysis.data_analysis.component import *
from cherrypick_data_analysis.data_analysis.component.graph import *
from cherrypick_data_analysis.data_analysis.component.others import *
from cherrypick_data_analysis.data_analysis.analysis.eda_analysis import *


def dashboard(params) :
    main_title("🍒 CHERRYPICK DATALAB", "데이터로 결정하는 팀 체리픽의 인사이트 허브")

    with st.expander("Guidelines") :
        col1, col2 = st.columns(2)
        with col1 :
            st.html(
                """
                    체리픽 데이터랩은 핫딜 플랫폼 ‘팀 체리픽’에서 발생하는 다양한 사용자 행동 데이터를 수집·분석하는 내부 분석 시스템입니다.<br>
                    사용자의 클릭, 투표, 댓글, 조회수 등 실제 활동 데이터를 기반으로, 어떤 상품이 인기를 끌고 있는지, 어떤 요소가 사용자 반응에 영향을 미치는지 등 다양한 인사이트를 도출합니다.<br>
                    현재 뽐뿌, 에펨코리아의 핫딜 정보를 수집 중이며, 추후 <b>자사 서비스의 데이터</b>도 추가될 예정입니다.<br>
                    수집된 데이터는 Streamlit 기반의 대시보드에서 시각화되어 누구나 쉽게 확인할 수 있으며, 이를 바탕으로 콘텐츠 개선, 상품 추천, 마케팅 전략 수립 등에 활용됩니다.<br><br>
    
                    <b>데이터로 움직이는 팀 체리픽, 그 중심에 데이터랩이 있습니다.</b><br>
                """)
        with col2 : memo_component("main_meno", 400)
    st.markdown("### 🗂️ 보유 데이터 현황")
    col1, col2, col3 = st.columns([3, 3, 4])
    with col1 :
        data_inventory_status_card(Site.FMKOREA)
    with col2 :
        data_inventory_status_card(Site.PPOMPPU)

    st.divider()
    st.markdown("## 🗂️ 기간별 활동량 개요")

    deal_status(params)
    comment_status(params)



