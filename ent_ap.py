import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px

# Page setup
st.set_page_config(page_title="🎾 Tennis Analytics Dashboard", layout="wide")

# DB connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="tennis_analytics"
    )

# Cached competitor data loader — FIXED!
@st.cache_data
def load_competitor_data(_conn):
    return pd.read_sql("""
        SELECT r.rank, r.points, r.movement, r.competitions_played,
               c.name, c.country, c.country_code
        FROM Competitor_Rankings r
        JOIN Competitors c ON r.competitor_id = c.competitor_id
    """, _conn)

# Dashboard metrics
def show_dashboard(_conn):
    st.title("🎾 Tennis Analytics: Game Insights Dashboard")
    col1, col2, col3 = st.columns(3)

    with _conn.cursor(dictionary=True) as cur:
        cur.execute("SELECT COUNT(*) AS total FROM Competitors")
        col1.metric("Total Competitors", cur.fetchone()['total'])

        cur.execute("SELECT COUNT(DISTINCT country) AS total FROM Competitors")
        col2.metric("Countries Represented", cur.fetchone()['total'])

        cur.execute("SELECT MAX(points) AS highest FROM Competitor_Rankings")
        col3.metric("Highest Points", cur.fetchone()['highest'])

# Filter and Search
def search_and_filter(df):
    st.subheader("🔍 Filter & Search Competitors")
    with st.expander("Click to filter"):
        name = st.text_input("Search by Name")
        country = st.selectbox("Filter by Country", options=["All"] + sorted(df['country'].unique()))
        min_rank, max_rank = st.slider("Rank Range", 1, int(df['rank'].max()), (1, 50))
        min_points = st.slider("Minimum Points", 0, int(df['points'].max()), 1000)

    filtered = df[
        (df['rank'].between(min_rank, max_rank)) &
        (df['points'] >= min_points)
    ]

    if name:
        filtered = filtered[filtered['name'].str.contains(name, case=False)]

    if country != "All":
        filtered = filtered[filtered['country'] == country]

    st.dataframe(filtered.sort_values('rank'), use_container_width=True)
    return filtered

# Detail Viewer
def show_competitor_viewer(df):
    st.subheader("👤 Competitor Detail Viewer")
    if df.empty:
        st.info("No competitor selected.")
        return
    selected = st.selectbox("Select a Competitor", options=df['name'].unique())
    row = df[df['name'] == selected].iloc[0]
    st.markdown(f"""
    **Name:** {row['name']}  
    **Rank:** {row['rank']}  
    **Points:** {row['points']}  
    **Movement:** {row['movement']}  
    **Competitions Played:** {row['competitions_played']}  
    **Country:** {row['country']}  
    """)

# Country-wise stats
def show_country_analysis(df):
    st.subheader("🌍 Country-Wise Statistics")
    stats = df.groupby("country").agg(
        total_competitors=("name", "count"),
        avg_points=("points", "mean")
    ).sort_values("total_competitors", ascending=False).reset_index()
    st.dataframe(stats)
    fig = px.bar(stats, x="country", y="total_competitors", hover_data=["avg_points"], title="Top Countries by Competitor Count")
    st.plotly_chart(fig, use_container_width=True)

# Leaderboards
def show_leaderboards(df):
    st.subheader("🏆 Leaderboards")
    tab1, tab2 = st.tabs(["Top-Ranked", "Top Points"])
    
    with tab1:
        top_ranks = df.sort_values("rank").head(10)
        st.dataframe(top_ranks)
        st.plotly_chart(px.bar(top_ranks, x="name", y="rank", color="rank", title="Top 10 by Rank"), use_container_width=True)
    
    with tab2:
        top_points = df.sort_values("points", ascending=False).head(10)
        st.dataframe(top_points)
        st.plotly_chart(px.bar(top_points, x="name", y="points", color="points", title="Top 10 by Points"), use_container_width=True)

# Main App
def main():
    try:
        conn = get_connection()
        show_dashboard(conn)
        df = load_competitor_data(conn)

        st.markdown("---")
        filtered_df = search_and_filter(df)

        st.markdown("---")
        show_competitor_viewer(filtered_df)

        st.markdown("---")
        show_country_analysis(df)

        st.markdown("---")
        show_leaderboards(df)

    except Exception as e:
        st.error(f"❌ Error: {e}")

    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main()
