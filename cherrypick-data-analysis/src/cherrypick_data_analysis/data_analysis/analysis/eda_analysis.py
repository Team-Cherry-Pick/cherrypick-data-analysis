from typing import List
import pandas as pd
from cherrypick_data_analysis.shared.database.database import get_session
from cherrypick_data_analysis.shared.database.model import Deal
from cherrypick_data_analysis.shared.enum.site import Site
from cherrypick_data_analysis.shared.util.redis_util import *
from cherrypick_data_analysis.shared.query.deal_query import get_all_deals_dataframe


# 월별 게시물 수 추이
def get_monthly_deal_post_trend(site_list: List[Site]) -> pd.DataFrame:

    df = get_cache(CacheKey.DEAL_ALL)
    if df is None :
        df = get_all_deals_dataframe()
        set_cache(CacheKey.DEAL_ALL, df)

    df["년월"] = df.created_at.dt.strftime("%y.%m")
    df["사이트"] = df = df[df["사이트"].isin(site_list)]
    grouped = df.groupby(["년월", "사이트"]).size().reset_index(name="게시글 수")
    pivoted = grouped.pivot(index="년월", columns="사이트", values="게시글 수").fillna(0).astype(int)

    return pivoted

# 카테고리 별 게시글 수
def get_post_count_by_category() -> pd.DataFrame:
    df = get_cache(CacheKey.DEAL_ALL)
    if df is None :
        df = get_all_deals_dataframe()
        set_cache(CacheKey.DEAL_ALL, df)

    df["카테고리"] = df.category_name
    grouped = df.groupby(["카테고리"]).size().reset_index(name="게시물 수")
    pivoted = grouped.set_index("카테고리")
    return pivoted

# 총 시장가치 그래프
def get_marcket_value_over_time(site_list: List[Site]) -> pd.DataFrame:
    df = get_cache(CacheKey.DEAL_ALL)
    if df is None :
        df = get_all_deals_dataframe()
        set_cache(CacheKey.DEAL_ALL, df)

    # 그래프 만들기 전 전처리
    df["년월"] = df.created_at.dt.strftime("%Y.%m")
    df["사이트"] = df["source_site"]
    df["discounted_price"] = df["discounted_price"].dropna()
    df["타입"] = df["price_type"]

    df["가치"] = df["discounted_price"] * df["views"] * 0.02 * 1500 if df["타입" == "USD"] else df["discounted_price"] * df["views"] * 0.02

    grouped = df.groupby(["년월", "타입"])["가치"].sum().reset_index(name="규모")
    pivoted = grouped.pivot(index="년월", columns="타입", value="규모")
    pivoted["합계"] = pivoted[pivoted["타입"] == "USD"] + pivoted[pivoted["타입"] == "KRW"]
    return pivoted

