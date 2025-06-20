import streamlit as st
from typing import List
import pandas as pd
from matplotlib import pyplot as plt
from cherrypick_data_analysis.shared.util.redis_util import *
import calendar
from cherrypick_data_analysis.shared.database.query.deal_query import *
from cherrypick_data_analysis.shared.database.query.comment_query import *


# 월별 게시물 수 추이
@st.cache_data
def get_deal_post_trend(site_list: List[str], start_date: datetime, end_date: datetime) -> pd.DataFrame:
    # 월별 데이터
    result = get_total_deal_count_group_by_create_at()

    # DataFrame으로 변환
    df = pd.DataFrame.from_records(result, columns=["created_at", "source_site", "deal_count", "views", "comment_count", "vote_count"])
    df['source_site'] = df['source_site'].apply(lambda x : x.name)

    # 'created_at' 컬럼을 datetime 형식으로 변환
    df = df[df['source_site'].isin(site_list)]
    df = df[(start_date <= df['created_at']) & (df['created_at'] <= end_date)]
    df['created_at'] = pd.to_datetime(df['created_at'])
    df = df.sort_values(by='created_at')

    return df

@st.cache_data
def get_user_deal_shape(site_list: List[str], start_date: datetime, end_date: datetime) -> pd.DataFrame:
    print(datetime.now())
    deal_result = get_total_deal_user(start_date, end_date)

    deal_df = pd.DataFrame([{
        "username" : data[0],
        "source_site" : data[1].name,
        "deal_count" : data[2],
        "views" : data[3],
        "vote" : data[4],
        "comment_count" : data[5]
    } for data in deal_result])

    df = deal_df[deal_df['source_site'].isin(site_list)]
    return df

@st.cache_data
def analyze_pareto_from_user_deals(
    site_list: List[str],
    start_date: datetime,
    end_date: datetime
) -> pd.DataFrame:
    """
    주어진 기간과 사이트 리스트에 따라 유저별 게시글 파레토 분석 결과 반환
    """
    # 유저별 deal 데이터 가져오기
    deal_df = get_user_deal_shape(site_list, start_date, end_date)

    # 게시글 수 기준 내림차순 정렬
    df_sorted = deal_df.sort_values(by="deal_count", ascending=False).reset_index(drop=True)

    # 누적 게시글 수 및 비율 계산
    total_deals = df_sorted["deal_count"].sum()
    df_sorted["cumulative_post"] = df_sorted["deal_count"].cumsum()
    df_sorted["cumulative_post_ratio"] = df_sorted["cumulative_post"] / total_deals

    # 유저 비율 계산
    df_sorted["user_ratio"] = (df_sorted.index + 1) / len(df_sorted)

    return df_sorted[[
        "username", "source_site", "deal_count",
        "user_ratio", "cumulative_post_ratio"
    ]]


@st.cache_data
def get_user_comment_shape(site_list: List[str], start_date: datetime, end_date: datetime):

    comment_result = get_total_comment_user(start_date, end_date)

    # Modin DataFrame으로 변환
    comment_df = pd.DataFrame.from_records(
        comment_result,
        columns=["username", "source_site", "comment_count", "upvote", "downvote"]
    )

    # enum -> 문자열로 변환
    comment_df["source_site"] = comment_df["source_site"].apply(lambda x: x.name)
    # site_list 필터링
    df = comment_df[comment_df["source_site"].isin(site_list)]

    return df

@st.cache_data
def analyze_pareto_from_user_comments(
    site_list: List[str],
    start_date: datetime,
    end_date: datetime
) -> pd.DataFrame:
    """
    주어진 기간과 사이트 리스트에 따라 유저별 게시글 파레토 분석 결과 반환
    """
    # 유저별 deal 데이터 가져오기
    comment_df = get_user_comment_shape(site_list, start_date, end_date)

    # 게시글 수 기준 내림차순 정렬
    df_sorted = comment_df.sort_values(by="comment_count", ascending=False).reset_index(drop=True)

    # 누적 게시글 수 및 비율 계산
    total_deals = df_sorted["comment_count"].sum()
    df_sorted["cumulative_post"] = df_sorted["comment_count"].cumsum()
    df_sorted["cumulative_post_ratio"] = df_sorted["cumulative_post"] / total_deals

    # 유저 비율 계산
    df_sorted["user_ratio"] = (df_sorted.index + 1) / len(df_sorted)

    return df_sorted[[
        "username", "source_site", "comment_count",
        "user_ratio", "cumulative_post_ratio"
    ]]

# 카테고리 별 게시글 수
def get_post_count_by_category() -> pd.DataFrame:
    df = get_cache(CacheKey.DEAL_ALL)
    if df is None :
        df = get_all_deals_dataframe()
        set_cache(CacheKey.DEAL_ALL, df)

    df["카테고리"] = df.category_name
    df = df[df.category_name != "분류불가"]
    grouped = df.groupby(["카테고리"]).size().reset_index(name="게시물 수")
    pivoted = grouped.set_index("카테고리")
    return pivoted

# 총 시장가치 그래프
def get_marcket_value_over_time() -> pd.DataFrame:
    df = get_cache(CacheKey.DEAL_ALL)
    if df is None :
        df = get_all_deals_dataframe()
        set_cache(CacheKey.DEAL_ALL, df)

    # 그래프 만들기 전 전처리
    df["년월"] = df.created_at.dt.strftime("%Y.%m")
    df["사이트"] = df["source_site"]
    df["discounted_price"] = df["discounted_price"].dropna()
    df["타입"] = df["price_type"]

    # 시장 규모 : market_size = prices*views*0.02
    df["가치"] = df["discounted_price"] * df["views"] * 0.02
    df.loc[df["price_type"] == "USD", "가치"] *= 1500  # 환율 적용

    grouped = df.groupby(["년월", "타입"])["가치"].sum().reset_index(name="규모")
    pivoted = grouped.pivot(index="년월", columns="타입", values="규모")
    pivoted["합계"] = pivoted["USD"] + pivoted["KRW"]
    return pivoted



def get_monthly_range(start_date, end_date):
    _, last_day = calendar.monthrange(end_date.year, end_date.month)
    start_date.replace(day=1)
    end_date.replace(day=last_day)
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    return start_date, end_date