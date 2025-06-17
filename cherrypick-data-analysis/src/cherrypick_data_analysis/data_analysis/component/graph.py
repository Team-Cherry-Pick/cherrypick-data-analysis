import streamlit as st

def line_chart(title:str, dataframe) :
    st.markdown(f"### {title}")
    st.line_chart(dataframe)

def bar_chart(title: str, dataframe):
    st.markdown(f"### {title}")
    st.bar_chart(dataframe)
