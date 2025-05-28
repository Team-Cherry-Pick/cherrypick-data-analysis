import streamlit as st
import pandas as pd
import numpy as np
from cherrypick_data_analysis.shared.database.database import engine, Base
from cherrypick_data_analysis.shared.query.deal_query import get_all_deals_dataframe

st.title("🍒CHERRYPICK DATA ANALYSIS🍒")

df = get_all_deals_dataframe()
if "category_name" in df.columns:
    category_stats = df["category_name"].value_counts().reset_index()
    category_stats.columns = ["category_name", "count"]

    st.markdown("### 📊 카테고리별 딜 수")
    st.bar_chart(category_stats.set_index("category_name"))
else:
    st.info("category_name 컬럼이 없어 차트를 그릴 수 없습니다.")

df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
df["월"] = df["created_at"].dt.strftime("%Y.%m")

monthly = df["월"].value_counts().reset_index()
monthly.columns = ["월", "게시글수"]
monthly = monthly.sort_values("월")

st.markdown("### 🗓️ 월별 딜 게시글 수 추이")
st.line_chart(monthly.set_index("월"))
