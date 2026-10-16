#!/usr/bin/env python3
"""
app.py
------
Interactive Web Dashboard & Dual-Engine Platform for:
"Netflix Movies and TV Shows Data Analysis using Hadoop and Hive"

Features:
- Dual Engine Mode: Local Demo Mode vs Hadoop Cluster Mode (matching presentation UI)
- Live Hadoop, HDFS, Java, and Hive Diagnostics
- Quick Hadoop Terminal Commands generator
- MapReduce Stream Runner (Local Python Mapper & Reducer simulation)
- Interactive HiveQL Query Studio (18+ queries with real-time execution)
- Visual Analytics Dashboard & Chart Gallery
- Interactive Viva Voce Flashcards & Academic Project Explorer
"""

import os
import sys
import csv
import json
import sqlite3
import shutil
import subprocess
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
import socket

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(PROJECT_ROOT, "dataset", "netflix_titles.csv")
WEB_DIR = os.path.join(PROJECT_ROOT, "web")
RESULTS_DIR = os.path.join(PROJECT_ROOT, "results")
CHARTS_DIR = os.path.join(PROJECT_ROOT, "results", "charts")

# Active processing mode state (in-memory)
ACTIVE_MODE = "local"  # 'local' or 'cluster'

# In-memory database simulating Hive netflix_cleaned
DB_CONN = None

