import streamlit as st
import pandas as pd
import os

st.set_page_config(layout="wide")

df = pd.read_excel("実験馬選択.xlsx")
df = df.fillna("")

@st.dialog(" ", width="large")
def show_image(name):
    image_path = f"images/{name}.jpg"
    if os.path.exists(image_path):
        st.image(image_path, use_container_width=True)
    else:
        st.warning("画像が見つかりません")

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

# --- セッション初期化 ---
if "selected_group" not in st.session_state:
    st.session_state.selected_group = "ア行"

if "selected_horse" not in st.session_state:
    st.session_state.selected_horse = None

if "last_group" not in st.session_state:
    st.session_state.last_group = st.session_state.selected_group

# --- 行選択 ---
selected_group = st.selectbox(
    "行を選択",
    list(groups.keys()),
    index=list(groups.keys()).index(st.session_state.selected_group)
)

# 行変更時リセット
if selected_group != st.session_state.last_group:
    st.session_state.selected_horse = None
    st.session_state.last_group = selected_group

st.session_state.selected_group = selected_group

# --- 馬名抽出 ---
selected_chars = groups[st.session_state.selected_group]
filtered = df[df["馬名"].astype(str).str.startswith(selected_chars)]
horse_list = filtered["馬名"].tolist()

st.subheader("🐎 馬を選択")

# --- radio（ここがポイント） ---
if horse_list:
    selected_horse = st.radio(
        "",
        horse_list,
        index=horse_list.index(st.session_state.selected_horse)
        if st.session_state.selected_horse in horse_list else 0
    )

    # 前回と違うときだけ表示
    if selected_horse != st.session_state.selected_horse:
        st.session_state.selected_horse = selected_horse
        show_image(selected_horse)

else:
    st.write("該当する馬がいません")
    st.session_state.selected_horse = None
