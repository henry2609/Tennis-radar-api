import streamlit as st
import pandas as pd
import mysql.connector

# --- SQL CONNECTION FUNCTION ---
@st.cache_resource
def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="tennis_analytics"
    )

# --- PAGE CONFIG ---
st.set_page_config(page_title="Tennis Event Explorer", layout="wide")

# --- HEADER ---
st.title("🎾 Game Analytics: Unlocking Tennis Data with SportRadar API")

conn = create_connection()

# --- SIDEBAR ---
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["🏠 Dashboard", "📊 Competitors", "🌍 Country Insights", "🏆 Leaderboard"])

# --- HOMEPAGE DASHBOARD ---
if page == "🏠 Dashboard":
    st.subheader("📌 Summary Statistics")

    total_competitors = pd.read_sql("SELECT COUNT(*) FROM competitors", conn).iloc[0, 0]
    countries = pd.read_sql("SELECT COUNT(DISTINCT country) FROM competitors", conn).iloc[0, 0]
    max_points = pd.read_sql("SELECT MAX(points) FROM competitor_rankings", conn).iloc[0, 0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Competitors", total_competitors)
    col2.metric("Countries Represented", countries)
    col3.metric("Highest Points", max_points)

    st.markdown("### 📅 Competitions Overview")
    df = pd.read_sql("""
        SELECT c.competition_name, c.gender, c.type, cat.category_name
        FROM competitions c
        JOIN categories cat ON c.category_id = cat.category_id
        """, conn)
    st.dataframe(df)

# --- COMPETITOR FILTER ---
elif page == "📊 Competitors":
    st.subheader("🔍 Search and Filter Competitors")

    name = st.text_input("Search by name")
    country = st.selectbox("Select Country", ["All"] + list(pd.read_sql("SELECT DISTINCT country FROM competitors", conn)["country"]))
    min_rank = st.slider("Minimum Rank", 1, 100, 1)
    max_rank = st.slider("Maximum Rank", 1, 100, 20)

    query = """
        SELECT c.name, c.country, r.rank, r.movement, r.points, r.competitions_played
        FROM competitors c
        JOIN competitor_rankings r ON c.competitor_id = r.competitor_id
        WHERE r.rank BETWEEN %s AND %s
    """
    params = [min_rank, max_rank]

    if name:
        query += " AND c.name LIKE %s"
        params.append(f"%{name}%")

    if country != "All":
        query += " AND c.country = %s"
        params.append(country)

    df = pd.read_sql(query, conn, params=params)
    st.dataframe(df)

# --- COUNTRY INSIGHTS ---
elif page == "🌍 Country Insights":
    st.subheader("🌎 Country-wise Analysis")

    df = pd.read_sql("""
        SELECT country, COUNT(*) as num_competitors, ROUND(AVG(points), 2) as avg_points
        FROM competitors c
        JOIN competitor_rankings r ON c.competitor_id = r.competitor_id
        GROUP BY country
        ORDER BY num_competitors DESC
    """, conn)

    st.dataframe(df)

# --- LEADERBOARD ---
elif page == "🏆 Leaderboard":
    st.subheader("🏅 Competitor Leaderboard")

    tab1, tab2, tab3 = st.tabs(["Top Ranked", "Highest Points", "Stable Rank"])

    with tab1:
        df1 = pd.read_sql("""
            SELECT c.name, c.country, r.rank, r.points
            FROM competitors c
            JOIN competitor_rankings r ON c.competitor_id = r.competitor_id
            ORDER BY r.rank ASC
            LIMIT 10
        """, conn)
        st.dataframe(df1)

    with tab2:
        df2 = pd.read_sql("""
            SELECT c.name, c.country, r.points, r.rank
            FROM competitors c
            JOIN competitor_rankings r ON c.competitor_id = r.competitor_id
            ORDER BY r.points DESC
            LIMIT 10
        """, conn)
        st.dataframe(df2)

    with tab3:
        df3 = pd.read_sql("""
            SELECT c.name, c.country, r.rank, r.movement
            FROM competitors c
            JOIN competitor_rankings r ON c.competitor_id = r.competitor_id
            WHERE r.movement = 0
        """, conn)
        st.dataframe(df3)
