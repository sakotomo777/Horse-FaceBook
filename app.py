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

# セッション初期化
if "selected_group" not in st.session_state:
    st.session_state.selected_group = "ア行"

if "selected_horse" not in st.session_state:
    st.session_state.selected_horse = None

if "last_group" not in st.session_state:
    st.session_state.last_group = st.session_state.selected_group

# --- 画面レイアウト ---
col1, col2 = st.columns([1, 2])

with col1:
    selected_group = st.selectbox(
        "行",
        list(groups.keys()),
        index=list(groups.keys()).index(st.session_state.selected_group)
    )

# 行が変わったら馬選択をリセット
if selected_group != st.session_state.last_group:
    st.session_state.selected_horse = None
    st.session_state.last_group = selected_group

st.session_state.selected_group = selected_group

# --- 馬名一覧 ---
selected_chars = groups[st.session_state.selected_group]
filtered = df[df["馬名"].astype(str).str.startswith(selected_chars)]
horse_list = filtered["馬名"].tolist()

with col2:
    if horse_list:
        selected_horse = st.selectbox(
            "馬名",
            options=["選択してください"] + horse_list,
            index=0 if st.session_state.selected_horse is None else (
                horse_list.index(st.session_state.selected_horse) + 1
                if st.session_state.selected_horse in horse_list else 0
            )
        )

        if selected_horse == "選択してください":
            st.session_state.selected_horse = None
        else:
            st.session_state.selected_horse = selected_horse
    else:
        st.selectbox("馬名", ["該当なし"], index=0)
        st.session_state.selected_horse = None

# --- 画像表示 ---
if st.session_state.selected_horse:
    show_image(st.session_state.selected_horse)
