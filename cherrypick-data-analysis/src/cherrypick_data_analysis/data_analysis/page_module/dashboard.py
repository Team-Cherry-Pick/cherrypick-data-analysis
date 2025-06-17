import streamlit as st

from cherrypick_data_analysis.data_analysis.component import *
from cherrypick_data_analysis.data_analysis.component.graph import *
from cherrypick_data_analysis.data_analysis.component.others import *
from cherrypick_data_analysis.data_analysis.analysis.eda_analysis import *


def dashboard(start_date, end_date, selected_sites) :
    main_title("🍒 CHERRYPICK DATALAB", "데이터로 결정하는 팀 체리픽의 인사이트 허브")
    data_status_card()



