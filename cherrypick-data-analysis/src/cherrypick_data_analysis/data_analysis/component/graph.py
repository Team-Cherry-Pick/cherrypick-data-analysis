import streamlit as st
from matplotlib import pyplot as plt
from cherrypick_data_analysis.data_analysis.analysis.eda_analysis import *
import plotly.graph_objects as go


def active_user_status(selected_sites, start_date, end_date) :
    deal_df = get_user_deal_shape(selected_sites, start_date, end_date)
    st.markdown("## 기간별 활동량 개요")
    st.caption("총 계")
    col1, col2, col3 = st.columns([3, 4, 4])
    total_deals_count = deal_df['count'].sum()
    total_views = deal_df['views'].sum()
    total_writer_count = len(deal_df)

    st.caption("통계")
    with col1:
        st.metric("총 게시글 수", f"{total_deals_count:,} 건")
    with col2:
        st.metric("총 조회수", f"{total_views:,} 회")
    with col3:
        st.metric("총 딜 작성 유저 수", f"{total_writer_count:,} 명")

    

    st.dataframe(deal_df)


def trend_of_post_graph(selected_sites, start_date, end_date):

    df = get_deal_post_trend(selected_sites, start_date, end_date)
    # 시계열 그래프 그리기
    fig = go.Figure()

    # 각 출처별로 시계열 데이터 추가
    for site in df['source_site'].unique():
        site_df = df[df['source_site'] == site]
        fig.add_trace(go.Scatter(x=site_df['created_at'], y=site_df['deal_count'], mode='lines+markers', name=site))

    fig.update_layout(
        title="게시물 수 추이",
        xaxis_title="created_at",
        yaxis_title="게시물 수",
        xaxis=dict(
            rangeslider=dict(visible=True),  # 범위 슬라이더 활성화
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1M", step="month", stepmode="backward"),
                    dict(count=3, label="3M", step="month", stepmode="backward"),
                    dict(count=6, label="6M", step="month", stepmode="backward"),
                    dict(step="all")
                ])
            )
        ),
        showlegend=True
    )

    # Streamlit에 Plotly 차트 출력
    st.plotly_chart(fig)

def trend_of_views_graph(selected_sites, start_date, end_date):

    df = get_deal_post_trend(selected_sites, start_date, end_date)

    # 시계열 그래프 그리기
    fig = go.Figure()

    # 각 출처별로 시계열 데이터 추가
    for site in df['source_site'].unique():
        site_df = df[df['source_site'] == site]
        fig.add_trace(go.Scatter(x=site_df['created_at'], y=site_df['views'], mode='lines+markers', name=site))

    fig.update_layout(
        title="총 조회수 추이",
        xaxis_title="created_at",
        yaxis_title="조회수",
        xaxis=dict(
            rangeslider=dict(visible=True),  # 범위 슬라이더 활성화
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1M", step="month", stepmode="backward"),
                    dict(count=3, label="3M", step="month", stepmode="backward"),
                    dict(count=6, label="6M", step="month", stepmode="backward"),
                    dict(step="all")
                ])
            )
        ),
        showlegend=True
    )

    # Streamlit에 Plotly 차트 출력
    st.plotly_chart(fig)

def line_chart(title:str, key, dataframe) :
    col1, col2 = st.columns([6.4, 3.6])
    with col1 :
        st.markdown(f"### {title}")
        st.pyplot(dataframe)
    with col2 :
        messages = st.container(height=300)
        if prompt := st.chat_input(key=f"{key}_chat"):
            messages.chat_message("user").write(prompt)
            messages.chat_message("assistant").write(f"Echo: {prompt}")

def bar_chart(title: str, key, dataframe):

    col1, col2 = st.columns([6.4, 3.6])
    with col1 :
        st.markdown(f"### {title}")
        st.bar_chart(dataframe)
    with col2 :
        st.text_area(f"{key}_memo", height=250)


