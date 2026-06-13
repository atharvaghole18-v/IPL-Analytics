import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings("ignore")

sns.set_theme(style="whitegrid", palette="muted")

# ── Load data ──────────────────────────────────────────
matches = pd.read_csv("data/matches.csv")
deliveries = pd.read_csv("data/deliveries.csv")

print("Matches shape:", matches.shape)
print("Deliveries shape:", deliveries.shape)

# ── Clean matches ──────────────────────────────────────
matches.dropna(subset=["winner"], inplace=True)
matches["season"] = matches["season"].apply(lambda x: int(str(x)[:4]))

# ── Clean deliveries ───────────────────────────────────
deliveries["total_runs"] = deliveries["total_runs"].fillna(0)

print("\n✅ Data loaded and cleaned successfully!")

# ── Create charts folder ───────────────────────────────
os.makedirs("charts", exist_ok=True)

# ── 1. Most successful teams ───────────────────────────
team_wins = matches["winner"].value_counts().head(10)

fig, ax = plt.subplots(figsize=(10, 5))
team_wins.plot(kind="barh", ax=ax, color=sns.color_palette("Blues_r", 10))
ax.set_title("Top 10 Most Winning Teams in IPL", fontsize=14)
ax.set_xlabel("Total Wins")
plt.tight_layout()
plt.savefig("charts/team_wins.png", dpi=150)
plt.show()

# ── 2. Toss decision impact ────────────────────────────
toss_win = matches[matches["toss_winner"] == matches["winner"]]
toss_pct = round(len(toss_win) / len(matches) * 100, 1)
print(f"\nToss winner also won the match: {toss_pct}%")

toss_decision = matches["toss_decision"].value_counts()
fig, ax = plt.subplots(figsize=(6, 4))
toss_decision.plot(kind="bar", ax=ax, color=["#60A5FA", "#34D399"])
ax.set_title("Toss Decision — Field vs Bat")
ax.set_xlabel("")
plt.tight_layout()
plt.savefig("charts/toss_decision.png", dpi=150)
plt.show()

# ── 3. Matches per season ──────────────────────────────
season_matches = matches.groupby("season").size()

fig, ax = plt.subplots(figsize=(10, 4))
season_matches.plot(kind="line", ax=ax, marker="o", color="#6366F1", linewidth=2)
ax.set_title("Number of Matches per IPL Season")
ax.set_ylabel("Matches")
ax.set_xlabel("Season")
plt.tight_layout()
plt.savefig("charts/season_matches.png", dpi=150)
plt.show()

# ── 4. Top venues ──────────────────────────────────────
top_venues = matches["venue"].value_counts().head(8)

fig, ax = plt.subplots(figsize=(10, 5))
top_venues.plot(kind="barh", ax=ax, color=sns.color_palette("Purples_r", 8))
ax.set_title("Top 8 IPL Venues by Matches Hosted")
plt.tight_layout()
plt.savefig("charts/venues.png", dpi=150)
plt.show()

# ── 5. Win by runs vs wickets ──────────────────────────
win_type = matches["result"].value_counts()

fig, ax = plt.subplots(figsize=(6, 6))
ax.pie(win_type, labels=win_type.index, autopct="%1.1f%%",
       colors=sns.color_palette("pastel"))
ax.set_title("Match Result Type")
plt.tight_layout()
plt.savefig("charts/win_type.png", dpi=150)
plt.show()

# ── Top run scorers ────────────────────────────────────
batsman_runs = (
    deliveries.groupby("batter")["batsman_runs"]
    .sum()
    .sort_values(ascending=False)
    .head(15)
    .reset_index()
)
batsman_runs.columns = ["Batsman", "Total Runs"]

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=batsman_runs, y="Batsman", x="Total Runs",
            palette="Blues_r", ax=ax)
ax.set_title("Top 15 Run Scorers in IPL History")
plt.tight_layout()
plt.savefig("charts/top_batsmen.png", dpi=150)
plt.show()

