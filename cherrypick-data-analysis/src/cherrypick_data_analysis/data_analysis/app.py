from datetime import date

import streamlit as st
from cherrypick_data_analysis.data_analysis.analysis.eda_analysis import *
from cherrypick_data_analysis.shared.util.redis_util import *
from cherrypick_data_analysis.shared.database.query.deal_query import get_all_deals_dataframe, get_deal_count
from cherrypick_data_analysis.shared.database.query.comment_query import get_all_comment_dataframe, get_comment_count
from cherrypick_data_analysis.data_analysis.component.others import *
from cherrypick_data_analysis.data_analysis.component.graph import *
from cherrypick_data_analysis.data_analysis.page_module.dashboard_page import dashboard
from cherrypick_data_analysis.data_analysis.page_module.statistics_page import statistics

st.set_page_config(layout="wide")

params = {}
sidebar_login()
selected_page = sidebar_page_selector()
start_date, end_date, selected_sites = sidebar_filter()

params["start_date"] = start_date
params["end_date"] = end_date
params["selected_sites"] = selected_sites



if selected_page == "Dashboard" :
    dashboard(params)
elif selected_page == "Statistics" :
    statistics(params)