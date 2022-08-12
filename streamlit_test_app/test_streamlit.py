import streamlit as st

def run():
    st.selectbox(label='yolo', options=[1, 2], on_change=lambda x: print(x), args=any)

run()