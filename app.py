import streamlit as st
import pandas as pd
import os

st.set_page_config(layout="wide")

st.title("馬選択")

df = pd.read_excel("実験馬選択.xlsx")
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


# セッションに選択状態を保存
if "selected_group" not in st.session_state:
    st.session_state.selected_group = "ア"

if "selected_horse" not in st.session_state:
    st.session_state.selected_horse = None

# --- レイアウト ---
left, right = st.columns([1, 4])

# --- 左：五十音ボタン ---
with left:
    for key in groups.keys():
        if st.button(key, use_container_width=True):
            st.session_state.selected_group = key
            st.session_state.selected_horse = None

# --- 右：馬名一覧 ---
with right:

    selected_chars = groups[st.session_state.selected_group]

    filtered = df[df["馬名"].astype(str).str.startswith(selected_chars)]

    st.subheader(f"{st.session_state.selected_group} 行")

    # 2列表示
    cols = st.columns(2)

    for i, (_, row) in enumerate(filtered.iterrows()):
        col = cols[i % 2]

        if col.button(row["馬名"], use_container_width=True):
            st.session_state.selected_horse = row["馬名"]

    # --- 画像表示 ---
    if st.session_state.selected_horse:
        st.divider()
        st.markdown(f"## {st.session_state.selected_horse}")

        image_path = f"images/{st.session_state.selected_horse}.jpg"

        if os.path.exists(image_path):
            st.image(image_path, use_container_width=True)
        else:
            st.warning("画像が見つかりません")
