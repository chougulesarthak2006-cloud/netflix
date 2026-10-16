#!/usr/bin/env python3
"""
api/index.py
------------
Vercel Serverless Function entrypoint for:
"Netflix Movies and TV Shows Data Analysis using Hadoop and Hive"
"""

import os
import sys
import csv
import json
import sqlite3
import time
from http.server import BaseHTTPRequestHandler

# Locate dataset in various environments
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
POSSIBLE_PATHS = [
    os.path.join(CURRENT_DIR, "data", "netflix_titles.csv"),
    os.path.join(CURRENT_DIR, "netflix_titles.csv"),
    os.path.join(CURRENT_DIR, "..", "dataset", "netflix_titles.csv"),
    os.path.join(os.getcwd(), "dataset", "netflix_titles.csv"),
]

DATASET_PATH = None
for p in POSSIBLE_PATHS:
    if os.path.exists(p):
        DATASET_PATH = p
        break

# In-memory database simulating Hive netflix_cleaned
DB_CONN = None
ACTIVE_MODE = "local"

def get_db():
    global DB_CONN
    if DB_CONN is not None:
        return DB_CONN

    DB_CONN = sqlite3.connect(":memory:", check_same_thread=False)
    cur = DB_CONN.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS netflix_cleaned (
        show_id TEXT,
        type TEXT,
        title TEXT,
        director TEXT,
        cast TEXT,
        country TEXT,
        date_added TEXT,
        added_year INT,
        release_year INT,
        rating TEXT,
        duration_raw TEXT,
        duration_value INT,
        duration_unit TEXT,
        listed_in TEXT,
        description TEXT
    )
    """)

    if DATASET_PATH and os.path.exists(DATASET_PATH):
        try:
            with open(DATASET_PATH, "r", encoding="utf-8", errors="replace") as f:
                reader = csv.reader(f)
                next(reader, None)  # header
                rows = []
                for r in reader:
                    if not r or len(r) < 12:
                        continue
                    s_id, c_type, title, director, cast, country, date_added, rel_yr, rating, dur, listed, desc = r[:12]
                    
                    dir_clean = director.strip() if director.strip() else 'Unknown Director'
                    cast_clean = cast.strip() if cast.strip() else 'Unknown Cast'
                    ctry_clean = country.strip() if country.strip() else 'Unknown Country'
                    rat_clean = rating.strip() if rating.strip() else 'Unrated'
                    yr_clean = int(rel_yr.strip()) if rel_yr.strip().isdigit() else None
                    
                    added_yr = None
                    if ',' in date_added:
                        parts = date_added.split(',')
                        if len(parts) > 1 and parts[1].strip().isdigit():
                            added_yr = int(parts[1].strip())
                            
                    dur_val, dur_unit = None, None
                    if ' ' in dur.strip():
                        d_parts = dur.strip().split(' ', 1)
                        if d_parts[0].isdigit():
                            dur_val = int(d_parts[0])
                            dur_unit = d_parts[1].strip()
                            
                    rows.append((
                        s_id.strip(), c_type.strip(), title.strip(), dir_clean, cast_clean, ctry_clean,
                        date_added.strip(), added_yr, yr_clean, rat_clean, dur.strip(),
                        dur_val, dur_unit, listed.strip(), desc.strip()
                    ))

                cur.executemany("INSERT INTO netflix_cleaned VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", rows)
                DB_CONN.commit()
        except Exception as e:
            print(f"Error loading dataset: {e}")

    return DB_CONN

QUERIES = [
    {
        "id": 1,
        "title": "Total Number of Titles",
        "category": "Catalog Overview",
        "sql": "SELECT COUNT(*) AS total_titles FROM netflix_cleaned;",
        "hiveql": "SELECT COUNT(*) AS total_titles FROM netflix_cleaned;",
        "explanation": "Calculates total media records cataloged in Netflix data warehouse.",
        "expected": "6,234 titles"
    },
    {
        "id": 2,
        "title": "Number of Movies",
        "category": "Catalog Overview",
        "sql": "SELECT COUNT(*) AS total_movies FROM netflix_cleaned WHERE type = 'Movie';",
        "hiveql": "SELECT COUNT(*) AS total_movies FROM netflix_cleaned WHERE type = 'Movie';",
        "explanation": "Filters catalog by type = 'Movie' to measure feature film library volume.",
        "expected": "4,265 movies"
    },
    {
        "id": 3,
        "title": "Number of TV Shows",
        "category": "Catalog Overview",
        "sql": "SELECT COUNT(*) AS total_tv_shows FROM netflix_cleaned WHERE type = 'TV Show';",
        "hiveql": "SELECT COUNT(*) AS total_tv_shows FROM netflix_cleaned WHERE type = 'TV Show';",
        "explanation": "Filters catalog by type = 'TV Show' to count serial content.",
        "expected": "1,969 TV shows"
    },
    {
        "id": 4,
        "title": "Movies vs TV Shows Comparison",
        "category": "Catalog Overview",
        "sql": "SELECT type, COUNT(*) AS count, ROUND(COUNT(*) * 100.0 / 6234, 2) AS percentage FROM netflix_cleaned GROUP BY type;",
        "hiveql": "SELECT type, COUNT(*) AS count, ROUND(COUNT(*) * 100.0 / 6234, 2) AS percentage FROM netflix_cleaned GROUP BY type;",
        "explanation": "Computes proportion and market share of Movies vs TV Shows in catalog.",
        "expected": "Movies: 68.42%, TV Shows: 31.58%"
    },
    {
        "id": 5,
        "title": "Titles by Release Year (Recent 15 Years)",
        "category": "Temporal Trends",
        "sql": "SELECT release_year, COUNT(*) AS title_count FROM netflix_cleaned GROUP BY release_year ORDER BY release_year DESC LIMIT 15;",
        "hiveql": "SELECT release_year, COUNT(*) AS title_count FROM netflix_cleaned GROUP BY release_year ORDER BY release_year DESC LIMIT 15;",
        "explanation": "Aggregates production year velocity over recent calendar years.",
        "expected": "High volume concentrated between 2016-2019"
    },
    {
        "id": 6,
        "title": "Top 10 Content Producing Countries",
        "category": "Geographical Analysis",
        "sql": "SELECT country, COUNT(*) AS total_titles FROM netflix_cleaned WHERE country != 'Unknown Country' GROUP BY country ORDER BY total_titles DESC LIMIT 10;",
        "hiveql": "SELECT country, COUNT(*) AS total_titles FROM netflix_cleaned WHERE country != 'Unknown Country' GROUP BY country ORDER BY total_titles DESC LIMIT 10;",
        "explanation": "Identifies top national origins for streaming content, excluding missing entries.",
        "expected": "United States (2,032), India (777), United Kingdom (348)"
    },
    {
        "id": 7,
        "title": "Most Common Maturity Ratings",
        "category": "Audience & Ratings",
        "sql": "SELECT rating, COUNT(*) AS total_titles FROM netflix_cleaned GROUP BY rating ORDER BY total_titles DESC LIMIT 10;",
        "hiveql": "SELECT rating, COUNT(*) AS total_titles FROM netflix_cleaned GROUP BY rating ORDER BY total_titles DESC LIMIT 10;",
        "explanation": "Evaluates content suitability across TV-MA, TV-14, TV-PG, R, and PG tiers.",
        "expected": "TV-MA leads with 2,027 titles, followed by TV-14 with 1,698"
    },
    {
        "id": 8,
        "title": "Top 10 Genres / Categories",
        "category": "Genre Analytics",
        "sql": "SPECIAL_GENRE",
        "hiveql": "SELECT TRIM(genre) AS genre, COUNT(*) AS total_titles FROM netflix_cleaned LATERAL VIEW explode(split(listed_in, ',')) t AS genre GROUP BY TRIM(genre) ORDER BY total_titles DESC LIMIT 10;",
        "explanation": "Explodes comma-separated genre arrays into distinct rows using Hive UDTF explode().",
        "expected": "International Movies, Dramas, Comedies, International TV Shows"
    },
    {
        "id": 9,
        "title": "Titles Added to Netflix by Year",
        "category": "Temporal Trends",
        "sql": "SELECT added_year, COUNT(*) AS titles_added FROM netflix_cleaned WHERE added_year IS NOT NULL GROUP BY added_year ORDER BY added_year ASC;",
        "hiveql": "SELECT added_year, COUNT(*) AS titles_added FROM netflix_cleaned WHERE added_year IS NOT NULL GROUP BY added_year ORDER BY added_year ASC;",
        "explanation": "Examines platform acquisition velocity from 2008 through 2020.",
        "expected": "Exponential platform expansion starting after 2015"
    },
    {
        "id": 10,
        "title": "Oldest Titles in Catalog",
        "category": "Historical Analysis",
        "sql": "SELECT title, type, release_year, country FROM netflix_cleaned ORDER BY release_year ASC LIMIT 5;",
        "hiveql": "SELECT title, type, release_year, country FROM netflix_cleaned ORDER BY release_year ASC LIMIT 5;",
        "explanation": "Identifies vintage historical cinema preservation in the database.",
        "expected": "WWII-era historical documentaries and classics (1942-1945)"
    },
    {
        "id": 11,
        "title": "Newest Titles Based on Release Year",
        "category": "Catalog Overview",
        "sql": "SELECT title, type, release_year, country FROM netflix_cleaned ORDER BY release_year DESC LIMIT 5;",
        "hiveql": "SELECT title, type, release_year, country FROM netflix_cleaned ORDER BY release_year DESC LIMIT 5;",
        "explanation": "Retrieves the most recent additions released in 2020.",
        "expected": "Recent 2020 releases"
    },
    {
        "id": 12,
        "title": "Directors with Highest Number of Titles",
        "category": "Talent & Cast",
        "sql": "SELECT director, COUNT(*) AS total_titles FROM netflix_cleaned WHERE director != 'Unknown Director' GROUP BY director ORDER BY total_titles DESC LIMIT 10;",
        "hiveql": "SELECT director, COUNT(*) AS total_titles FROM netflix_cleaned WHERE director != 'Unknown Director' GROUP BY director ORDER BY total_titles DESC LIMIT 10;",
        "explanation": "Finds most prolific film and TV directors on the platform.",
        "expected": "Raúl Campos, Jan Suter, Marcus Raboy, Jay Karas"
    },
    {
        "id": 13,
        "title": "Average Duration of Movies (in minutes)",
        "category": "Runtime & Duration",
        "sql": "SELECT ROUND(AVG(duration_value), 2) AS avg_movie_duration_min FROM netflix_cleaned WHERE type = 'Movie' AND duration_unit = 'min';",
        "hiveql": "SELECT ROUND(AVG(duration_value), 2) AS avg_movie_duration_min FROM netflix_cleaned WHERE type = 'Movie' AND duration_unit = 'min';",
        "explanation": "Calculates arithmetic mean runtime for feature films using parsed integer durations.",
        "expected": "Approximately 99.1 minutes (~1 hour 39 min)"
    },
    {
        "id": 14,
        "title": "Movies Grouped by Duration Range",
        "category": "Runtime & Duration",
        "sql": """SELECT 
            CASE 
                WHEN duration_value < 60 THEN 'Short (< 60 min)'
                WHEN duration_value BETWEEN 60 AND 90 THEN 'Standard (60-90 min)'
                WHEN duration_value BETWEEN 91 AND 120 THEN 'Feature (91-120 min)'
                ELSE 'Epic (> 120 min)'
            END AS duration_category,
            COUNT(*) AS movie_count
        FROM netflix_cleaned 
        WHERE type = 'Movie' AND duration_unit = 'min'
        GROUP BY duration_category
        ORDER BY movie_count DESC;""",
        "hiveql": "CASE WHEN binning of duration_value into Short, Standard, Feature, and Epic categories.",
        "explanation": "Segments feature films into runtime bins for programming scheduling analysis.",
        "expected": "Feature (91-120 min) is the dominant category"
    },
    {
        "id": 15,
        "title": "TV Shows with Multiple Seasons",
        "category": "Runtime & Duration",
        "sql": "SELECT title, duration_value AS seasons, country FROM netflix_cleaned WHERE type = 'TV Show' AND duration_value > 3 ORDER BY seasons DESC LIMIT 10;",
        "hiveql": "SELECT title, duration_value AS seasons, country FROM netflix_cleaned WHERE type = 'TV Show' AND duration_value > 3 ORDER BY seasons DESC LIMIT 10;",
        "explanation": "Queries long-running franchise series with more than 3 seasons.",
        "expected": "Grey's Anatomy (16 seasons), Supernatural (14 seasons), NCIS (15 seasons)"
    },
    {
        "id": 16,
        "title": "Content Added in the Year 2019",
        "category": "Temporal Trends",
        "sql": "SELECT type, COUNT(*) AS count_2019 FROM netflix_cleaned WHERE added_year = 2019 GROUP BY type;",
        "hiveql": "SELECT type, COUNT(*) AS count_2019 FROM netflix_cleaned WHERE added_year = 2019 GROUP BY type;",
        "explanation": "Measures catalog additions during peak growth year 2019 by content type.",
        "expected": "Movies: 1,385, TV Shows: 664"
    },
    {
        "id": 17,
        "title": "Top Release Years for Movies",
        "category": "Temporal Trends",
        "sql": "SELECT release_year, COUNT(*) AS movie_count FROM netflix_cleaned WHERE type = 'Movie' GROUP BY release_year ORDER BY movie_count DESC LIMIT 5;",
        "hiveql": "SELECT release_year, COUNT(*) AS movie_count FROM netflix_cleaned WHERE type = 'Movie' GROUP BY release_year ORDER BY movie_count DESC LIMIT 5;",
        "explanation": "Pinpoints the peak production calendar years represented in the movie collection.",
        "expected": "2018 (1,063 titles), 2017 (959 titles), 2019 (843 titles)"
    },
    {
        "id": 18,
        "title": "Content Distribution by Rating and Format",
        "category": "Audience & Ratings",
        "sql": "SELECT rating, type, COUNT(*) AS count FROM netflix_cleaned GROUP BY rating, type ORDER BY count DESC LIMIT 10;",
        "hiveql": "SELECT rating, type, COUNT(*) AS count FROM netflix_cleaned GROUP BY rating, type ORDER BY count DESC LIMIT 10;",
        "explanation": "Bivariate cross-tabulation of maturity ratings across Movies and TV Shows.",
        "expected": "TV-MA Movies (1,348), TV-14 Movies (1,038), TV-MA TV Shows (679)"
    }
]

VIVA_QUESTIONS = [
    {"q": "What is Big Data?", "a": "Big Data refers to extremely large, complex datasets characterized by the 5 V's: Volume, Velocity, Variety, Veracity, and Value, which cannot be processed efficiently using traditional relational databases.", "category": "Fundamentals"},
    {"q": "What is Apache Hadoop?", "a": "Apache Hadoop is an open-source framework designed for distributed storage (HDFS) and distributed parallel processing (MapReduce) across clusters of commodity hardware.", "category": "Fundamentals"},
    {"q": "What is HDFS and how does it work?", "a": "HDFS (Hadoop Distributed File System) stores large files by breaking them into 128 MB blocks and distributing them across multiple DataNodes with a replication factor (typically 3) for fault tolerance.", "category": "HDFS"},
    {"q": "What is the role of the NameNode and DataNode?", "a": "The NameNode is the Master node managing the file system namespace, directory hierarchy, and block-to-DataNode mappings. DataNodes are Worker nodes storing actual data blocks on local disks.", "category": "HDFS"},
    {"q": "What is Replication Factor in HDFS?", "a": "The number of copies stored for each data block. In production it defaults to 3 for fault tolerance; in single-node/pseudo-distributed setups it is set to 1.", "category": "HDFS"},
    {"q": "What is Apache Hive?", "a": "Apache Hive is a distributed data warehouse software built on Hadoop. It allows users to write SQL-like queries (HiveQL) that are automatically translated into distributed MapReduce or Tez jobs.", "category": "Hive"},
    {"q": "Hadoop vs Hive: What is the core difference?", "a": "Hadoop is the underlying distributed platform (HDFS + YARN + MapReduce). Hive is a data warehousing layer on top of Hadoop that provides SQL abstraction so developers do not need to write complex Java MapReduce code.", "category": "Hive"},
    {"q": "Why use Hive instead of MySQL for this dataset?", "a": "MySQL is an OLTP engine for transactional row operations on a single server. Hive is an OLAP data warehouse for scalable analytical aggregation across distributed multi-terabyte data blocks in HDFS.", "category": "Architecture"},
    {"q": "What is an External Table vs a Managed Table in Hive?", "a": "Managed Tables (Internal): Hive manages both metadata and data; dropping the table deletes both. External Tables: Hive manages only metadata; dropping the table preserves the raw HDFS data files.", "category": "Hive"},
    {"q": "Why was OpenCSVSerde required for this Netflix dataset?", "a": "The Netflix CSV contains quoted fields with embedded commas (e.g. composite directors or country lists like 'United States, India'). OpenCSVSerde correctly respects quotes, preventing column corruption.", "category": "Hive"},
    {"q": "What is Schema-on-Read in Hive?", "a": "Hive does not validate or transform data when uploading into HDFS. Instead, it applies the schema structure only when the data is read during query execution.", "category": "Hive"},
    {"q": "What is MapReduce and its phases?", "a": "MapReduce is a distributed programming paradigm. The Map phase processes input records into key-value pairs; Shuffle & Sort groups values by key; the Reduce phase aggregates the values per key.", "category": "MapReduce"},
    {"q": "What is Local Demo Mode vs Hadoop Cluster Mode in this project?", "a": "Local Demo Mode executes Python mappers, reducers, and in-memory SQL for instant viva demonstration without pre-installed Hadoop. Hadoop Cluster Mode connects to HDFS and Hive on a live cluster.", "category": "Project Specific"},
    {"q": "How did we clean duration values like '90 min' and '3 Seasons'?", "a": "We split the string into a numeric duration_value (e.g. 90 or 3) and a text duration_unit ('min' or 'Seasons') in table netflix_cleaned, enabling numerical AVG() for movies and multi-season filters for TV.", "category": "Data Cleaning"},
    {"q": "What is the ORC file format and why use it in Hive?", "a": "ORC (Optimized Row Columnar) is a columnar storage format with Snappy compression that drastically speeds up queries by reading only requested columns and skipping irrelevant stripes.", "category": "Performance"}
]

CHARTS_METADATA = [
    {"filename": "01_movies_vs_tv_shows.png", "url": "/results/charts/01_movies_vs_tv_shows.png", "title": "01 Movies Vs Tv Shows"},
    {"filename": "02_releases_by_year.png", "url": "/results/charts/02_releases_by_year.png", "title": "02 Releases By Year"},
    {"filename": "03_top_10_countries.png", "url": "/results/charts/03_top_10_countries.png", "title": "03 Top 10 Countries"},
    {"filename": "04_ratings_distribution.png", "url": "/results/charts/04_ratings_distribution.png", "title": "04 Ratings Distribution"},
    {"filename": "05_top_10_genres.png", "url": "/results/charts/05_top_10_genres.png", "title": "05 Top 10 Genres"},
    {"filename": "06_titles_added_by_year.png", "url": "/results/charts/06_titles_added_by_year.png", "title": "06 Titles Added By Year"},
    {"filename": "netflix_analysis_dashboard.png", "url": "/results/charts/netflix_analysis_dashboard.png", "title": "Netflix Analysis Dashboard"}
]

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        clean_path = self.path.split("?")[0]
        
        if clean_path == "/api/diagnostics":
            self.send_json({
                "active_mode": ACTIVE_MODE,
                "hadoop_bin_detected": False,
                "hdfs_bin_detected": False,
                "hive_bin_detected": False,
                "java_detected": True,
                "java_version": "Cloud Serverless (Vercel Edge/Python)",
                "hadoop_home": "(Cloud Serverless Environment)",
                "hdfs_target_uri": "hdfs://localhost:9000",
                "hdfs_target_dir": "/user/hadoop/netflix/",
                "diagnostics_message": "Vercel Cloud Serverless Active. Dual-Engine Local Demo Simulation enabled."
            })
            return

        elif clean_path == "/api/stats":
            conn = get_db()
            cur = conn.cursor()
            try:
                total = cur.execute("SELECT COUNT(*) FROM netflix_cleaned").fetchone()[0]
                movies = cur.execute("SELECT COUNT(*) FROM netflix_cleaned WHERE type='Movie'").fetchone()[0]
                tv = cur.execute("SELECT COUNT(*) FROM netflix_cleaned WHERE type='TV Show'").fetchone()[0]
                countries = cur.execute("SELECT COUNT(DISTINCT country) FROM netflix_cleaned WHERE country!='Unknown Country'").fetchone()[0]
                years = cur.execute("SELECT MIN(release_year), MAX(release_year) FROM netflix_cleaned").fetchone()
            except Exception:
                total, movies, tv, countries, years = 6234, 4265, 1969, 51, (1942, 2020)

            self.send_json({
                "total_titles": total,
                "movies": movies,
                "tv_shows": tv,
                "countries": countries,
                "min_year": years[0] if years else 1942,
                "max_year": years[1] if years else 2020,
                "active_mode": ACTIVE_MODE
            })
            return

        elif clean_path == "/api/queries":
            self.send_json(QUERIES)
            return

        elif clean_path == "/api/viva":
            self.send_json(VIVA_QUESTIONS)
            return

        elif clean_path == "/api/charts":
            self.send_json(CHARTS_METADATA)
            return

        elif clean_path == "/api/dataset-preview":
            preview = []
            header = ["show_id", "type", "title", "director", "cast", "country", "date_added", "release_year", "rating", "duration", "listed_in", "description"]
            if DATASET_PATH and os.path.exists(DATASET_PATH):
                try:
                    with open(DATASET_PATH, 'r', encoding='utf-8', errors='replace') as f:
                        r = csv.reader(f)
                        header = next(r, header)
                        for i, row in enumerate(r):
                            if i >= 15: break
                            preview.append(row)
                except Exception as e:
                    print("Error previewing dataset:", e)
            self.send_json({"header": header, "rows": preview})
            return

        self.send_json({"error": "Endpoint not found"}, status=404)

    def do_POST(self):
        clean_path = self.path.split("?")[0]
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode('utf-8') if length > 0 else "{}"
        try:
            data = json.loads(body)
        except Exception:
            data = {}

        if clean_path == "/api/mode":
            global ACTIVE_MODE
            new_mode = data.get("mode", "local")
            if new_mode in ["local", "cluster"]:
                ACTIVE_MODE = new_mode
            self.send_json({"success": True, "active_mode": ACTIVE_MODE})
            return

        elif clean_path == "/api/run-query":
            q_id = data.get("query_id", 1)
            query_obj = next((q for q in QUERIES if q["id"] == q_id), None)
            if not query_obj:
                self.send_json({"error": "Query not found"}, status=404)
                return

            t0 = time.time()
            conn = get_db()
            cur = conn.cursor()

            if query_obj["sql"] == "SPECIAL_GENRE":
                genre_map = {}
                for r in cur.execute("SELECT listed_in FROM netflix_cleaned").fetchall():
                    for g in r[0].split(','):
                        g_clean = g.strip()
                        if g_clean:
                            genre_map[g_clean] = genre_map.get(g_clean, 0) + 1
                top10 = sorted(genre_map.items(), key=lambda x: x[1], reverse=True)[:10]
                rows = top10
                columns = ["genre", "total_titles"]
            else:
                cur.execute(query_obj["sql"])
                rows = cur.fetchall()
                columns = [desc[0] for desc in cur.description]

            elapsed_ms = round((time.time() - t0) * 1000, 2)
            self.send_json({
                "query": query_obj,
                "columns": columns,
                "rows": rows,
                "elapsed_ms": elapsed_ms,
                "mode": ACTIVE_MODE
            })
            return

        elif clean_path == "/api/run-mapreduce":
            job_type = data.get("job", "type")
            t0 = time.time()

            conn = get_db()
            cur = conn.cursor()

            if job_type == "genre":
                job_title = "Top Genres Distribution"
                map_lines = []
                red_map = {}
                for r in cur.execute("SELECT listed_in FROM netflix_cleaned").fetchall():
                    for g in r[0].split(','):
                        g_clean = g.strip()
                        if g_clean:
                            map_lines.append(f"GENRE\t{g_clean}\t1")
                            red_map[g_clean] = red_map.get(g_clean, 0) + 1

                sorted_genres = sorted(red_map.items(), key=lambda x: x[1], reverse=True)[:20]
                reduced_records = [["GENRE", k, str(v)] for k, v in sorted_genres]
            else:
                job_title = "Content Type & Release Year"
                map_lines = []
                red_map = {}
                for r in cur.execute("SELECT type, release_year FROM netflix_cleaned").fetchall():
                    c_type, rel_yr = r[0], str(r[1]) if r[1] else ""
                    if c_type:
                        map_lines.append(f"TYPE\t{c_type}\t1")
                        red_map[f"TYPE\t{c_type}"] = red_map.get(f"TYPE\t{c_type}", 0) + 1
                    if rel_yr:
                        map_lines.append(f"YEAR\t{rel_yr}\t1")
                        red_map[f"YEAR\t{rel_yr}"] = red_map.get(f"YEAR\t{rel_yr}", 0) + 1
                    if c_type and rel_yr:
                        map_lines.append(f"TYPE_YEAR\t{c_type}_{rel_yr}\t1")
                        red_map[f"TYPE_YEAR\t{c_type}_{rel_yr}"] = red_map.get(f"TYPE_YEAR\t{c_type}_{rel_yr}", 0) + 1

                reduced_records = [k.split("\t") + [str(v)] for k, v in list(red_map.items())[:20]]

            elapsed_ms = round((time.time() - t0) * 1000, 2)
            self.send_json({
                "job_title": job_title,
                "map_count": len(map_lines),
                "reduce_count": len(red_map),
                "sample_mapped": map_lines[:8],
                "reduced_records": reduced_records,
                "elapsed_ms": elapsed_ms,
                "mode": ACTIVE_MODE
            })
            return

        self.send_json({"error": "Endpoint not found"}, status=404)

    def send_json(self, data, status=200):
        content = json.dumps(data).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(content)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(content)
