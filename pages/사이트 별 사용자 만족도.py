import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

file_path = 'UI_UX_Dataset.csv'
data = pd.read_csv(file path)

st.header("UI/UX user interaction dataset across popular digital platforms")

st.session_state['data'] = data
st.session_state['data_loaded'] = True
st.write("데이터셋을 성공적으로 불러왔습니다.")
st.write(data.head())
    with st.expander('전체 데이터 보기'):
        st.write(data)

      
