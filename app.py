import streamlit as st
import itertools
import pandas as pd

st.set_page_config(page_title="オッズディストーションAI PRO", layout="wide")

st.title("🐎 オッズディストーションAI PRO")

st.caption("オッズ歪み + 人気構造 + メディア評価からレース危険度を解析")

# -------------------
# サイドバー
# -------------------

st.sidebar.header("① オッズ入力")

win = st.sidebar.number_input("単勝", value=1.5)
quinella = st.sidebar.number_input("馬連", value=3.5)
exacta = st.sidebar.number_input("馬単", value=7.0)
trio = st.sidebar.number_input("3連複", value=12.0)
trifecta = st.sidebar.number_input("3連単", value=25.0)

st.sidebar.header("② 人気構造")

second_odds = st.sidebar.number_input("2番人気単勝", value=3.0)

st.sidebar.header("③ メディア評価")

sent = st.sidebar.selectbox(
"記事評価",
["絶賛（死角なし）","普通","不安"]
)

# -------------------
# オッズ歪み
# -------------------

distortion = (
(quinella / win) +
(exacta / quinella) +
(trio / exacta) +
(trifecta / trio)
)

# -------------------
# 人気集中度
# -------------------

concentration = second_odds / win

if concentration < 1.2:
    pop_state = "1強"
elif concentration < 1.6:
    pop_state = "やや1強"
elif concentration < 2.5:
    pop_state = "平均"
else:
    pop_state = "混戦"

# -------------------
# 飛び確率
# -------------------

risk = distortion * 5

if pop_state == "混戦":
    risk += 10

if sent == "不安":
    risk += 10

if sent == "絶賛（死角なし）":
    risk -= 5

risk = max(5, min(80, risk))

# -------------------
# レース危険度
# -------------------

if risk < 20:
    race_state = "鉄板レース"
    race_color = "success"
elif risk < 35:
    race_state = "標準レース"
    race_color = "info"
elif risk < 50:
    race_state = "荒れ注意レース"
    race_color = "warning"
else:
    race_state = "人気崩壊ゾーン"
    race_color = "error"

# -------------------
# 表示
# -------------------

col1,col2,col3 = st.columns(3)

with col1:
    st.metric("オッズ歪み", round(distortion,2))

with col2:
    st.metric("人気構造", pop_state)

with col3:
    st.metric("1番人気飛び確率", f"{int(risk)}%")

st.subheader("AIレース判定")

if race_color == "success":
    st.success(race_state)
elif race_color == "warning":
    st.warning(race_state)
elif race_color == "error":
    st.error(race_state)
else:
    st.info(race_state)

# -------------------
# 馬番入力
# -------------------

st.sidebar.header("④ 馬番入力")

h_in = st.sidebar.text_input(
"人気1〜10",
"1,2,3,4,5,6,7,8,9,10"
)

horses = [h.strip() for h in h_in.split(",") if h.strip()]

if len(horses) < 5:
    st.warning("最低5頭必要です")
    st.stop()

# -------------------
# 印
# -------------------

st.sidebar.header("⑤ 印")

m1 = st.sidebar.selectbox("◎", horses)
m2 = st.sidebar.selectbox("○", horses)
m3 = st.sidebar.selectbox("▲", horses)
m4 = st.sidebar.selectbox("△", horses)
m5 = st.sidebar.selectbox("×", horses)

marks = [m1,m2,m3,m4,m5]

# -------------------
# 資金
# -------------------

st.sidebar.header("⑥ 資金管理")

budget = st.sidebar.number_input("予算", value=5000)
unit = st.sidebar.number_input("1点金額", value=100)

# -------------------
# 買い目生成
# -------------------

if st.button("🚀 AI買い目生成"):

    ana = [m2,m3,m4,m5]

    a = list(itertools.combinations(ana,3))
    c = list(itertools.combinations(ana,2))

    others = [h for h in horses if h not in marks]

    g = [m4,m5] + others

    b = [(m1,x,y) for x,y in itertools.combinations(g,2)]
    d = [(m1,x) for x in g]

    total_bets = len(a)+len(b)+len(c)+len(d)
    cost = total_bets * unit

    st.subheader("💰 資金シミュレーション")

    st.write(f"点数: {total_bets}")
    st.write(f"必要資金: {cost}円")

    if cost > budget:
        st.error("予算オーバー")
    else:
        st.success("予算内")

    col1,col2 = st.columns(2)

    with col1:

        st.subheader(f"A:3連複BOX ({len(a)})")

        df_a = pd.DataFrame(a,columns=["馬1","馬2","馬3"])
        st.table(df_a)

        st.subheader(f"C:馬連BOX ({len(c)})")

        df_c = pd.DataFrame(c,columns=["馬1","馬2"])
        st.table(df_c)

    with col2:

        st.subheader(f"B:3連複軸 ({len(b)})")

        df_b = pd.DataFrame(b,columns=["軸","馬1","馬2"])
        st.table(df_b)

        st.subheader(f"D:馬連軸 ({len(d)})")

        df_d = pd.DataFrame(d,columns=["軸","相手"])
        st.table(df_d)
