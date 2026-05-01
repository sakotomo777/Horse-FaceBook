import streamlit as st
import pandas as pd
import os

st.set_page_config(layout="wide")

# --- データ読み込み ---
df = pd.read_excel("馬情報.xlsx")
df = df.fillna("")

# --- スマホ表示の調整 ---
st.markdown("""
<style>
@media (max-width: 768px) {
    div[data-testid="stButton"] {
        margin-bottom: 2px !important;
    }

    div[data-testid="stButton"] > button {
        padding: 3px 4px !important;
        font-size: 12px !important;
        min-height: 30px !important;
    }

    div[data-testid="element-container"] {
        margin-bottom: 2px !important;
    }

    div[data-testid="stHorizontalBlock"] {
        flex-wrap: nowrap !important;
        gap: 8px !important;
    }

    div[data-testid="column"] {
        min-width: 0 !important;
        width: auto !important;
        flex: unset !important;
    }
}

.block-container {
    padding-top: 0.2rem !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
div[data-testid="stSelectbox"] {
    font-size: 12px;
}
div[data-testid="stButton"] > button {
    padding: 4px 6px;
    font-size: 12px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
div[data-testid="stCheckbox"] label {
    font-size: 12px;
}
</style>
""", unsafe_allow_html=True)


# --- 画像表示 ---
@st.dialog(" ", width="large")
def show_image(name):
    image_path = f"images/{name}.jpg"

    if os.path.exists(image_path):
        st.image(image_path, use_container_width=True)
    else:
        st.warning("画像が見つかりません")

# --- 五十音グループ ---
groups = {
    "ア行": ("ア", "イ", "ウ", "ヴ", "エ", "オ"),
    "カ行": ("カ", "キ", "ク", "ケ", "コ", "ガ", "ギ", "グ", "ゲ", "ゴ"),
    "サ行": ("サ", "シ", "ス", "セ", "ソ", "ザ", "ジ", "ズ", "ゼ", "ゾ"),
    "タ行": ("タ", "チ", "ツ", "テ", "ト", "ダ", "ヂ", "ヅ", "デ", "ド"),
    "ナ行": ("ナ", "ニ", "ヌ", "ネ", "ノ"),
    "ハ行": ("ハ", "ヒ", "フ", "ヘ", "ホ", "バ", "ビ", "ブ", "ベ", "ボ", "パ", "ピ", "プ", "ペ", "ポ"),
    "マ行": ("マ", "ミ", "ム", "メ", "モ"),
    "ヤラワ行": ("ヤ", "ユ", "ヨ", "ラ", "リ", "ル", "レ", "ロ", "ワ"),
}

# --- 選択状態 ---
if "selected_group" not in st.session_state:
    st.session_state.selected_group = "ア行"

if "selected_horse" not in st.session_state:
    st.session_state.selected_horse = None

if "prev_group" not in st.session_state:
    st.session_state.prev_group = st.session_state.selected_group

# --- 行選択 ---
st.selectbox(
    "行を選択",
    list(groups.keys()),
    key="selected_group"
)
# --- 条件エリア ---
head = st.checkbox("頭")
right_front = st.checkbox("右前")
left_front = st.checkbox("左前")
right_back = st.checkbox("右後")
left_back = st.checkbox("左後")

color = st.selectbox("毛色", ["選択なし", "鹿", "黒", "芦"])

search_clicked = st.button("検索", use_container_width=True)

# 行が変わったら馬選択をリセット
if st.session_state.selected_group != st.session_state.prev_group:
    st.session_state.selected_horse = None
    st.session_state.prev_group = st.session_state.selected_group

# --- 馬名一覧 ---
selected_chars = groups[st.session_state.selected_group]
filtered = df[df["馬名"].astype(str).str.startswith(selected_chars)]
horse_list = filtered["馬名"].tolist()

for horse in horse_list:
    label = f"✓ {horse}" if horse == st.session_state.selected_horse else horse

    if st.button(label, key=f"horse_{horse}", use_container_width=True):
        st.session_state.selected_horse = horse
        show_image(horse)
