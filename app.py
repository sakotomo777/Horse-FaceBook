import streamlit as st
import pandas as pd
import os

st.set_page_config(layout="wide")

st.markdown("""
<style>
div[data-testid="stVerticalBlock"] > div:has(.sticky-header) {
    position: sticky;
    top: 0;
    background-color: white;
    z-index: 999;
    padding-top: 10px;
    padding-bottom: 10px;
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

st.title("馬選択")

# --- 五十音グループ ---
groups = {
    "ア": ("ア","イ","ウ","ヴ","エ","オ"),
    "カ": ("カ","キ","ク","ケ","コ","ガ","ギ","グ","ゲ","ゴ"),
    "サ": ("サ","シ","ス","セ","ソ","ザ","ジ","ズ","ゼ","ゾ"),
    "タ": ("タ","チ","ツ","テ","ト","ダ","ヂ","ヅ","デ","ド"),
    "ナ": ("ナ","ニ","ヌ","ネ","ノ"),
    "ハ": ("ハ","ヒ","フ","ヘ","ホ","バ","ビ","ブ","ベ","ボ","パ","ピ","プ","ペ","ポ"),
    "マ": ("マ","ミ","ム","メ","モ"),
    "ヤラワ": ("ヤ","ユ","ヨ","ラ","リ","ル","レ","ロ","ワ")
}


# セッションに選択状態を保存
if "selected_group" not in st.session_state:
    st.session_state.selected_group = "ア"

if "selected_horse" not in st.session_state:
    st.session_state.selected_horse = None

# ---五十音ボタン ---
st.markdown('<div class="sticky-header">', unsafe_allow_html=True)

keys = list(groups.keys())

row1 = st.columns(4)
row2 = st.columns(4)

for i in range(4):
    if row1[i].button(keys[i], use_container_width=True):
        st.session_state.selected_group = keys[i]

for i in range(4, len(keys)):
    if row2[i-4].button(keys[i], use_container_width=True):
        st.session_state.selected_group = keys[i]

st.markdown('</div>', unsafe_allow_html=True)

# ---馬名一覧 ---
selected_chars = groups[st.session_state.selected_group]

filtered = df[df["馬名"].astype(str).str.startswith(selected_chars)]

st.subheader(f"{st.session_state.selected_group} 行")

# 2列表示
cols = st.columns(2)

for i, (_, row) in enumerate(filtered.iterrows()):
    col = cols[i % 2]
    
    # --- 画像表示 ---
    if col.button(row["馬名"], use_container_width=True):
        st.session_state.selected_horse = row["馬名"]
        show_image(row["馬名"])
