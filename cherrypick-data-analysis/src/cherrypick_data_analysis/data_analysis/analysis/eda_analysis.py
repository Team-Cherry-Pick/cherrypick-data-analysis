from typing import List
import pandas as pd
from cherrypick_data_analysis.shared.util.redis_util import *
from cherrypick_data_analysis.shared.database.query.deal_query import get_all_deals_dataframe
import calendar

# 월별 게시물 수 추이
def get_monthly_deal_post_trend(site_list: List[str], start_date:datetime, end_date:datetime) -> pd.DataFrame:

    start_date, end_date = get_monthly_range(start_date, end_date)

    df = get_cache(CacheKey.DEAL_ALL)
    if df is None :
        df = get_all_deals_dataframe()
        set_cache(CacheKey.DEAL_ALL, df)

    df = df[df["source_site"].isin(site_list)]
    df = df[(df["created_at"] >= start_date) & (df["created_at"] <= end_date)]
    df["사이트"] = df["source_site"]
    df["년월"] = df.created_at.dt.strftime("%y.%m")
    grouped = df.groupby(["년월", "사이트"]).size().reset_index(name="게시글 수")
    pivoted = grouped.pivot(index="년월", columns="사이트", values="게시글 수")
    pivoted["TOTAL"] = pivoted[site_list].sum(axis=1)

    return pivoted

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

# 월별 게시물 수 추이
def get_monthly_deal_view_trend(site_list: List[str], start_date:datetime, end_date:datetime) -> pd.DataFrame:

    start_date, end_date = get_monthly_range(start_date, end_date)

    df = get_cache(CacheKey.DEAL_ALL)
    if df is None :
        df = get_all_deals_dataframe()
        set_cache(CacheKey.DEAL_ALL, df)

    df = df[df["source_site"].isin(site_list)]
    df = df[(df["created_at"] >= start_date) & (df["created_at"] <= end_date)]

    df["사이트"] = df["source_site"]
    df["년월"] = df.created_at.dt.strftime("%y.%m")
    grouped = df.groupby(["년월", "사이트"])["views"].sum().reset_index(name="조회수 합계")
    pivoted = grouped.pivot(index="년월", columns="사이트", values="조회수 합계")
    pivoted["TOTAL"] = pivoted[site_list].sum(axis=1)

    return pivoted

def get_monthly_range(start_date, end_date):
    _, last_day = calendar.monthrange(end_date.year, end_date.month)
    start_date.replace(day=1)
    end_date.replace(day=last_day)
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    return start_date, end_date