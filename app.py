import streamlit as st
import pandas as pd
import os

st.set_page_config(layout="wide")

df = pd.read_excel("馬情報.xlsx")
df = df.fillna("")

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
}
</style>
""", unsafe_allow_html=True)

# 余白を削る
st.markdown("""
<style>
.block-container {
    padding-top: 0.2rem !important;
}
</style>
""", unsafe_allow_html=True)

# 画像表示
@st.dialog(" ", width="large")
def show_image(name):
    image_path = f"images/{name}.jpg"
    if os.path.exists(image_path):
        st.image(image_path, use_container_width=True)
    else:
        st.warning("画像が見つかりません")

# スマホでも columns を横並びにする
st.markdown("""
<style>
@media (max-width: 768px) {
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
</style>
""", unsafe_allow_html=True)

# チェックボックスのラベルを消す
st.markdown("""
<style>
div[data-testid="stCheckbox"] label p {
    display: none;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* チェックボックスを画像側に寄せる */
div[data-testid="stCheckbox"] {
    margin-bottom: -10px;
}

/* 左側のチェックを右に寄せる */
div[data-testid="stHorizontalBlock"] > div:nth-child(1) div[data-testid="stCheckbox"] {
    margin-right: -10px;
}

/* 右側のチェックを左に寄せる */
div[data-testid="stHorizontalBlock"] > div:nth-child(3) div[data-testid="stCheckbox"] {
    margin-left: -10px;
}
</style>
""", unsafe_allow_html=True)

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

if "prev_group" not in st.session_state:
    st.session_state.prev_group = st.session_state.selected_group

st.selectbox(
    "行を選択",
    list(groups.keys()),
    key="selected_group"
)
#選択画像
import base64
from pathlib import Path

img_path = Path("images/horse-image.png")
img_base64 = base64.b64encode(img_path.read_bytes()).decode()

# CSS
st.markdown("""
<style>
.horse-wrapper {
    position: relative;
    width: 150px;
    height: 190px;
}

/* 画像 */
.horse-img {
    position: absolute;
    top: 0;
    left: 0;
    width: 150px;
}

/* checkboxを入れる枠 */
.cb-box {
    position: absolute;
}

/* 各位置 */
.cb-right-back { top: 10px; left: 30px; }
.cb-left-back  { top: 10px; left: 105px; }

.cb-right-front { top: 110px; left: 5px; }
.cb-left-front  { top: 110px; left: 130px; }

.cb-head { top: 165px; left: 70px; }
</style>
""", unsafe_allow_html=True)

left_area, button_area = st.columns([1, 2])

with left_area:
    # 枠を作る
    st.markdown(f"""
    <div class="horse-wrapper">
        <img class="horse-img" src="data:image/png;base64,{img_base64}">
    </div>
    """, unsafe_allow_html=True)

    # 各checkboxを“枠付きで”配置
    def place_cb(cls, key):
        st.markdown(f'<div class="cb-box {cls}">', unsafe_allow_html=True)
        val = st.checkbox("", key=key)
        st.markdown('</div>', unsafe_allow_html=True)
        return val

    right_back = place_cb("cb-right-back", "right_back")
    left_back  = place_cb("cb-left-back", "left_back")
    right_front = place_cb("cb-right-front", "right_front")
    left_front  = place_cb("cb-left-front", "left_front")
    head        = place_cb("cb-head", "head")

with button_area:
    st.button("登録", use_container_width=True)
    st.button("クリア", use_container_width=True)

# 行が変わったら馬選択をリセット
if st.session_state.selected_group != st.session_state.prev_group:
    st.session_state.selected_horse = None
    st.session_state.prev_group = st.session_state.selected_group

selected_chars = groups[st.session_state.selected_group]
filtered = df[df["馬名"].astype(str).str.startswith(selected_chars)]
horse_list = filtered["馬名"].tolist()

for horse in horse_list:
    label = f"✓ {horse}" if horse == st.session_state.selected_horse else horse
    if st.button(label, key=f"horse_{horse}", use_container_width=True):
        st.session_state.selected_horse = horse
        show_image(horse)
