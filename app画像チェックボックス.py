import streamlit as st
import pandas as pd
import os
from streamlit_image_coordinates import streamlit_image_coordinates
from PIL import Image, ImageDraw

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
# --- チェック状態の初期化 ---
parts = ["right_back", "left_back", "right_front", "left_front", "head"]

for p in parts:
    if p not in st.session_state:
        st.session_state[p] = False

# --- 画像読み込み ---
img = Image.open("images/horse-image.png").convert("RGBA")
img = img.resize((150, 190))

draw = ImageDraw.Draw(img)

# チェック位置
boxes = {
    "right_back":  (35, 15),
    "left_back":   (105, 15),
    "right_front": (10, 110),
    "left_front":  (130, 110),
    "head":        (70, 165),
}

box_size = 14

# □を画像に描く
for key, (x, y) in boxes.items():
    draw.rectangle(
        [x, y, x + box_size, y + box_size],
        outline="black",
        width=2
    )

    # チェック済みなら✓を描く
    if st.session_state[key]:
        draw.line([x + 3, y + 7, x + 6, y + 11, x + 12, y + 3], fill="black", width=2)

# --- 画像クリック取得 ---
clicked = streamlit_image_coordinates(
    img,
    key="horse_check_image"
)

# --- クリック位置判定 ---
if clicked:
    cx = clicked["x"]
    cy = clicked["y"]

    for key, (x, y) in boxes.items():
        if x <= cx <= x + box_size and y <= cy <= y + box_size:
            st.session_state[key] = not st.session_state[key]
            st.rerun()

# --- チェック結果 ---
checked = []

if st.session_state["right_back"]:
    checked.append("右後")
if st.session_state["left_back"]:
    checked.append("左後")
if st.session_state["right_front"]:
    checked.append("右前")
if st.session_state["left_front"]:
    checked.append("左前")
if st.session_state["head"]:
    checked.append("頭")

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
