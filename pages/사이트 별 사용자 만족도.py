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
    st.success(f"이 데이터는 {data.shape[0]}개의 행(가로줄), {data.shape[1]}개의 열(세로줄)로 이루어진 데이터입니다. 이중 분석할 열만 선택해주세요.")
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

if st.session_state['columns_selected']:
    st.success("데이터를 살펴보고, 각 변수가 수치형인지 범주형인지 확인해보세요.")
    if st.session_state['selected_columns'] is not None:
        data_selected = st.session_state['data'][st.session_state['selected_columns']]
        inferred_types = eda.infer_column_types(data_selected)
        user_column_types = {}

        options_en = ['Numeric', 'Categorical']
        options_kr = ["수치형", "범주형"]
        options_dic = {'수치형': 'Numeric', '범주형': 'Categorical'}
        
        # 반반 나눠서 나열
        col1, col2 = st.columns(2)
        keys = list(inferred_types.keys())
        half = len(keys) // 2 

        dict1 = {key: inferred_types[key] for key in keys[:half]}
        dict2 = {key: inferred_types[key] for key in keys[half:]}

        with col1:
            for column, col_type in dict2.items():
                default_index = options_en.index(col_type)
                user_col_type = st.radio(
                    f"'{column}'의 유형:",
                    options_kr,
                    index=default_index,
                    key=column
                )
                user_column_types[column] = options_dic[user_col_type]



        with col2:
            for column, col_type in dict1.items():
                default_index = options_en.index(col_type)
                user_col_type = st.radio(
                    f"'{column}'의 유형:",
                    options_kr,
                    index=default_index,
                    key=column
                )
                user_column_types[column] = options_dic[user_col_type]
        # for col in df_selected.columns:
        #     col_type = st.selectbox(f"{col} 유형 선택", ['Numeric', 'Categorical'], index=0 if inferred_types[col] == 'Numeric' else 1, key=col)
        #     user_column_types[col] = col_type
        if st.button('유형 변경 완료!'):
            st.session_state['user_column_types'] = user_column_types
            st.session_state['types_set'] = True
            st.success("데이터 유형 변경완료!")