# ── Strike rate (min 500 balls faced) ─────────────────
balls_faced = deliveries.groupby("batter")["ball"].count()
runs_scored = deliveries.groupby("batter")["batsman_runs"].sum()

strike_rate = (runs_scored / balls_faced * 100).round(2)
sr_df = pd.DataFrame({"Strike Rate": strike_rate,
                       "Balls": balls_faced,
                       "Runs": runs_scored})
sr_df = sr_df[sr_df["Balls"] >= 500].sort_values("Strike Rate", ascending=False).head(10)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=sr_df.reset_index(), y="batter", x="Strike Rate",
            palette="Oranges_r", ax=ax)
ax.set_title("Top 10 Batsmen by Strike Rate (min 500 balls)")
plt.tight_layout()
plt.savefig("charts/strike_rate.png", dpi=150)
plt.show()

# ── Top wicket takers ──────────────────────────────────
wicket_df = deliveries[deliveries["dismissal_kind"].notna()]
wicket_df = wicket_df[~wicket_df["dismissal_kind"].isin(
    ["run out", "retired hurt", "obstructing the field"]
)]

bowler_wickets = (
    wicket_df.groupby("bowler")["dismissal_kind"]
    .count()
    .sort_values(ascending=False)
    .head(15)
    .reset_index()
)
bowler_wickets.columns = ["Bowler", "Wickets"]

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=bowler_wickets, y="Bowler", x="Wickets",
            palette="Greens_r", ax=ax)
ax.set_title("Top 15 Wicket Takers in IPL History")
plt.tight_layout()
plt.savefig("charts/top_bowlers.png", dpi=150)
plt.show()

# ── Economy rate (min 300 balls bowled) ───────────────
balls_bowled = deliveries.groupby("bowler")["ball"].count()
runs_given = deliveries.groupby("bowler")["total_runs"].sum()

economy = (runs_given / balls_bowled * 6).round(2)
eco_df = pd.DataFrame({"Economy": economy, "Balls": balls_bowled})
eco_df = eco_df[eco_df["Balls"] >= 300].sort_values("Economy").head(10)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=eco_df.reset_index(), y="bowler", x="Economy",
            palette="Reds_r", ax=ax)
ax.set_title("Top 10 Most Economical Bowlers (min 300 balls)")
plt.tight_layout()
plt.savefig("charts/economy.png", dpi=150)
plt.show()

# ── Sixes hitters ──────────────────────────────────────
sixes = (
    deliveries[deliveries["batsman_runs"] == 6]
    .groupby("batter")["batsman_runs"]
    .count()
    .sort_values(ascending=False)
    .head(10)
)

fig, ax = plt.subplots(figsize=(10, 5))
sixes.plot(kind="bar", ax=ax, color="#F59E0B")
ax.set_title("Top 10 Six Hitters in IPL")
ax.set_xlabel("Batsman")
ax.set_ylabel("Sixes")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("charts/sixes.png", dpi=150)
plt.show()

print("✅ All charts saved in charts/ folder!")

# ── Final KPI summary ──────────────────────────────────
print("=" * 45)
print("         IPL ANALYTICS — KEY STATS")
print("=" * 45)
print(f"Total Seasons      : {matches['season'].nunique()}")
print(f"Total Matches      : {len(matches)}")
print(f"Total Teams        : {matches['team1'].nunique()}")
print(f"Most Wins (Team)   : {matches['winner'].value_counts().index[0]}")
print(f"Top Run Scorer     : {batsman_runs.iloc[0]['Batsman']} "
      f"({batsman_runs.iloc[0]['Total Runs']} runs)")
print(f"Top Wicket Taker   : {bowler_wickets.iloc[0]['Bowler']} "
      f"({bowler_wickets.iloc[0]['Wickets']} wickets)")
print(f"Toss Win = Match Win: {toss_pct}% of matches")
print("=" * 45)