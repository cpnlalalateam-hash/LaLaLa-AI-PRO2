import streamlit as st
import itertools

# =========================
# ページ設定
# =========================

st.set_page_config(page_title="LaLaLa式・裏読みAI 8頭版", layout="wide")

st.title("🏇 LaLaLa式・裏読みAI【8頭版】")
st.caption("逆張り思想ベースの競馬分析ツール")

# =========================
# サイドバー入力
# =========================

st.sidebar.header("① 5大オッズ（1番人気）")

win = st.sidebar.number_input("単勝", value=1.5, step=0.1)
quinella = st.sidebar.number_input("馬連", value=3.5, step=0.1)
exacta = st.sidebar.number_input("馬単", value=7.0, step=0.1)
trio = st.sidebar.number_input("3連複", value=8.0, step=0.1)
trifecta = st.sidebar.number_input("3連単", value=15.0, step=1.0)

st.sidebar.header("② 1番人気の評判")

sentiment = st.sidebar.selectbox(
    "記事トーン",
    ["絶賛（死角なし）", "普通（一長一短）", "不安（疑問あり）"]
)

st.sidebar.header("③ 馬番入力（最大8頭）")

horse_input = st.sidebar.text_input(
    "カンマ区切り",
    "1,2,3,4,5,6,7,8"
)

horses = [h.strip() for h in horse_input.split(",") if h.strip() != ""]

# =========================
# バリデーション
# =========================

if len(horses) < 5:
    st.error("⚠ 馬は最低5頭必要です")
    st.stop()

if len(horses) > 8:
    st.error("⚠ 8頭までにしてください")
    st.stop()

if len(set(horses)) != len(horses):
    st.error("⚠ 馬番が重複しています")
    st.stop()

# =========================
# 印入力
# =========================

st.sidebar.header("④ 直感印")

m1 = st.sidebar.selectbox("◎ 本命", horses, index=0)
m2 = st.sidebar.selectbox("○ 対抗", horses, index=1)
m3 = st.sidebar.selectbox("▲ 黒三角", horses, index=2)
m4 = st.sidebar.selectbox("△ 白三角", horses, index=3)
m5 = st.sidebar.selectbox("× ペケ", horses, index=4)

marks = [m1, m2, m3, m4, m5]

# =========================
# 歪み計算
# =========================

distortion = (
    (quinella / win)
    + (exacta / quinella)
    + (trio / exacta)
    + (trifecta / trio)
)

# =========================
# レース判定
# =========================

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

# =========================
# 判定結果
# =========================

st.subheader("📊 レース判定")

if score == 0:
    st.success("鉄板レース")
    st.caption("本命信頼度が高い")

elif score <= 2:
    st.info("標準レース")
    st.caption("平均的なオッズ構造")

elif score <= 4:
    st.warning("波乱レース")
    st.caption("1番人気が飛ぶ可能性あり")

else:
    st.error("混沌レース")
    st.caption("市場評価が崩壊")

# =========================
# 歪み表示
# =========================

st.subheader("📉 オッズ歪み指数")

st.write(round(distortion, 2))
st.caption("オッズ構造のゆがみを数値化")

# =========================
# 買い目生成
# =========================

if st.button("🚀 買い目生成（8頭版）"):

    others = [h for h in horses if h not in marks]

    g = [m4, m5] + others

    # A
    A = list(itertools.combinations([m2, m3, m4, m5], 3))

    # B
    B = [(m1, x, y) for x, y in itertools.combinations(g, 2)]

    # C
    C = list(itertools.combinations([m2, m3, m4, m5], 2))

    # D
    D = [(m1, x) for x in g]

    st.divider()

    c1, c2 = st.columns(2)

    with c1:

        st.subheader(f"A 3連複BOX ({len(A)}点)")
        st.code("\n".join([f"{a}-{b}-{c}" for a,b,c in A]))

        st.subheader(f"C 馬連BOX ({len(C)}点)")
        st.code("\n".join([f"{a}-{b}" for a,b in C]))

    with c2:

        st.subheader(f"B 3連複◎軸 ({len(B)}点)")
        st.code("\n".join([f"{a}-{b}-{c}" for a,b,c in B]))

        st.subheader(f"D 馬連◎軸 ({len(D)}点)")
        st.code("\n".join([f"{a}-{b}" for a,b in D]))

    total = len(A) + len(B) + len(C) + len(D)

    st.subheader("合計点数")

    st.success(f"{total} 点")
