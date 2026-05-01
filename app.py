import streamlit as st
import pandas as pd
import os

st.set_page_config(layout="wide")

# --- データ ---
df = pd.read_excel("馬情報.xlsx").fillna("")

# --- 最低限のCSSだけ ---
st.markdown("""
<style>
.block-container {
    padding-top: 0.5rem;
}

div[data-testid="stButton"] > button {
    font-size: 12px;
    padding: 4px 6px;
}

div[data-testid="stSelectbox"] {
    font-size: 12px;
}

div[data-testid="stCheckbox"] label {
    font-size: 12px;
}
</style>
""", unsafe_allow_html=True)

# --- 画像表示 ---
@st.dialog(" ", width="large")
def show_image(name):
    path = f"images/{name}.jpg"
    if os.path.exists(path):
        st.image(path, use_container_width=True)
    else:
        st.warning("画像が見つかりません")

# --- グループ ---
groups = {
    "ア行": ("ア","イ","ウ","ヴ","エ","オ"),
    "カ行": ("カ","キ","ク","ケ","コ","ガ","ギ","グ","ゲ","ゴ"),
    "サ行": ("サ","シ","ス","セ","ソ","ザ","ジ","ズ","ゼ","ゾ"),
    "タ行": ("タ","チ","ツ","テ","ト","ダ","ヂ","ヅ","デ","ド"),
    "ナ行": ("ナ","ニ","ヌ","ネ","ノ"),
    "ハ行": ("ハ","ヒ","フ","ヘ","ホ","バ","ビ","ブ","ベ","ボ","パ","ピ","プ","ペ","ポ"),
    "マ行": ("マ","ミ","ム","メ","モ"),
    "ヤラワ行": ("ヤ","ユ","ヨ","ラ","リ","ル","レ","ロ","ワ"),
}

# --- 状態 ---
if "selected_group" not in st.session_state:
    st.session_state.selected_group = "ア行"

if "selected_horse" not in st.session_state:
    st.session_state.selected_horse = None

# --- 行選択 ---
st.selectbox("行を選択", list(groups.keys()), key="selected_group")

# --- 条件 ---
head = st.checkbox("頭")
right_front = st.checkbox("右前")
left_front = st.checkbox("左前")
right_back = st.checkbox("右後")
left_back = st.checkbox("左後")

color = st.selectbox("毛色", ["選択なし", "鹿", "黒", "芦"])
search_clicked = st.button("検索", use_container_width=True)

# --- 馬リスト ---
selected_chars = groups[st.session_state.selected_group]
filtered = df[df["馬名"].astype(str).str.startswith(selected_chars)]

for horse in filtered["馬名"]:
    if st.button(horse, use_container_width=True):
        st.session_state.selected_horse = horse
        show_image(horse)