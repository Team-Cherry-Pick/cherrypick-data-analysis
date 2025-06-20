from cherrypick_data_analysis.data_analysis.analysis.eda_analysis import *
from cherrypick_data_analysis.data_analysis.component.graph import *


def statistics(start_date, end_date, selected_sites) :
    tab1, tab2, tab3, tab4 = st.tabs(["활동량", "유저", "게시글", "댓글"])
    with tab1 :
        activity_metric(start_date, end_date, selected_sites)



def activity_metric(start_date, end_date, selected_sites) :
    active_user_status(selected_sites, start_date, end_date)
    trend_of_post_graph(selected_sites, start_date, end_date)
    trend_of_views_graph(selected_sites, start_date, end_date)


