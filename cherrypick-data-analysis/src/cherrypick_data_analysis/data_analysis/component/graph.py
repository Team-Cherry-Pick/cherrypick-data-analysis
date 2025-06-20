import streamlit as st
from matplotlib import pyplot as plt
from cherrypick_data_analysis.data_analysis.analysis.eda_analysis import *
import plotly.graph_objects as go

def deal_status(params) :
    selected_sites = params["selected_sites"]
    start_date = params["start_date"]
    end_date = params["end_date"]

    deal_df = get_user_deal_shape(selected_sites, start_date, end_date)
    deal_df.sort_values('deal_count', ascending=False, inplace=True)
    total_deals_count = deal_df['deal_count'].sum()
    total_views = deal_df['views'].sum()
    total_writer_count = len(deal_df)

    col1, col2 = st.columns([2, 3])
    with col1:
        st.caption("DEAL")
        st.metric("총 딜 작성 유저 수", f"{total_writer_count:,} 명")
        st.metric("총 게시글 수", f"{total_deals_count:,} 건")
        st.metric("총 조회수", f"{total_views:,} 회")
    with col2:
        st.dataframe(deal_df)

def comment_status(params) :
    selected_sites = params["selected_sites"]
    start_date = params["start_date"]
    end_date = params["end_date"]

    comment_df = get_user_comment_shape(selected_sites, start_date, end_date)
    comment_df.sort_values('comment_count', ascending=False, inplace=True)
    total_comment_count = comment_df['comment_count'].sum()
    total_comment_user_count = len(comment_df)
    total_comments_vote_count = comment_df['upvote'].sum() - comment_df['downvote'].sum()

    col1, col2 = st.columns([2, 3])
    with col1:
        st.caption("COMMENT")
        st.metric("총 댓글 작성자 수", f"{total_comment_user_count:,} 회")
        st.metric("총 댓글 수", f"{total_comment_count:,} 건")
        st.metric("총 추천 수", f"{total_comments_vote_count:,} 명")
    with col2:
        st.dataframe(comment_df)


def plot_pareto_post_distribution(params : dict):
    selected_sites = params["selected_sites"]
    start_date = params["start_date"]
    end_date = params["end_date"]
    pareto_df = analyze_pareto_from_user_deals(selected_sites, start_date, end_date)
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=pareto_df["user_ratio"] * 100,
        y=pareto_df["cumulative_post_ratio"] * 100,
        mode="lines+markers",
        name="누적 게시글 비율",
        line=dict(shape="hv")
    ))

    fig.update_layout(
        title="유저별 게시글 누적 기여도 (Pareto 분석)",
        xaxis_title="누적 작성자 비율 (%)",
        yaxis_title="누적 게시글 기여도 (%)",
        xaxis=dict(tickmode='linear', tick0=0, dtick=10),
        yaxis=dict(range=[0, 100]),
        template="plotly_white"
    )

    fig.show()
    st.plotly_chart(fig)

def plot_pareto_comment_distribution(params : dict):
    selected_sites = params["selected_sites"]
    start_date = params["start_date"]
    end_date = params["end_date"]
    pareto_df = analyze_pareto_from_user_comments(selected_sites, start_date, end_date)
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=pareto_df["user_ratio"] * 100,
        y=pareto_df["cumulative_post_ratio"] * 100,
        mode="lines+markers",
        name="누적 댓글 비율",
        line=dict(shape="hv")
    ))

    fig.update_layout(
        title="유저별 댓글 누적 기여도 (Pareto 분석)",
        xaxis_title="누적 작성자 비율 (%)",
        yaxis_title="누적 댓글 기여도 (%)",
        xaxis=dict(tickmode='linear', tick0=0, dtick=10),
        yaxis=dict(range=[0, 100]),
        template="plotly_white"
    )

    fig.show()
    st.plotly_chart(fig)

def trend_of_post_graph(params):
    selected_sites = params["selected_sites"]
    start_date = params["start_date"]
    end_date = params["end_date"]
    df = get_deal_post_trend(selected_sites, start_date, end_date)
    # 시계열 그래프 그리기
    fig = go.Figure()

    # 각 출처별로 시계열 데이터 추가
    for site in df['source_site'].unique():
        site_df = df[df['source_site'] == site]
        fig.add_trace(go.Scatter(x=site_df['created_at'], y=site_df['deal_count'], mode='lines+markers', name=site))

    fig.update_layout(
        title="게시물 수 추이",
        xaxis_title="날짜",
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

def trend_of_views_graph(params):
    selected_sites = params["selected_sites"]
    start_date = params["start_date"]
    end_date = params["end_date"]
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


