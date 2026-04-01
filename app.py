import streamlit as st
import pandas as pd
import os

st.set_page_config(layout="wide")

#ラジオボタンの〇消す
st.markdown("""
<style>
div[role="radiogroup"] label > div:first-child {
    display: none;
}
</style>
""", unsafe_allow_html=True)


df = pd.read_excel("実験馬選択.xlsx")
df = df.fillna("")

@st.dialog(" ", width="large")
def show_image(name):
    image_path = f"images/{name}.jpg"
    if os.path.exists(image_path):
        st.image(image_path, use_container_width=True)

# --- 五十音グループ ---
groups = {
    "ア行": ("ア","イ","ウ","ヴ","エ","オ"),
    "カ行": ("カ","キ","ク","ケ","コ","ガ","ギ","グ","ゲ","ゴ"),
    "サ行": ("サ","シ","ス","セ","ソ","ザ","ジ","ズ","ゼ","ゾ"),
    "タ行": ("タ","チ","ツ","テ","ト","ダ","ヂ","ヅ","デ","ド"),
    "ナ行": ("ナ","ニ","ヌ","ネ","ノ"),
    "ハ行": ("ハ","ヒ","フ","ヘ","ホ","バ","ビ","ブ","ベ","ボ","パ","ピ","プ","ペ","ポ"),
    "マ行": ("マ","ミ","ム","メ","モ"),
    "ヤラワ行": ("ヤ","ユ","ヨ","ラ","リ","ル","レ","ロ","ワ")
}

# セッションに選択状態を保存
if "selected_group" not in st.session_state:
    st.session_state.selected_group = "ア行"

if "selected_horse" not in st.session_state:
    st.session_state.selected_horse = None

#　画面レイアウト
col1, col2 = st.columns([2,1])

with col1:
    st.title("行選択")

with col2:
    selected_group = st.selectbox(
        "行",
        list(groups.keys()),
        index=list(groups.keys()).index(st.session_state.selected_group),
        label_visibility="collapsed"
    )

st.session_state.selected_group = selected_group

# ---馬名一覧 ---
selected_chars = groups[st.session_state.selected_group]

filtered = df[df["馬名"].astype(str).str.startswith(selected_chars)]

horse_list = filtered["馬名"].tolist()

horse = st.radio(
    "🐎 馬を選択",
    horse_list,
    key="horse_radio"
)

# 初期化
if "last_horse" not in st.session_state:
    st.session_state.last_horse = None

if "prev_group" not in st.session_state:
    st.session_state.prev_group = st.session_state.selected_group

# 行変更時はリセット
if st.session_state.prev_group != st.session_state.selected_group:
    st.session_state.last_horse = None
    st.session_state.prev_group = st.session_state.selected_group

if horse and horse != st.session_state.last_horse:
    show_image(horse)
    st.session_state.last_horse = horse

# 常に保存
st.session_state.selected_horse = horse
