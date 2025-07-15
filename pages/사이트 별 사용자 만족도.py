import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

file_path = 'UI_UX_Dataset.csv'
data = pd.read_csv(file_path)

st.header("UI/UX user interaction dataset across popular digital platforms")

st.session_state['data'] = data      
st.session_state['data_loaded'] = True
st.write("데이터셋을 성공적으로 불러왔습니다.")
st.write(data.head())
with st.expander('전체 데이터 보기'):
    st.write(data)

if st.session_state['data_loaded']:
    data = st.session_state['data']
    st.subheader("분석할 열을 선택해주세요.")
    st.success(f"이 데이터는 {data.shape[0]}개의 행, {data.shape[1]}개의 열로 이루어진 데이터입니다. 열이 많으니 몇 개만 골라서 분석하는 걸 추천합니다.")
    if st.checkbox('모든 열 선택하기', key='select_all', value = data.columns.all()):
        default_columns = data.columns.tolist() if 'select_all' in st.session_state and st.session_state['select_all'] else []
    else:
        default_columns = data.columns.tolist() if 'selected_columns' not in st.session_state else st.session_state['selected_columns']

    selected_columns = st.multiselect('분석하고자 하는 열을 선택하세요:', st.session_state['data'].columns.tolist(), default=default_columns)
    st.write(data[selected_columns].head())

    st.session_state['selected_columns'] = selected_columns
    if st.button('열 선택 완료!'):
        st.session_state['columns_selected'] = True
        st.success("열 선택 완료!")

