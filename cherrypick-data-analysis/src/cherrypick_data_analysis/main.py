import streamlit as st
import pandas as pd
import numpy as np
from logic.model import *
from cherrypick_data_analysis.glob.config.database import engine, Base


def init_func():
    print(Base.metadata.tables.keys())
    Base.metadata.create_all(engine)
    st.write("초기화 작업 실행됨")

if 'init_done' not in st.session_state:
    init_func()
    st.session_state['init_done'] = True


st.title("Streamlit Basic Example")

# Sidebar input
age = st.sidebar.slider("Select your age", 0, 100, 25)
gender = st.sidebar.radio("Select your gender", ["Male", "Female", "Other"])

st.write(f"Age: {age}, Gender: {gender}")

# Text input and button
name = st.text_input("Enter your name:")
if st.button("Greet"):
    st.write(f"Hello, {name}!")

# Display dataframe with random data
data = pd.DataFrame(np.random.randn(10, 3), columns=["A", "B", "C"])
st.dataframe(data)

# Chart example
st.line_chart(data["A"])

# File uploader example
uploaded_file = st.file_uploader("Upload a CSV file")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Uploaded CSV data:")
    st.dataframe(df)
