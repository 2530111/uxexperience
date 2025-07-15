import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# 예시 EDA 함수
class EDA:
    @staticmethod
    def infer_column_types(df):
        inferred = {}
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                inferred[col] = 'Numeric'
            else:
                inferred[col] = 'Categorical'
        return inferred

    @staticmethod
    def convert_column_types(df, types):
        # 여기서는 타입 변환 안 하고 그냥 원본 반환
        return df

    @staticmethod
    def 모든_그래프_그리기(df):
        st.write("📊 (여기에 모든 그래프 출력!)")

eda = EDA()

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

    select_all = st.checkbox('모든 열 선택하기', key='select_all', value=False)

    if select_all:
        default_columns = data.columns.tolist()
    else:
        default_columns = st.session_state.get('selected_columns', [])

    selected_columns = st.multiselect(
        '분석하고자 하는 열을 선택하세요:',
        data.columns.tolist(),
        default=default_columns
    )

    st.write(data[selected_columns].head())

    st.session_state['selected_columns'] = selected_columns

    if st.button('열 선택 완료!'):
        st.session_state['columns_selected'] = True
        st.success("열 선택 완료!")

if st.session_state.get('columns_selected', False):
    st.success("각 변수의 데이터 유형을 확인하세요!")

    if st.session_state['selected_columns'] is not None:
        data_selected = st.session_state['data'][st.session_state['selected_columns']]
        inferred_types = eda.infer_column_types(data_selected)
        user_column_types = {}

        options_en = ['Numeric', 'Categorical']
        options_kr = ["수치형", "범주형"]
        options_dic = {'수치형': 'Numeric', '범주형': 'Categorical'}

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

        if st.button('유형 변경 완료!'):
            st.session_state['user_column_types'] = user_column_types
            st.session_state['types_set'] = True
            st.success("데이터 유형 변경완료!")

# ✅ 조건문 고쳐야 함!!
if st.session_state.get('types_set', False):
    st.subheader("📊 데이터 한꺼번에 요약과 시각화")
    data_selected = st.session_state['data'][st.session_state['selected_columns']]
    user_column_types = st.session_state['user_column_types']
    converted_data = eda.convert_column_types(data_selected, user_column_types)
    st.success(f"설정된 열의 개수: {len(converted_data.columns)} → {len(converted_data.columns)**2}개의 그래프가 그려집니다.")

    st.session_state['converted_data'] = converted_data

    tab1, tab2 = st.tabs(['데이터 시각화', '기술통계량 확인하기'])

    with tab1:
        eda.모든_그래프_그리기(converted_data)
        st.session_state['viz'] = True

    with tab2:
        for column, col_type in user_column_types.items():
            st.write(f"**{column}** ({col_type})")
            if col_type == 'Numeric':
                numeric_descriptive = pd.DataFrame(converted_data[column].describe()).T
                numeric_descriptive.columns = ['총 개수', '평균', '표준편차', '최솟값', '제1사분위수', '중앙값', '제3사분위수', '최댓값']
                st.write(numeric_descriptive)
            elif col_type == 'Categorical':
                categoric_descriptive = pd.DataFrame(converted_data[column].value_counts()).T
                categoric_descriptive.index = ["개수"]
                st.write(categoric_descriptive.style.background_gradient(axis=1))
