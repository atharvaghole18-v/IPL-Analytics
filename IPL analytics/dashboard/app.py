import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="IPL Analytics", page_icon="🏏", layout="wide")

@st.cache_data
def load_data():
    matches = pd.read_csv("data/matches.csv")
    deliveries = pd.read_csv("data/deliveries.csv")
    matches.dropna(subset=["winner"], inplace=True)
    matches["season"] = matches["season"].apply(lambda x: int(str(x)[:4]))
    return matches, deliveries

matches, deliveries = load_data()

# ── Sidebar ────────────────────────────────────────────
st.sidebar.title("🏏 IPL Analytics")
seasons = sorted(matches["season"].unique())
selected_seasons = st.sidebar.multiselect(
    "Select Seasons", seasons, default=seasons
)

filtered = matches[matches["season"].isin(selected_seasons)]

# ── KPI Cards ──────────────────────────────────────────
st.title("🏏 IPL Analytics Dashboard")

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Matches", len(filtered))
k2.metric("Total Teams", filtered["team1"].nunique())
k3.metric("Total Seasons", filtered["season"].nunique())

toss_win_count = filtered[filtered["toss_winner"] == filtered["winner"]]
k4.metric("Toss→Win Rate", f"{round(len(toss_win_count)/len(filtered)*100, 1)}%")

st.divider()

# ── Row 1 ──────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("Most Winning Teams")
    team_wins = filtered["winner"].value_counts().head(8)
    fig, ax = plt.subplots(figsize=(6, 4))
    team_wins.plot(kind="barh", ax=ax, color=sns.color_palette("Blues_r", 8))
    ax.set_xlabel("Wins")
    plt.tight_layout()
    st.pyplot(fig)

with col2:
    st.subheader("Toss Decision Preference")
    toss_dec = filtered["toss_decision"].value_counts()
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.pie(toss_dec, labels=toss_dec.index, autopct="%1.1f%%",
           colors=["#60A5FA", "#34D399"])
    plt.tight_layout()
    st.pyplot(fig)

st.divider()

# ── Row 2 ──────────────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    st.subheader("Top Run Scorers")
    match_ids = filtered["id"].tolist()
    filtered_del = deliveries[deliveries["match_id"].isin(match_ids)]
    top_batsmen = (filtered_del.groupby("batter")["batsman_runs"]
                   .sum().sort_values(ascending=False).head(10))
    fig, ax = plt.subplots(figsize=(6, 4))
    top_batsmen.plot(kind="barh", ax=ax, color=sns.color_palette("Oranges_r", 10))
    ax.set_xlabel("Runs")
    plt.tight_layout()
    st.pyplot(fig)

with col4:
    st.subheader("Top Wicket Takers")
    wicket_del = filtered_del[filtered_del["dismissal_kind"].notna()]
    wicket_del = wicket_del[~wicket_del["dismissal_kind"].isin(
        ["run out", "retired hurt"])]
    top_bowlers = (wicket_del.groupby("bowler")["dismissal_kind"]
                   .count().sort_values(ascending=False).head(10))
    fig, ax = plt.subplots(figsize=(6, 4))
    top_bowlers.plot(kind="barh", ax=ax, color=sns.color_palette("Greens_r", 10))
    ax.set_xlabel("Wickets")
    plt.tight_layout()
    st.pyplot(fig)

st.divider()

# ── Season trend ───────────────────────────────────────
st.subheader("Matches per Season")
season_count = filtered.groupby("season").size()
fig, ax = plt.subplots(figsize=(10, 3))
season_count.plot(kind="line", ax=ax, marker="o", color="#6366F1", linewidth=2)
ax.set_ylabel("Matches")
plt.tight_layout()
st.pyplot(fig)

st.divider()
st.subheader("Raw Match Data")
st.dataframe(filtered[["season", "team1", "team2", "winner",
                        "toss_winner", "toss_decision", "venue"]].head(50),
             use_container_width=True)