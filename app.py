import streamlit as st
import itertools
import pandas as pd

st.set_page_config(page_title="OddsDistortion Lab", layout="wide")

st.title("🏇 OddsDistortion Lab")
st.caption("オッズ歪み検知 + 人気飛び確率AI")

# -----------------------------
# サイドバー入力
# -----------------------------

st.sidebar.header("オッズ入力")

win = st.sidebar.number_input("単勝", 0.1, value=2.0)
quinella = st.sidebar.number_input("馬連", 0.1, value=4.0)
exacta = st.sidebar.number_input("馬単", 0.1, value=8.0)
trio = st.sidebar.number_input("3連複", 0.1, value=12.0)
trifecta = st.sidebar.number_input("3連単", 0.1, value=25.0)

st.sidebar.header("記事評価")

sentiment = st.sidebar.selectbox(
    "メディア評価",
    ["絶賛（死角なし）", "普通", "不安あり"]
)

st.sidebar.header("馬番入力")

horse_input = st.sidebar.text_input(
    "人気1〜10位",
    "1,2,3,4,5,6,7,8,9,10"
)

# -----------------------------
# 馬番処理
# -----------------------------

horses = [h.strip() for h in horse_input.split(",") if h.strip()]

if len(horses) < 5:
    st.error("最低5頭入力してください")
    st.stop()

if len(set(horses)) != len(horses):
    st.error("馬番が重複しています")
    st.stop()

# -----------------------------
# 印
# -----------------------------

st.sidebar.header("予想印")

honmei = st.sidebar.selectbox("◎ 本命", horses, index=0)
taiko = st.sidebar.selectbox("○ 対抗", horses, index=1)
tansho = st.sidebar.selectbox("▲ 単穴", horses, index=2)
renka = st.sidebar.selectbox("△ 連下", horses, index=3)
ana = st.sidebar.selectbox("× 穴", horses, index=4)

marks = {
    "◎": honmei,
    "○": taiko,
    "▲": tansho,
    "△": renka,
    "×": ana
}

# -----------------------------
# 歪み計算
# -----------------------------

distortion = (
    quinella / win +
    exacta / quinella +
    trio / exacta +
    trifecta / trio
)

# -----------------------------
# スコア
# -----------------------------

score = 0

if win >= 2:
    score += 1

if quinella >= 7:
    score += 1

if exacta >= 15:
    score += 1

if trio >= 15:
    score += 1

if trifecta >= 30:
    score += 1

if sentiment == "絶賛（死角なし）":
    score += 1

# -----------------------------
# レース評価
# -----------------------------

if score == 0:
    status = "鉄板レース"
    comment = "本命信頼度高"

elif score <= 2:
    status = "標準レース"
    comment = "平均的"

elif score <= 4:
    status = "波乱レース"
    comment = "本命注意"

else:
    status = "崩壊レース"
    comment = "人気崩壊警戒"

# -----------------------------
# 人気飛び確率
# -----------------------------

prob_table = {
    0:15,
    1:25,
    2:40,
    3:55,
    4:70,
    5:85,
    6:90
}

collapse_prob = prob_table.get(score,90)

# -----------------------------
# 表示
# -----------------------------

st.subheader("AI解析")

col1,col2,col3 = st.columns(3)

with col1:
    st.metric("レース判定", status)

with col2:
    st.metric("オッズ歪み", round(distortion,2))

with col3:
    st.metric("1番人気飛び確率", f"{collapse_prob}%")

st.caption("歪み = (馬連/単勝)+(馬単/馬連)+(3連複/馬単)+(3連単/3連複)")

# -----------------------------
# 買い目生成
# -----------------------------

if st.button("買い目生成"):

    ana_set = [marks["○"],marks["▲"],marks["△"],marks["×"]]

    used = set(marks.values())

    unmarked = [h for h in horses if h not in used]

    g_bd = [marks["△"],marks["×"]] + unmarked

    g_bd = list(set(g_bd) - {honmei})

    A = list(itertools.combinations(ana_set,3))
    B = [tuple(sorted((honmei,p[0],p[1]))) for p in itertools.combinations(g_bd,2)]
    C = list(itertools.combinations(ana_set,2))
    D = [(honmei,o) for o in g_bd]

    st.divider()

    c1,c2 = st.columns(2)

    with c1:

        st.subheader(f"A:3連複BOX ({len(A)})")
        st.code("\n".join([f"{a[0]}-{a[1]}-{a[2]}" for a in A]))

        st.subheader(f"C:馬連BOX ({len(C)})")
        st.code("\n".join([f"{a[0]}-{a[1]}" for a in C]))

    with c2:

        st.subheader(f"B:3連複軸 ({len(B)})")
        st.code("\n".join([f"{a[0]}-{a[1]}-{a[2]}" for a in B]))

        st.subheader(f"D:馬連軸 ({len(D)})")
        st.code("\n".join([f"{a[0]}-{a[1]}" for a in D]))
