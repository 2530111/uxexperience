import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ----------------------------------------
# EDA 클래스
# ----------------------------------------
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
    def plot_histograms(df):
        fig, axes = plt.subplots(len(df.columns), 1, figsize=(8, 4 * len(df.columns)))
        if len(df.columns) == 1:
            axes = [axes]
        for ax, col in zip(axes, df.columns):
            sns.histplot(df[col].dropna(), kde=True, ax=ax)
            ax.set_title(f"{col} 분포")
        st.pyplot(fig)

    @staticmethod
    def plot_scatter(df, x_col, y_col):
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.scatterplot(x=df[x_col], y=df[y_col], ax=ax)
        ax.set_title(f"{x_col} vs {y_col}")
        st.pyplot(fig)

    @staticmethod
    def plot_pairplot(df):
        fig = sns.pairplot(df)
        st.pyplot(fig)


eda = EDA()

# ----------------------------------------
# 데이터 로드
# ----------------------------------------
file_path = 'UI_UX_Dataset.csv'
data = pd.read_csv(file_path)

st.title("📊 UI/UX Dataset EDA (공통 열 선택 탭 버전)")

# ----------------------------------------
# 공통 열 선택
# ----------------------------------------
selected_cols = st.multiselect(
    "📌 분석에 사용할 열 선택 (전체 탭 공통)",
    data.columns.tolist()
)

if selected_cols:
    selected_data = data[selected_cols]

    tab1, tab2, tab3 = st.tabs(["📊 히스토그램", "🔗 산점도", "📌 Pairplot"])

    with tab1:
        st.header("📊 히스토그램")
        eda.plot_histograms(selected_data)

    with tab2:
        st.header("🔗 산점도")
        numeric_cols = selected_data.select_dtypes(include='number').columns.tolist()
        if len(numeric_cols) >= 2:
            x_col = st.selectbox("X축 열", numeric_cols, key="x_col")
            y_col = st.selectbox("Y축 열", numeric_cols, key="y_col")
            if x_col and y_col:
                eda.plot_scatter(selected_data, x_col, y_col)
        else:
            st.warning("수치형 열이 2개 이상 있어야 산점도를 그릴 수 있어요!")

    with tab3:
        st.header("📌 Pairplot")
        if len(selected_cols) > 5:
            st.warning("Pairplot은 열 5개 이하 권장!")
        else:
            eda.plot_pairplot(selected_data)

else:
    st.info("하나 이상의 열을 선택해주세요.")
