import streamlit as st

# 'authorization'의 'auth' 딕셔너리 가져오기
auth = st.secrets["authorization"]["auth"]

def get_key() :
    """
    로그인 상태라면 key 반환,
    로그아웃 상태라면 None
    """
    return st.session_state['key']

def is_admin_name(key) :
    if key in auth.values() :
        return True
    else :
        return False

