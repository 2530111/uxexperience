import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# -------------------------------
# 📌 EDA 클래스 정의
# -------------------------------
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
        # 여기서는 간단하게 원본 반환
        return df

    @staticmethod
    def 모든_그래프_그리기(df):
        num_cols = len(df.columns)
        fig, axes = plt.subplots(num_cols, num_cols, figsize=(4*num_cols, 4*num_cols))

        for i in range(num_cols):
            for j in range(num_cols):
                ax = axes[i, j]
                x = df.iloc[:, j]
                y = df.iloc[:, i]

                if i == j:
                    # 대각선: 히스토그램
                    ax.hist(x.dropna(), bins=30, color='skyblue', edgecolor='black')
                    ax.set_title(f"Histogram of {df.columns[i]}")
                else:
                    # 나머지: 산점도
                    ax.scatter(x, y, alpha=0.5)
                    ax.set_xlabel(df.columns[j])
                    ax.set_ylabel(df.columns[i])

        plt.tight_layout()
        st.pyplot(fig)

# -------------------------------
# 📌 EDA 인스턴스
# -------------------------------
eda = EDA()

# -------------------------------
# 📌 데이터 불러오기
# -------------------------------
file_path = 'UI_UX_Dataset.csv'
data = pd.read_csv(file_path)

st.header("UI/UX User Interaction Dataset")

st.session_state['data'] = data
st.session_state['data_loaded'] = True

st.success("데이터셋 불러오기 성공!")
st.write(data.head())

with st.expander("전체 데이터 보기"):
    st.write(data)

# -------------------------------
# 📌 열 선택
# -------------------------------
if st.session_state['data_loaded']:
    data = st.session_state['data']
    st.subheader("분석할 열을 선택해주세요!")
    st.success(f"데이터는 {data.shape[0]}개의 행, {data.shape[1]}개의 열로 이루어져 있습니다. 원하는 열만 선택해보세요!")

    select_all = st.checkbox("모든 열 선택하기", value=False, key="select_all")

    if select_all:
        default_columns = data.columns.tolist()
    else:
        default_columns = st.session_state.get('selected_columns', [])

    selected_columns = st.multiselect(
        "분석할 열 선택:",
        data.columns.tolist(),
        default=default_columns
    )

    st.write(data[selected_columns].head())

    st.session_state['selected_columns'] = selected_columns

    if st.button("열 선택 완료!"):
        st.session_state['columns_selected'] = True
        st.success("열 선택이 완료되었습니다!")

# -------------------------------
# 📌 데이터 타입 설정
# -------------------------------
if st.session_state.get('columns_selected', False):
    st.subheader("선택한 열의 데이터 타입을 설정하세요!")

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
                f"'{column}'의 데이터 유형:",
                options_kr,
                index=default_index,
                key=f"type_{column}"
            )
            user_column_types[column] = options_dic[user_col_type]

    with col2:
        for column, col_type in dict1.items():
            default_index = options_en.index(col_type)
            user_col_type = st.radio(
                f"'{column}'의 데이터 유형:",
                options_kr,
                index=default_index,
                key=f"type_{column}"
            )
            user_column_types[column] = options_dic[user_col_type]

    if st.button("유형 설정 완료!"):
        st.session_state['user_column_types'] = user_column_types
        st.session_state['types_set'] = True
        st.success("데이터 유형이 저장되었습니다!")

# -------------------------------
# 📌 전체 그래프 출력
# -------------------------------
if st.session_state.get('types_set', False):
    st.subheader("📊 선택한 열로 전체 히스토그램 & 산점도 그리기")

    converted_data = eda.convert_column_types(data_selected, st.session_state['user_column_types'])
    st.success(f"{len(converted_data.columns)}개의 열로 {len(converted_data.columns)**2}개의 그래프가 출력됩니다!")

    eda.모든_그래프_그리기(converted_data)
