import site

import streamlit as st

from cherrypick_data_analysis.data_analysis.component import *
from cherrypick_data_analysis.data_analysis.component.graph import *
from cherrypick_data_analysis.data_analysis.component.others import *
from cherrypick_data_analysis.data_analysis.analysis.eda_analysis import *


def dashboard(params) :
    main_title("🍒 CHERRYPICK DATALAB", "데이터로 결정하는 팀 체리픽의 인사이트 허브")
    st.markdown("### 🗂️ 보유 데이터 현황")
    col1, col2, col3 = st.columns([3, 3, 4])
    with col1 :
        data_inventory_status_card(Site.FMKOREA)
    with col2 :
        data_inventory_status_card(Site.PPOMPPU)

    memo_component("main", 400)
    st.divider()
    st.markdown("## 🗂️ 기간별 활동량 개요")

    deal_status(params)
    comment_status(params)



