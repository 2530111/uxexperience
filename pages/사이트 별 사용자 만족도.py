import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

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
        # 필요하면 타입 변환 로직 추가!
        return df


def 모든_그래프_그리기(df, types):
    num_cols = len(df.columns)
    fig, axes = plt.subplots(num_cols, num_cols, figsize=(4*num_cols, 4*num_cols))

    for i in range(num_cols):
        for j in range(num_cols):
            ax = axes[i, j]
            x = df.iloc[:, j]
            y = df.iloc[:, i]
            x_name = df.columns[j]
            y_name = df.columns[i]

            x_type = types[x_name]
            y_type = types[y_name]

            if i == j:
                # 수치형: hist + KDE
                if x_type == 'Numeric':
                    sns.histplot(x, kde=True, ax=ax, color='orange')
                else:
                    sns.countplot(x=x, ax=ax, palette='pastel')
                ax.set_title(f"{x_name}")
            else:
                if x_type == 'Numeric' and y_type == 'Numeric':
                    sns.scatterplot(x=x, y=y, ax=ax, alpha=0.5)
                elif x_type == 'Categorical' and y_type == 'Numeric':
                    sns.boxplot(x=x, y=y, ax=ax, palette='Set2')
                elif x_type == 'Numeric' and y_type == 'Categorical':
                    sns.boxplot(x=y, y=x, ax=ax, palette='Set2')
                elif x_type == 'Categorical' and y_type == 'Categorical':
                    sns.countplot(x=x, hue=y, ax=ax)
                ax.set_xlabel(x_name)
                ax.set_ylabel(y_name)

    plt.tight_layout()
    st.pyplot(fig)


# -------------------------------
# 📌 Streamlit 앱 시작!
# -------------------------------
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
    if st.checkbox('모든 열 선택하기', key='select_all'):
        default_columns = data.columns.tolist()
    else:
        default_columns = data.columns.tolist() if 'selected_columns' not in st.session_state else st.session_state['selected_columns']

    selected_columns = st.multiselect('분석하고자 하는 열을 선택하세요:', data.columns.tolist(), default=default_columns)
    st.write(data[selected_columns].head())

    st.session_state['selected_columns'] = selected_columns
    if st.button('열 선택 완료!'):
        st.session_state['columns_selected'] = True
        st.success("열 선택 완료!")

if st.session_state.get('columns_selected', False):
    st.subheader("선택한 열의 데이터 타입을 선택해주세요!")

    data_selected = data[st.session_state['selected_columns']]
    inferred_types = EDA.infer_column_types(data_selected)
    user_column_types = {}

    options_en = ['Numeric', 'Categorical']
    options_kr = ['수치형', '범주형']
    options_dic = {'수치형': 'Numeric', '범주형': 'Categorical'}

    col1, col2 = st.columns(2)
    keys = list(inferred_types.keys())
    half = len(keys) // 2

    dict1 = {key: inferred_types[key] for key in keys[:half]}
    dict2 = {key: inferred_types[key] for key in keys[half:]}

    with col1:
        for column, col_type in dict1.items():
            default_index = options_en.index(col_type)
            user_col_type = st.radio(
                f"'{column}' 데이터 유형:",
                options_kr,
                index=default_index,
                key=f"type_{column}"
            )
            user_column_types[column] = options_dic[user_col_type]

    with col2:
        for column, col_type in dict2.items():
            default_index = options_en.index(col_type)
            user_col_type = st.radio(
                f"'{column}' 데이터 유형:",
                options_kr,
                index=default_index,
                key=f"type_{column}"
            )
            user_column_types[column] = options_dic[user_col_type]

    if st.button("데이터 유형 저장하기"):
        st.session_state['user_column_types'] = user_column_types
        st.session_state['types_set'] = True
        st.success("데이터 유형이 저장되었습니다!")

# -------------------------------
# 📌 최종 그래프 그리기
# -------------------------------
if st.session_state.get('types_set', False):
    st.subheader("📊 선택한 열로 전체 히스토그램 & 산점도 그리기")

    converted_data = EDA.convert_column_types(
        data[st.session_state['selected_columns']],
        st.session_state['user_column_types']
    )

    st.success(
        f"{converted_data.shape[0]}개 행, {converted_data.shape[1]}개 열로 {converted_data.shape[1] ** 2}개 그래프 출력!"
    )

    모든_그래프_그리기(converted_data, st.session_state['user_column_types'])
