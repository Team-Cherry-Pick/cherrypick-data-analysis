import streamlit as st
import pandas as pd
import numpy as np
from cherrypick_data_analysis.glob.config.database import engine, Base
from cherrypick_data_analysis.glob.enum.site import Site
from cherrypick_data_analysis.logic.crawler.crawler_factory import crawl_start

st.title("Data Management")

# Text input and button
start_no = st.text_input("FM_KOREA Start No:")
if st.button("FM_KOREA_CRAWL"):
    crawl_start(Site.FMKOREA, start_no)

