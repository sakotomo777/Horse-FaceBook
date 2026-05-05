import streamlit as st
import pandas as pd
import os

st.set_page_config(layout="wide")

# --- データ ---
df = pd.read_excel("馬情報.xlsx").fillna("")

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

if "search_mode" not in st.session_state:
    st.session_state.search_mode = "kana"

# --- 行選択 ---
st.markdown("<br>", unsafe_allow_html=True)

st.selectbox(
    "馬名から選ぶ場合はこっち",
    list(groups.keys()),
    key="selected_group"
)

# 行を変えたら五十音検索に戻す
st.session_state.search_mode = "kana"

# --- 条件 ---
st.write("白い個所をチェック")

head = st.checkbox("頭")
right_front = st.checkbox("右前")
left_front = st.checkbox("左前")
right_back = st.checkbox("右後")
left_back = st.checkbox("左後")

color = st.selectbox("見た目の毛色", ["選択なし", "鹿", "黒", "芦"])

search_clicked = st.button("検索", use_container_width=True)

if search_clicked:
    st.session_state.search_mode = "condition"
    st.session_state.selected_horse = None

st.markdown("<br>", unsafe_allow_html=True)

# --- 馬リスト ---
if st.session_state.search_mode == "condition":

    filtered = df.copy()

    # 毛色
    if color != "選択なし":
        filtered = filtered[filtered["毛色"] == color]
    # チェック状態を辞書化
    conditions = {
        "額": head,
        "右前": right_front,
        "左前": left_front,
        "右後": right_back,
        "左後": left_back
    }

    for col, is_checked in conditions.items():
        if is_checked:
            filtered = filtered[filtered[col] == "○"]
        else:
            filtered = filtered[filtered[col] != "○"]
else:
    selected_chars = groups[st.session_state.selected_group]
    filtered = df[df["馬名"].astype(str).str.startswith(selected_chars)]
    filtered = filtered.sort_values("馬名")

# --- 表示 ---
if filtered.empty:
    st.warning("該当する馬がいません")
else:
    for horse in filtered["馬名"]:
        if st.button(horse, use_container_width=True):
            st.session_state.selected_horse = horse
            show_image(horse)