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

# --- 画像をbase64化 ---
img_path = Path("images/horse-image.png")
img_base64 = base64.b64encode(img_path.read_bytes()).decode()

# --- CSS ---
st.markdown("""
<style>
.horse-container {
    position: relative;
    width: 150px;
    margin: auto;
}

.horse-container img {
    width: 150px;
}

/* チェックボックス共通 */
.horse-check {
    position: absolute;
    transform: scale(0.9);
}

/* 位置調整（ここが重要） */
.cb-right-back { top: 10px; left: 30px; }
.cb-left-back  { top: 10px; left: 105px; }

.cb-right-front { top: 110px; left: 5px; }
.cb-left-front  { top: 110px; left: 135px; }

.cb-head { top: 165px; left: 70px; }
</style>
""", unsafe_allow_html=True)

# --- レイアウト ---
left_area, button_area = st.columns([1, 2], gap="small")

with left_area:
    st.markdown(f"""
    <div class="horse-container">
        <img src="data:image/png;base64,{img_base64}">
    </div>
    """, unsafe_allow_html=True)

    # ↓ ここが重要：checkboxは別に置く
    st.markdown('<div class="horse-check cb-right-back">', unsafe_allow_html=True)
    right_back = st.checkbox("", key="right_back")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="horse-check cb-left-back">', unsafe_allow_html=True)
    left_back = st.checkbox("", key="left_back")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="horse-check cb-right-front">', unsafe_allow_html=True)
    right_front = st.checkbox("", key="right_front")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="horse-check cb-left-front">', unsafe_allow_html=True)
    left_front = st.checkbox("", key="left_front")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="horse-check cb-head">', unsafe_allow_html=True)
    head = st.checkbox("", key="head")
    st.markdown('</div>', unsafe_allow_html=True)

with button_area:
    st.button("登録", use_container_width=True)
    st.button("クリア", use_container_width=True)

# --- 取得結果 ---
checked = []
if head: checked.append("頭")
if right_front: checked.append("右前")
if left_front: checked.append("左前")
if right_back: checked.append("右後")
if left_back: checked.append("左後")

st.write("チェック:", checked)

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
