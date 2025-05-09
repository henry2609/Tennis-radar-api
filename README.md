# 🎾 Game Analytics: Unlocking Tennis Data with SportRadar API

## 📌 Objective
This project aims to build an interactive dashboard for analyzing tennis competition data using the SportRadar API. It enables users to explore competition hierarchies, player rankings, and venue data with real-time insights.

---

## 🛠️ Tech Stack
- **Languages**: Python
- **API**: [SportRadar Tennis API](https://developer.sportradar.com/tennis/reference/)
- **Database**: MySQL / PostgreSQL
- **App Framework**: Streamlit

---

## 📊 Features
- **Event Exploration**: Browse through tournaments and categories.
- **Player Leaderboards**: View top-ranked players in doubles.
- **Venue & Complex Insights**: Analyze global venue distribution.
- **Country-Wise Analysis**: Competitor stats by country.
- **Search & Filter**: By rank, country, or points.
- **Interactive UI**: Dynamic charts and tables.

---

## 🔗 API Endpoints Used
- `competitions`: To fetch category and competition details.
- `complexes`: For venue and complex metadata.
- `doubles-competitor-rankings`: For current player rankings.

---

## 🗃️ Database Schema
- `Categories`
- `Competitions`
- `Complexes`
- `Venues`
- `Competitors`
- `Competitor_Rankings`

> All tables are normalized with primary and foreign keys.

---

## 🧠 Sample SQL Queries
```sql
-- Top 5 ranked players
SELECT name, rank, points FROM Competitor_Rankings 
JOIN Competitors ON Competitor_Rankings.competitor_id = Competitors.competitor_id 
ORDER BY rank ASC LIMIT 5;

-- Competitions by Category
SELECT category_name, COUNT(*) as total_competitions 
FROM Competitions 
JOIN Categories USING(category_id) 
GROUP BY category_name;
