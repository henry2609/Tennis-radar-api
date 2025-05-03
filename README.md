# Tennis-radar-api
Unlocking Tennis Data with SportRadar API
Game Analytics: Unlocking Tennis Data with SportRadar API
This project provides an interactive Streamlit dashboard to explore, analyze, and visualize tennis competition data collected from the SportRadar Tennis API. It supports real-time filtering, competitor search, rankings display, and country-level performance analysis.

🚀 Features
🏠 Dashboard Overview: Summary metrics of total competitors, countries represented, and highest points scored.

📊 Competitor Search & Filters: Filter by rank range, country, or search by name.

🌍 Country Insights: Group competitors by country with average points and total participation.

🏆 Leaderboards:

Top-ranked players

Players with the highest points

Competitors with stable rank movement (0)

🗃️ Database Schema
1. Categories Table

category_id (PK)

category_name

2. Competitions Table

competition_id (PK)

competition_name

parent_id

type

gender

category_id (FK)

3. Complexes Table

complex_id (PK)

complex_name

4. Venues Table

venue_id (PK)

venue_name

city_name

country_name

country_code

timezone

complex_id (FK)

5. Competitors Table

competitor_id (PK)

name

country

country_code

abbreviation

6. Competitor_Rankings Table

rank_id (PK, AUTO_INCREMENT)

rank

movement

points

competitions_played

competitor_id (FK)

📦 Installation
bash
Copy
Edit
# Clone this repo
git clone https://github.com/your-username/sport-radar-tennis-analytics.git
cd sport-radar-tennis-analytics

# Install dependencies
pip install -r requirements.txt
requirements.txt

nginx
Copy
Edit
streamlit
mysql-connector-python
pandas
🔧 Configuration
Edit the database credentials inside streamlit_app.py:

python
Copy
Edit
conn = mysql.connector.connect(
    host="localhost",
    user="your_user",
    password="your_password",
    database="tennis_db"
)
Make sure your MySQL database is running and the schema is loaded with the required tables and data.

🏁 Running the App
bash
Copy
Edit
streamlit run streamlit_app.py
Then visit: http://localhost:8501

📊 Example SQL Queries Used
Top 10 ranked competitors

Competitor points grouped by country

Competitions with no parent (top-level)

Venues grouped by country and complex

Competitors with stable ranking movement
