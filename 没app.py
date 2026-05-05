import streamlit as st
import pandas as pd
import os

st.set_page_config(layout="wide")

st.title("馬選択")

df = pd.read_excel("馬情報.xlsx")
df = df.fillna("")

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

# --- セッション初期化 ---
if "selected_group" not in st.session_state:
    st.session_state.selected_group = "ア"

if "selected_horse" not in st.session_state:
    st.session_state.selected_horse = None

if "search_mode" not in st.session_state:
    st.session_state.search_mode = "kana"

# チェック状態
parts = ["head", "right_front", "left_front", "right_back", "left_back"]

for p in parts:
    if p not in st.session_state:
        st.session_state[p] = False

# --- レイアウト ---
left, right = st.columns([1, 4])

# --- 左：五十音ボタン ---
with left:
    for key in groups.keys():
        if st.button(key, use_container_width=True):
            st.session_state.selected_group = key
            st.session_state.selected_horse = None
            st.session_state.search_mode = "kana"

# --- 右側 ---
with right:

    # --- 条件検索エリア ---
    st.markdown("### 条件検索")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.checkbox("額", key="head")

    with col2:
        st.checkbox("右前", key="right_front")

    with col3:
        st.checkbox("左前", key="left_front")

    with col4:
        st.checkbox("右後", key="right_back")

    with col5:
        st.checkbox("左後", key="left_back")

    color = st.selectbox(
        "見た目の毛色",
        ["選択なし", "鹿", "黒", "芦"]
    )

    if st.button("検索"):
        st.session_state.search_mode = "condition"
        st.session_state.selected_horse = None

    st.divider()

    # --- 表示する馬を決める ---
    if st.session_state.search_mode == "condition":

        filtered = df.copy()

        # 毛色
        if color != "選択なし":
            filtered = filtered[filtered["毛色"] == color]

        # チェック項目
        if st.session_state.head:
            filtered = filtered[filtered["額"] == "○"]

        if st.session_state.right_front:
            filtered = filtered[filtered["右前"] == "○"]

        if st.session_state.left_front:
            filtered = filtered[filtered["左前"] == "○"]

        if st.session_state.right_back:
            filtered = filtered[filtered["右後"] == "○"]

        if st.session_state.left_back:
            filtered = filtered[filtered["左後"] == "○"]

        filtered = filtered.sort_values("馬名")

        st.subheader("検索結果")

    else:
        selected_chars = groups[st.session_state.selected_group]
        filtered = df[df["馬名"].astype(str).str.startswith(selected_chars)]
        filtered = filtered.sort_values("馬名")

        st.subheader(f"{st.session_state.selected_group} 行")

    # --- 馬名一覧：2列表示 ---
    cols = st.columns(2)

    for i, (_, row) in enumerate(filtered.iterrows()):
        col = cols[i % 2]

        if col.button(row["馬名"], use_container_width=True):
            st.session_state.selected_horse = row["馬名"]

    # --- 該当なし ---
    if filtered.empty:
        st.warning("該当する馬がいません")

    # --- 画像表示 ---
    if st.session_state.selected_horse:
        st.divider()
        st.markdown(f"## {st.session_state.selected_horse}")

        image_path = f"images/{st.session_state.selected_horse}.jpg"

        if os.path.exists(image_path):
            st.image(image_path, use_container_width=True)
        else:
            st.warning("画像が見つかりません")