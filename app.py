import streamlit as st
import pandas as pd
import os

st.set_page_config(layout="wide")

df = pd.read_excel("実験馬選択.xlsx")
df = df.fillna("")

st.markdown("""
<style>
/* iPhoneなどの狭い画面でも2列を維持 */
@media (max-width: 768px) {
    div[data-testid="stHorizontalBlock"] {
        flex-wrap: nowrap !important;
        gap: 0.4rem !important;
    }

    div[data-testid="column"] {
        min-width: 0 !important;
        flex: 1 1 0 !important;
    }

    div[data-testid="stButton"] > button {
        width: 100% !important;
        font-size: 13px !important;
        padding: 0.4rem 0.3rem !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }
}
</style>
""", unsafe_allow_html=True)

#ボタン小さく
st.markdown("""
<style>
@media (max-width: 768px) {
    div[data-testid="stHorizontalBlock"] {
        flex-wrap: nowrap !important;
        gap: 0.25rem !important;
    }

    div[data-testid="column"] {
        min-width: 0 !important;
        flex: 1 1 0 !important;
        padding: 0 !important;
    }

    div[data-testid="stButton"] {
        width: 100% !important;
    }

    div[data-testid="stButton"] > button {
        width: 100% !important;
        min-height: 32px !important;
        height: 32px !important;
        font-size: 11px !important;
        padding: 0 4px !important;
        line-height: 1 !important;
        border-radius: 6px !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }
}
</style>
""", unsafe_allow_html=True)


@st.dialog(" ", width="large")
def show_image(name):
    image_path = f"images/{name}.jpg"
    if os.path.exists(image_path):
        st.image(image_path, use_container_width=True)
    else:
        st.warning("画像が見つかりません")

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

if "selected_group" not in st.session_state:
    st.session_state.selected_group = "ア行"

if "selected_horse" not in st.session_state:
    st.session_state.selected_horse = None

selected_group = st.selectbox(
    "行を選択",
    list(groups.keys()),
    index=list(groups.keys()).index(st.session_state.selected_group)
)

st.session_state.selected_group = selected_group

selected_chars = groups[st.session_state.selected_group]
filtered = df[df["馬名"].astype(str).str.startswith(selected_chars)]
horse_list = filtered["馬名"].tolist()

st.write("### 馬名を選択")

cols = st.columns(2, gap="small")

for i, horse in enumerate(horse_list):
    with cols[i % 2]:
        label = horse
        if horse == st.session_state.selected_horse:
            label = f"✓ {horse}"

        if st.button(label, key=f"horse_{horse}", use_container_width=True):
            st.session_state.selected_horse = horse
            show_image(horse)