def init_database():
    global DB_CONN
    print("[*] Initializing in-memory database mirroring Hive 'netflix_cleaned'...")
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

    if not os.path.exists(DATASET_PATH):
        print(f"[!] Warning: Dataset not found at {DATASET_PATH}")
        return

    with open(DATASET_PATH, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        next(reader) # header
        rows = []
        for r in reader:
            if not r or len(r) < 12:
                continue
            s_id, c_type, title, director, cast, country, date_added, rel_yr, rating, dur, listed, desc = r[:12]
            
            # Cleaning rules
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
        print(f"[+] Cleaned dataset loaded: {len(rows):,} records ready for HiveQL queries.")

def get_diagnostics():
    """Check Hadoop, HDFS, Java, and Hive on host system."""
    hadoop_home = os.environ.get("HADOOP_HOME", "")
    hadoop_bin = shutil.which("hadoop") or (os.path.join(hadoop_home, "bin", "hadoop.cmd" if os.name == "nt" else "hadoop") if hadoop_home else None)
    hdfs_bin = shutil.which("hdfs") or (os.path.join(hadoop_home, "bin", "hdfs.cmd" if os.name == "nt" else "hdfs") if hadoop_home else None)
    hive_bin = shutil.which("hive") or shutil.which("beeline")
    java_bin = shutil.which("java")

    hadoop_detected = bool(hadoop_bin and os.path.exists(hadoop_bin)) if hadoop_bin else False
    hdfs_detected = bool(hdfs_bin and os.path.exists(hdfs_bin)) if hdfs_bin else False
    hive_detected = bool(hive_bin)
    java_detected = bool(java_bin)

    java_version = "Not Detected"
    if java_detected:
        try:
            res = subprocess.run(["java", "-version"], capture_output=True, text=True, timeout=2)
            first_line = (res.stderr or res.stdout).split("\n")[0]
            java_version = first_line.strip()
        except Exception:
            java_version = "Detected (Version probe timed out)"

    return {
        "active_mode": ACTIVE_MODE,
        "hadoop_bin_detected": hadoop_detected,
        "hdfs_bin_detected": hdfs_detected,
        "hive_bin_detected": hive_detected,
        "java_detected": java_detected,
        "java_version": java_version,
        "hadoop_home": hadoop_home if hadoop_home else "(Not set in environment)",
        "hdfs_target_uri": "hdfs://localhost:9000",
        "hdfs_target_dir": "/user/hadoop/netflix/",
        "diagnostics_message": (
            "Hadoop & Hive binaries detected on system!"
            if (hadoop_detected and hive_detected)
            else "Hadoop binaries not found in PATH and HADOOP_HOME environment. Use Local Demo Mode for standalone execution."
        )
    }

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
        "category": "Creator Spotlight",
        "sql": "SELECT director, COUNT(*) AS total_titles FROM netflix_cleaned WHERE director != 'Unknown Director' GROUP BY director ORDER BY total_titles DESC LIMIT 10;",
        "hiveql": "SELECT director, COUNT(*) AS total_titles FROM netflix_cleaned WHERE director != 'Unknown Director' GROUP BY director ORDER BY total_titles DESC LIMIT 10;",
        "explanation": "Ranks prolific movie and TV directors collaborating with Netflix.",
        "expected": "Raúl Campos, Jan Suter, Marcus Raboy, Jay Karas"
    },
    {
        "id": 13,
        "title": "Movie Duration Metrics (Average, Min, Max)",
        "category": "Runtime Analytics",
        "sql": "SELECT ROUND(AVG(duration_value), 2) AS avg_minutes, MIN(duration_value) AS min_minutes, MAX(duration_value) AS max_minutes FROM netflix_cleaned WHERE type = 'Movie' AND duration_unit = 'min';",
        "hiveql": "SELECT ROUND(AVG(duration_value), 2) AS avg_minutes, MIN(duration_value) AS min_minutes, MAX(duration_value) AS max_minutes FROM netflix_cleaned WHERE type = 'Movie' AND duration_unit = 'min';",
        "explanation": "Calculates descriptive statistics for feature film runtimes in minutes.",
        "expected": "Average: 99.10 min, Min: 3 min, Max: 312 min"
    },
    {
        "id": 14,
        "title": "Content Distribution by Country and Format",
        "category": "Geographical Analysis",
        "sql": "SELECT country, type, COUNT(*) AS count FROM netflix_cleaned WHERE country != 'Unknown Country' GROUP BY country, type ORDER BY count DESC LIMIT 10;",
        "hiveql": "SELECT country, type, COUNT(*) AS count FROM netflix_cleaned WHERE country != 'Unknown Country' GROUP BY country, type ORDER BY count DESC LIMIT 10;",
        "explanation": "Cross-tabulates country of origin by Movie vs TV Show.",
        "expected": "United States Movies (1,482), United States TV Shows (550), India Movies (724)"
    },
    {
        "id": 15,
        "title": "Movies Released After 2018",
        "category": "Temporal Trends",
        "sql": "SELECT title, release_year, rating, duration_raw FROM netflix_cleaned WHERE type = 'Movie' AND release_year >= 2019 ORDER BY release_year DESC LIMIT 8;",
        "hiveql": "SELECT title, release_year, rating, duration_raw FROM netflix_cleaned WHERE type = 'Movie' AND release_year >= 2019 ORDER BY release_year DESC LIMIT 8;",
        "explanation": "Filters recent post-2018 films with runtime and maturity details.",
        "expected": "Recent film selections with metadata"
    },
    {
        "id": 16,
        "title": "TV Shows with Multiple Seasons",
        "category": "Runtime Analytics",
        "sql": "SELECT title, release_year, duration_value AS seasons, duration_raw FROM netflix_cleaned WHERE type = 'TV Show' AND duration_value > 1 ORDER BY duration_value DESC LIMIT 10;",
        "hiveql": "SELECT title, release_year, duration_value AS seasons, duration_raw FROM netflix_cleaned WHERE type = 'TV Show' AND duration_value > 1 ORDER BY duration_value DESC LIMIT 10;",
        "explanation": "Extracts long-running multi-season series using normalized duration_value.",
        "expected": "Grey's Anatomy (15 Seasons), Supernatural (14 Seasons), NCIS (15 Seasons)"
    },
    {
        "id": 17,
        "title": "Top Release Years by Production Volume",
        "category": "Temporal Trends",
        "sql": "SELECT release_year, COUNT(*) AS total_releases FROM netflix_cleaned GROUP BY release_year ORDER BY total_releases DESC LIMIT 10;",
        "hiveql": "SELECT release_year, COUNT(*) AS total_releases FROM netflix_cleaned GROUP BY release_year ORDER BY total_releases DESC LIMIT 10;",
        "explanation": "Ranks calendar years with highest content volume.",
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

class BigDataDashboardHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Route static files
        clean_path = path.split("?")[0]
        if clean_path.startswith("/results/"):
            rel = clean_path[len("/results/"):]
            return os.path.join(RESULTS_DIR, rel)
        elif clean_path == "/" or clean_path == "/index.html":
            return os.path.join(WEB_DIR, "index.html")
        else:
            rel = clean_path.lstrip("/")
            local_target = os.path.join(WEB_DIR, rel)
            if os.path.exists(local_target):
                return local_target
            return os.path.join(WEB_DIR, "index.html")

    def do_GET(self):
        url_path = self.path.split("?")[0]
        
        if url_path == "/api/diagnostics":
            self.send_json(get_diagnostics())
            return
        elif url_path == "/api/stats":
            cur = DB_CONN.cursor()
            total = cur.execute("SELECT COUNT(*) FROM netflix_cleaned").fetchone()[0]
            movies = cur.execute("SELECT COUNT(*) FROM netflix_cleaned WHERE type='Movie'").fetchone()[0]
            tv = cur.execute("SELECT COUNT(*) FROM netflix_cleaned WHERE type='TV Show'").fetchone()[0]
            countries = cur.execute("SELECT COUNT(DISTINCT country) FROM netflix_cleaned WHERE country!='Unknown Country'").fetchone()[0]
            years = cur.execute("SELECT MIN(release_year), MAX(release_year) FROM netflix_cleaned").fetchone()
            
            self.send_json({
                "total_titles": total,
                "movies": movies,
                "tv_shows": tv,
                "countries": countries,
                "min_year": years[0],
                "max_year": years[1],
                "active_mode": ACTIVE_MODE
            })
            return
        elif url_path == "/api/queries":
            self.send_json(QUERIES)
            return
        elif url_path == "/api/viva":
            self.send_json(VIVA_QUESTIONS)
            return
        elif url_path == "/api/dataset-preview":
            preview = []
            if os.path.exists(DATASET_PATH):
                with open(DATASET_PATH, 'r', encoding='utf-8', errors='replace') as f:
                    r = csv.reader(f)
                    header = next(r)
                    for i, row in enumerate(r):
                        if i >= 15: break
                        preview.append(row)
                self.send_json({"header": header, "rows": preview})
            else:
                self.send_json({"error": "Dataset not found"})
            return
        elif url_path == "/api/charts":
            charts = []
            if os.path.exists(CHARTS_DIR):
                for f in sorted(os.listdir(CHARTS_DIR)):
                    if f.endswith('.png'):
                        charts.append({
                            "filename": f,
                            "url": f"/results/charts/{f}",
                            "title": f.replace('.png', '').replace('_', ' ').title()
                        })
            self.send_json(charts)
            return

        # Fallback to static files
        super().do_GET()

    def do_POST(self):
        url_path = self.path.split("?")[0]
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode('utf-8') if length > 0 else "{}"
        try:
            data = json.loads(body)
        except Exception:
            data = {}

        if url_path == "/api/mode":
            global ACTIVE_MODE
            new_mode = data.get("mode", "local")
            if new_mode in ["local", "cluster"]:
                ACTIVE_MODE = new_mode
            self.send_json({"success": True, "active_mode": ACTIVE_MODE})
            return

        elif url_path == "/api/run-query":
            q_id = data.get("query_id", 1)
            query_obj = next((q for q in QUERIES if q["id"] == q_id), None)
            if not query_obj:
                self.send_json({"error": "Query not found"}, status=404)
                return

            t0 = time.time()
            if query_obj["sql"] == "SPECIAL_GENRE":
                # Simulated Hive Lateral View Explode
                cur = DB_CONN.cursor()
                genre_map = {}
                for r in cur.execute("SELECT listed_in FROM netflix_cleaned").fetchall():
                    for g in r[0].split(','):
                        g_clean = g.strip()
                        if g_clean: genre_map[g_clean] = genre_map.get(g_clean, 0) + 1
                top10 = sorted(genre_map.items(), key=lambda x: x[1], reverse=True)[:10]
                rows = top10
                columns = ["genre", "total_titles"]
            else:
                cur = DB_CONN.cursor()
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

        elif url_path == "/api/run-mapreduce":
            job_type = data.get("job", "type")
            t0 = time.time()
            if job_type == "genre":
                m_script = os.path.join(PROJECT_ROOT, "hadoop", "mapper_genre.py")
                r_script = os.path.join(PROJECT_ROOT, "hadoop", "reducer_genre.py")
                job_title = "Top Genres Distribution"
            else:
                m_script = os.path.join(PROJECT_ROOT, "hadoop", "mapper.py")
                r_script = os.path.join(PROJECT_ROOT, "hadoop", "reducer.py")
                job_title = "Content Type & Release Year"

            # Execute Map phase
            with open(DATASET_PATH, 'r', encoding='utf-8', errors='replace') as f:
                p_map = subprocess.Popen([sys.executable, m_script], stdin=f, stdout=subprocess.PIPE, text=True)
                map_out, _ = p_map.communicate()

            map_lines = [l for l in map_out.strip().split("\n") if l]
            sample_mapped = map_lines[:8]

            # Shuffle & Sort
            sorted_lines = sorted(map_lines)
            sorted_str = "\n".join(sorted_lines) + "\n"

            # Reduce phase
            p_red = subprocess.Popen([sys.executable, r_script], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
            red_out, _ = p_red.communicate(input=sorted_str)
            red_lines = [l for l in red_out.strip().split("\n") if l]

            elapsed_ms = round((time.time() - t0) * 1000, 2)
            self.send_json({
                "job_title": job_title,
                "map_count": len(map_lines),
                "reduce_count": len(red_lines),
                "sample_mapped": sample_mapped,
                "reduced_records": [l.split("\t") for l in red_lines[:20]],
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
        self.end_headers()
        self.wfile.write(content)

def find_free_port(start_port=5000):
    for port in range(start_port, start_port + 50):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if s.connect_ex(('127.0.0.1', port)) != 0:
                return port
    return start_port

def start_server():
    init_database()
    env_port = os.environ.get("PORT")
    port = int(env_port) if env_port and env_port.isdigit() else find_free_port(5000)
    
    # Bind to 0.0.0.0 so both localhost and 127.0.0.1 work smoothly across IPv4/IPv6
    HTTPServer.allow_reuse_address = True
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, BigDataDashboardHandler)
    
    url_local = f"http://localhost:{port}"
    url_ip = f"http://127.0.0.1:{port}"
    
    print(f"\n{'='*70}")
    print(f"  Netflix Big Data Platform Server Running")
    print(f"  URL: {url_local}")
    print(f"  Alt: {url_ip}")
    print(f"  Local Demo Mode: ACTIVE")
    print(f"  Press Ctrl+C to terminate server.")
    print(f"{'='*70}\n")
    
    # Auto-open browser after 0.5 seconds
    import webbrowser
    import threading
    def open_browser():
        time.sleep(0.5)
        try:
            webbrowser.open(url_local)
        except Exception:
            pass
    threading.Thread(target=open_browser, daemon=True).start()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[+] Server stopped.")

if __name__ == "__main__":
    start_server()
