# Netflix Movies and TV Shows Data Analysis using Hadoop and Hive

[![Hadoop](https://img.shields.io/badge/Apache_Hadoop-3.3+-red.svg?logo=apachehadoop)](https://hadoop.apache.org/)
[![Hive](https://img.shields.io/badge/Apache_Hive-3.1+-orange.svg?logo=apachehive)](https://hive.apache.org/)
[![Ubuntu](https://img.shields.io/badge/OS-Ubuntu_Linux_/_Debian-E95420.svg?logo=ubuntu)](https://ubuntu.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?logo=python)](https://python.org/)
[![Academic Micro-Project](https://img.shields.io/badge/Status-Complete-brightgreen.svg)]()

> A complete, production-grade Big Data academic micro-project demonstrating distributed data storage with **Hadoop HDFS**, schema-on-read querying and data cleansing with **Apache Hive (HiveQL)**, **Hadoop MapReduce Streaming**, and an interactive **Dual-Mode Web Platform** supporting both **Local Demo Mode** and **Hadoop Cluster Mode**.

---

## 🌟 Processing Modes: Local Demo Mode vs. Hadoop Cluster Mode

This project uniquely supports two interchangeable processing engines to guarantee reliable presentation and defense under any environment:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        SELECT ACTIVE PROCESSING ENGINE                                 │
├───────────────────────────────────────────┬────────────────────────────────────────────┤
│  ⚡ LOCAL DEMO MODE [ACTIVE]              │  🐘 HADOOP CLUSTER MODE                    │
│  - Python Mapper & Reducer stream runner  │  - Real HDFS block storage (128 MB blocks) │
│  - Zero Hadoop installation required      │  - Apache Hive with OpenCSVSerde & ORC     │
│  - In-memory SQL engine mirroring Hive    │  - Hadoop Streaming JAR execution on YARN  │
│  - 100% offline, bulletproof for viva     │  - Docker Compose single-command cluster   │
└───────────────────────────────────────────┴────────────────────────────────────────────┘
```

---

## Table of Contents
1. [Abstract](#1-abstract)
2. [Problem Statement](#2-problem-statement)
3. [Objectives](#3-objectives)
4. [Dual Execution Modes (Local vs Cluster)](#4-dual-execution-modes-local-vs-cluster)
5. [Interactive Web Dashboard & Platform](#5-interactive-web-dashboard--platform)
6. [Technologies Used](#6-technologies-used)
7. [System Requirements](#7-system-requirements)
8. [Dataset Description](#8-dataset-description)
9. [System Architecture & Workflow](#9-system-architecture--workflow)
10. [Hadoop MapReduce Streaming Implementation](#10-hadoop-mapreduce-streaming-implementation)
11. [Installation & Prerequisites](#11-installation--prerequisites)
12. [Hadoop Configuration Requirements](#12-hadoop-configuration-requirements)
13. [Step-by-Step Execution Guide](#13-step-by-step-execution-guide)
    - [Option A: 1-Click Interactive Web Platform](#option-a-1-click-interactive-web-platform)
    - [Option B: Automated Local Terminal Pipeline](#option-b-automated-local-terminal-pipeline)
    - [Option C: Real Hadoop & Hive Cluster Execution](#option-c-real-hadoop--hive-cluster-execution)
14. [HiveQL Analytical Queries & Results (18+ Queries)](#14-hiveql-analytical-queries--results-18-queries)
15. [Visual Dashboard & Charts](#15-visual-dashboard--charts)
16. [Project Folder Structure](#16-project-folder-structure)
17. [Academic Documentation & 35 Viva Q&As](#17-academic-documentation--35-viva-qas)
18. [Future Scope & Conclusion](#18-future-scope--conclusion)

---

## 1. Abstract
The exponential expansion of on-demand digital entertainment platforms has generated unprecedented volumes of media catalog and consumption metadata. Traditional relational database management systems (RDBMS) struggle with analytical scalability, unstructured text fields, and high-volume batch processing. 

This academic micro-project demonstrates an end-to-end Big Data analytical solution for the global Netflix Movies and TV Shows catalog (6,234 records, 12 attributes) utilizing **Apache Hadoop HDFS** and **Apache Hive**. Raw CSV data is ingested into HDFS and mapped to a Hive External Table using `OpenCSVSerde` to parse double-quoted fields with embedded commas. An Extract-Load-Transform (ELT) pattern cleans missing data, decomposes compound duration strings, and ingests the data into an optimized columnar ORC Managed Table with Snappy compression. Eighteen analytical HiveQL queries evaluate content distribution, geographic production hotspots, maturity ratings, and platform growth velocity.

---

## 2. Problem Statement
Commercial streaming giants such as Netflix manage diverse, semi-structured catalog metadata where single attributes often contain multiple composite values (e.g., international co-production countries, multi-director credits, and variable duration metrics like `"90 min"` versus `"3 Seasons"`). Conventional relational database engines like MySQL face vertical scaling limitations, storage bottlenecks, and query performance degradation on analytical aggregation tasks.

The challenge is to design a fault-tolerant, horizontally scalable Big Data pipeline that:
- Securely stores semi-structured CSV data across distributed file blocks.
- Employs Schema-on-Read with RFC-4180 compliance to prevent column corruption.
- Transforms raw dirty strings into clean analytical metrics using HiveQL.
- Executes parallel distributed aggregations to deliver business intelligence.

---

## 3. Objectives
- **Demonstrate Distributed Storage:** Configure Hadoop HDFS for data block distribution, replication, and fault tolerance.
- **Implement Schema-on-Read:** Utilize Apache Hive with `OpenCSVSerde` to ingest quoted CSV data without column bleeding.
- **Perform In-Engine Data Cleansing:** Standardize null/empty strings, cast data types, and normalize compound duration strings directly via HiveQL.
- **Formulate 18+ Analytical Queries:** Compute critical metrics regarding content type ratios, country-wise volume, maturity demographics, and runtime averages.
- **Leverage Columnar Optimization:** Store cleaned data in ORC format with Snappy compression for query acceleration and storage savings.
- **Synthesize Reports & Dashboards:** Export query results to CSV and generate publication-quality visual charts.

---

## 4. Dual Execution Modes (Local vs Cluster)

A common obstacle in college viva presentations is the inability to run resource-heavy Hadoop clusters on classroom presentation laptops. To solve this, this project features **Dual-Engine Architecture**:

### 1. Local Demo Mode (Default, Recommended for Presentations)
- **Engine:** Python MapReduce Stream Runner + In-memory SQL engine mirroring Hive.
- **Prerequisites:** Python 3.8+ (Zero Hadoop / Java installation required).
- **Behavior:**
  - Emulates HDFS input splits, mapper streaming, key sorting, and reducer aggregations.
  - Applies identical data cleansing logic (handling empty strings, casting types, extracting `added_year`, splitting `"90 min"` and `"3 Seasons"`).
  - Executes all 18 HiveQL analytical queries with sub-millisecond response times.
  - Generates all 7 high-resolution presentation charts.

### 2. Hadoop Cluster Mode (Distributed Enterprise Execution)
- **Engine:** Apache Hadoop 3.x (HDFS, YARN) + Apache Hive 3.x (or Docker cluster).
- **Prerequisites:** Java 8/11, Hadoop daemons, and Hive metastore.
- **Behavior:**
  - Files are stored in HDFS under `/user/hadoop/netflix/` across 128 MB blocks.
  - Queries are submitted to HiveQL and compiled into distributed MapReduce or Apache Tez DAGs.
  - Distributed streaming jobs execute using Hadoop Streaming JAR with `hadoop/mapper.py` and `hadoop/reducer.py`.

---

## 5. Interactive Web Dashboard & Platform

An interactive, modern dark-themed web platform is included to provide a visual interface for both students and examiners:

- **Launch Command:** `python app.py` (or double-click `run_dashboard.bat` on Windows / `./run_dashboard.sh` on Linux).
- **URL:** `http://localhost:5000`
- **Key Tabs & Capabilities:**
  1. **⚙️ Engine & Cluster Settings:** Real-time Hadoop diagnostics, live binary detection (`hadoop`, `hdfs`, `hive`, `java`), and quick copy-pasteable terminal commands.
  2. **📊 Analytics & Charts:** Live KPI counters (6,234 titles, 68.4% movies, 31.6% TV shows, 72 countries) and interactive zoomable gallery of all 7 analytical charts.
  3. **⚡ HiveQL Query Studio:** Interactive studio to browse, inspect, and execute all 18+ HiveQL queries in real-time with formatted output tables.
  4. **🔄 MapReduce Visualizer:** Step-by-step MapReduce pipeline simulation displaying mapper output, shuffle/sort, and reducer aggregates.
  5. **🏛️ HDFS & Architecture:** Visual breakdown of the 5-stage ELT architecture, HDFS block sizes, and OpenCSVSerde mechanics.
  6. **🎓 Viva Voce Coach:** Searchable flashcards covering 35 oral exam questions and answers.

---

## 6. Technologies Used
| Technology | Category | Purpose in Project |
|---|---|---|
| **Ubuntu Linux** (20.04/22.04) | Operating System | Host environment for Hadoop ecosystem |
| **Apache Hadoop (HDFS)** | Distributed Storage | Reliable, fault-tolerant block-based file storage |
| **Apache Hive** | Data Warehouse | SQL query abstraction and schema management over HDFS |
| **HiveQL (HQL)** | Query Language | Declarative SQL queries compiled into MapReduce/Tez jobs |
| **Hadoop Streaming** | Distributed Compute | Runs Python mapper and reducer scripts on Hadoop cluster |
| **OpenCSVSerde** | Deserializer | RFC-4180 CSV parsing handling embedded commas & quotes |
| **ORC + Snappy** | Storage Format | High-compression columnar storage for clean analytical table |
| **Python / Matplotlib / Pandas** | Visualization & UI | Interactive web platform & graphical charts |
| **Bash Shell** | Automation | Scripting Hadoop daemons, HDFS uploads, and pipeline jobs |

## 5. System Requirements
### Hardware
- **Processor:** 64-bit x86 Dual-Core CPU (Quad-core recommended).
- **RAM:** Minimum 8 GB (16 GB recommended for running Hadoop + Hive concurrently).
- **Disk Space:** 20 GB free space (SSD recommended).

### Software
- **Operating System:** Ubuntu 20.04 LTS / 22.04 LTS (or Windows 10/11 with WSL2).
- **Java:** OpenJDK 8 (`java-8-openjdk-amd64`) or OpenJDK 11.
- **Hadoop:** Apache Hadoop 2.10.x or 3.3.x.
- **Hive:** Apache Hive 2.3.x or 3.1.x.
- **Python:** Python 3.8+ with Matplotlib and Pandas (for charts).

---

## 6. Dataset Description
- **Dataset File:** `dataset/netflix_titles.csv`
- **Total Records:** 6,234 titles (plus 1 header row)
- **Source:** Kaggle Netflix Movies and TV Shows Dataset (Flixable)
- **Attributes (12 columns):**
  1. `show_id`: Unique identifier (e.g., `81145628`)
  2. `type`: Program format (`Movie` or `TV Show`)
  3. `title`: Title of the movie or television series
  4. `director`: Director name(s) (contains embedded commas)
  5. `cast`: Leading actors/actresses (comma-separated list)
  6. `country`: Country of production (contains embedded commas)
  7. `date_added`: Date published on Netflix (e.g., `"September 9, 2019"`)
  8. `release_year`: Calendar year of original production release
  9. `rating`: Content age rating (`TV-MA`, `TV-14`, `PG-13`, `R`, etc.)
  10. `duration`: Runtime (`"90 min"` or `"3 Seasons"`)
  11. `listed_in`: Platform genre categories (e.g., `"Comedies, Dramas"`)
  12. `description`: Storyline synopsis

---

## 7. System Architecture & Workflow

```
[ Netflix CSV Dataset ] ── (Local Download & Verification)
           │
           ▼
[ Local Linux File System ] (/home/hadoop/Netflix-Hadoop-Hive/dataset/)
           │
           ▼ (hdfs dfs -put)
[ Hadoop HDFS ] (/user/hadoop/netflix/netflix_titles.csv)
           │
           ▼ (OpenCSVSerde Schema-on-Read)
[ Hive External Raw Table ] (netflix_db.netflix_raw)
           │
           ▼ (Data Cleansing & Duration Parsing: INSERT OVERWRITE)
[ Hive Managed Clean Table ] (netflix_db.netflix_cleaned [ORC + Snappy])
           │
           ▼ (Distributed Query Execution: MapReduce / Tez)
[ 18+ Analytical HiveQL Queries ]
           │
           ▼ (INSERT OVERWRITE LOCAL DIRECTORY)
[ Exported Result Datasets ] (results/data/*.csv)
           │
           ▼ (visualize.py)
[ Graphical Charts & Dashboards ] (results/charts/*.png)
```

---

## 8. Installation & Prerequisites

### 1. Java Installation (Ubuntu/Linux)
```bash
sudo apt update
sudo apt install -y openjdk-8-jdk
java -version
```

### 2. Configure Environment Variables in `~/.bashrc`
Add the following lines to your `~/.bashrc`:
```bash
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export HADOOP_HOME=/usr/local/hadoop
export HADOOP_INSTALL=$HADOOP_HOME
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_COMMON_HOME=$HADOOP_HOME
export HADOOP_HDFS_HOME=$HADOOP_HOME
export YARN_HOME=$HADOOP_HOME
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
export HIVE_HOME=/usr/local/hive

export PATH=$PATH:$JAVA_HOME/bin:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$HIVE_HOME/bin
```
Reload your environment:
```bash
source ~/.bashrc
```

---

## 9. Hadoop Configuration Requirements

Ensure the following configuration files in `$HADOOP_HOME/etc/hadoop/` are set:

### `core-site.xml`
```xml
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost:9000</value>
    </property>
</configuration>
```

### `hdfs-site.xml`
```xml
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
</configuration>
```

---

## 10. Step-by-Step Execution Guide

### Step 1: Dataset Setup
Verify the dataset or download a fresh copy using the helper script:
```bash
cd Netflix-Hadoop-Hive/dataset
python3 download_dataset.py
```

### Step 2: Hadoop HDFS Commands
Start Hadoop daemons and upload the dataset using the provided script:
```bash
cd ../hdfs
chmod +x hdfs_commands.sh setup_hadoop_env.sh

# 1. Start Hadoop services
./hdfs_commands.sh start

# 2. Check running daemons
./hdfs_commands.sh status

# 3. Create HDFS directory and upload data
./hdfs_commands.sh all
```

#### Manual HDFS Command Reference:
```bash
# Start daemons
start-dfs.sh
start-yarn.sh

# Verify daemons (Must show NameNode, DataNode, SecondaryNameNode, ResourceManager, NodeManager)
jps

# Create HDFS directory (Username configurable)
hdfs dfs -mkdir -p /user/hadoop/netflix/

# Upload the CSV dataset
hdfs dfs -put -f ../dataset/netflix_titles.csv /user/hadoop/netflix/

# List and verify the uploaded file
hdfs dfs -ls -h /user/hadoop/netflix/

# Inspect first 10 rows
hdfs dfs -cat /user/hadoop/netflix/netflix_titles.csv | head -n 10
```

---

### Step 3: Hive Database & External Table Creation
Start the Hive CLI or execute the scripts directly:
```bash
cd ../hive

# Create netflix_db
hive -f 01_create_database.sql

# Create netflix_raw (External table with OpenCSVSerde)
hive -f 02_create_external_table.sql
```

**Why OpenCSVSerde?**
Standard Hive `ROW FORMAT DELIMITED FIELDS TERMINATED BY ','` fails because movie descriptions, casts, and countries contain commas inside double quotes (e.g. `"United States, India, South Korea"`). `OpenCSVSerde` parses quoted tokens according to RFC-4180 standards.

---

### Step 4: Data Cleansing & Managed Table Ingestion
Run the cleaning script:
```bash
hive -f 03_data_cleaning.sql
```
This script executes:
1. Replacement of empty strings (`""`) with `'Unknown Director'`, `'Unknown Cast'`, `'Unknown Country'`, and `'Unrated'`.
2. Casting of `release_year` to `INT`.
3. Extraction of `added_year` from date strings (e.g. `"September 9, 2019"` $\rightarrow$ `2019`).
4. Decomposition of compound duration strings into `duration_value` (`INT`) and `duration_unit` (`STRING`).
5. Storage of cleaned records into an **ORC** table with **Snappy compression**.

---

### Step 5: Analytical HiveQL Queries
Run all 18 analytical queries:
```bash
hive -f 04_analysis_queries.sql
```
Or run the all-in-one automation runner:
```bash
chmod +x run_all_hive.sh
./run_all_hive.sh
```

---

### Step 6: Visualization & Reporting
Export results to CSV (already performed or via `05_export_results.sql`) and render visual charts:
```bash
cd ../visualization
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python3 visualize.py
```
All charts will be saved directly into `results/charts/`.

---

## 11. HiveQL Analytical Queries & Results

Below are the 18 core analytical queries with their HiveQL syntax and actual results from the dataset:

### Query 1: Total Titles in Catalog
```sql
SELECT COUNT(*) AS total_titles FROM netflix_cleaned;
```
**Output:** `6234`

---

### Query 2: Number of Movies
```sql
SELECT COUNT(*) AS total_movies FROM netflix_cleaned WHERE type = 'Movie';
```
**Output:** `4265`

---

### Query 3: Number of TV Shows
```sql
SELECT COUNT(*) AS total_tv_shows FROM netflix_cleaned WHERE type = 'TV Show';
```
**Output:** `1969`

---

### Query 4: Movies vs TV Shows Comparison
```sql
SELECT type, COUNT(*) AS count, ROUND(COUNT(*) * 100.0 / 6234, 2) AS percentage
FROM netflix_cleaned
GROUP BY type;
```
**Output:**
| type | count | percentage |
|---|---|---|
| Movie | 4265 | 68.42% |
| TV Show | 1969 | 31.58% |

---

### Query 5: Titles by Release Year (Recent Decade)
```sql
SELECT release_year, COUNT(*) AS title_count 
FROM netflix_cleaned 
GROUP BY release_year 
ORDER BY release_year DESC 
LIMIT 10;
```
**Output:**
| release_year | title_count |
|---|---|
| 2020 | 25 |
| 2019 | 843 |
| 2018 | 1063 |
| 2017 | 959 |
| 2016 | 830 |
| 2015 | 517 |

---

### Query 6: Top 10 Content Producing Countries
```sql
SELECT country, COUNT(*) AS total_titles 
FROM netflix_cleaned 
WHERE country != 'Unknown Country' 
GROUP BY country 
ORDER BY total_titles DESC 
LIMIT 10;
```
**Output:**
| country | total_titles |
|---|---|
| United States | 2032 |
| India | 777 |
| United Kingdom | 348 |
| Japan | 176 |
| Canada | 141 |
| South Korea | 136 |
| Spain | 117 |
| France | 90 |
| Mexico | 83 |
| Turkey | 79 |

---

### Query 7: Most Common Content Ratings
```sql
SELECT rating, COUNT(*) AS total_titles 
FROM netflix_cleaned 
GROUP BY rating 
ORDER BY total_titles DESC 
LIMIT 7;
```
**Output:**
| rating | total_titles |
|---|---|
| TV-MA | 2027 |
| TV-14 | 1698 |
| TV-PG | 701 |
| R | 508 |
| PG-13 | 286 |
| NR | 218 |
| PG | 184 |

---

### Query 8: Top 10 Genres (Using LATERAL VIEW explode)
```sql
SELECT TRIM(genre) AS genre, COUNT(*) AS title_count 
FROM netflix_cleaned 
LATERAL VIEW explode(split(listed_in, ',')) genre_table AS genre 
WHERE TRIM(genre) != '' 
GROUP BY TRIM(genre) 
ORDER BY title_count DESC 
LIMIT 10;
```
**Output:**
| genre | title_count |
|---|---|
| International Movies | 1927 |
| Dramas | 1623 |
| Comedies | 1113 |
| International TV Shows | 1001 |
| Documentaries | 668 |
| TV Dramas | 599 |
| Action & Adventure | 597 |
| Independent Movies | 552 |
| TV Comedies | 436 |
| Thrillers | 392 |

---

### Query 9: Titles Added by Year (Ingestion Velocity)
```sql
SELECT added_year, COUNT(*) AS titles_added 
FROM netflix_cleaned 
WHERE added_year IS NOT NULL 
GROUP BY added_year 
ORDER BY added_year ASC;
```
**Output:**
| added_year | titles_added |
|---|---|
| 2015 | 90 |
| 2016 | 456 |
| 2017 | 1300 |
| 2018 | 1782 |
| 2019 | 2349 |

---

### Query 10: Oldest Titles in the Catalog
```sql
SELECT title, type, release_year, country 
FROM netflix_cleaned 
ORDER BY release_year ASC 
LIMIT 5;
```
**Output:**
| title | type | release_year | country |
|---|---|---|---|
| Pioneers: First Women Filmmakers* | TV Show | 1925 | Unknown Country |
| Prelude to War | Movie | 1942 | United States |
| The Battle of Midway | Movie | 1942 | United States |
| Undercover: How to Operate Behind Enemy Lines | Movie | 1943 | United States |
| Why We Fight: The Battle of Russia | Movie | 1943 | United States |

---

### Query 11: Newest Titles Based on Release Year
```sql
SELECT title, type, release_year, country 
FROM netflix_cleaned 
ORDER BY release_year DESC 
LIMIT 5;
```
**Output:**
| title | type | release_year | country |
|---|---|---|---|
| Maradona in Mexico | TV Show | 2020 | Argentina, United States, Mexico |
| Bulletproof 2 | Movie | 2020 | United States |
| Cheer | TV Show | 2020 | United States |
| Live Twice, Love Once | Movie | 2020 | Spain |
| Dracula | TV Show | 2020 | United Kingdom |

---

### Query 12: Top 10 Directors
```sql
SELECT director, COUNT(*) AS total_titles 
FROM netflix_cleaned 
WHERE director != 'Unknown Director' 
GROUP BY director 
ORDER BY total_titles DESC 
LIMIT 6;
```
**Output:**
| director | total_titles |
|---|---|
| Raúl Campos, Jan Suter | 18 |
| Marcus Raboy | 14 |
| Jay Karas | 13 |
| Jay Chapman | 12 |
| Steven Spielberg | 9 |
| Martin Scorsese | 9 |

---

### Query 13: Average Movie Duration Metrics
```sql
SELECT 
    ROUND(AVG(duration_value), 2) AS avg_duration_minutes,
    MIN(duration_value) AS min_duration,
    MAX(duration_value) AS max_duration
FROM netflix_cleaned 
WHERE type = 'Movie' AND duration_unit = 'min';
```
**Output:**
- **Average Duration:** `99.10 minutes` (~1h 39m)
- **Minimum Duration:** `3 minutes`
- **Maximum Duration:** `312 minutes`

---

### Query 14: Distribution of Content by Country and Type
```sql
SELECT country, type, COUNT(*) AS total_count 
FROM netflix_cleaned 
WHERE country != 'Unknown Country' 
GROUP BY country, type 
ORDER BY total_count DESC 
LIMIT 5;
```
**Output:**
| country | type | total_count |
|---|---|---|
| United States | Movie | 1482 |
| India | Movie | 724 |
| United States | TV Show | 550 |
| United Kingdom | TV Show | 178 |
| United Kingdom | Movie | 170 |

---

### Query 15: Movies Released in or after 2019
```sql
SELECT title, release_year, rating, duration_raw 
FROM netflix_cleaned 
WHERE type = 'Movie' AND release_year >= 2019 
ORDER BY release_year DESC 
LIMIT 5;
```
**Output:** Displays recent feature films like *The Irishman* (209 min), *Marriage Story* (137 min), and *Norm of the North* (90 min).

---

### Query 16: Longest Running TV Shows (Multi-Season)
```sql
SELECT title, release_year, duration_value, duration_raw 
FROM netflix_cleaned 
WHERE type = 'TV Show' AND duration_value > 1 
ORDER BY duration_value DESC 
LIMIT 5;
```
**Output:**
| title | release_year | duration_value | duration_raw |
|---|---|---|---|
| Grey's Anatomy | 2018 | 15 | 15 Seasons |
| NCIS | 2017 | 15 | 15 Seasons |
| Supernatural | 2019 | 14 | 14 Seasons |
| COMEDIANS of the world | 2019 | 13 | 13 Seasons |
| Red vs. Blue | 2015 | 13 | 13 Seasons |

---

### Query 17: Top Release Years by Volume
```sql
SELECT release_year, COUNT(*) AS release_count 
FROM netflix_cleaned 
GROUP BY release_year 
ORDER BY release_count DESC 
LIMIT 5;
```
**Output:**
| release_year | release_count |
|---|---|
| 2018 | 1063 |
| 2017 | 959 |
| 2019 | 843 |
| 2016 | 830 |
| 2015 | 517 |

---

### Query 18: Content Distribution by Rating and Type
```sql
SELECT rating, type, COUNT(*) AS content_count 
FROM netflix_cleaned 
GROUP BY rating, type 
ORDER BY content_count DESC 
LIMIT 5;
```
**Output:**
| rating | type | content_count |
|---|---|---|
| TV-MA | Movie | 1348 |
| TV-14 | Movie | 1038 |
| TV-MA | TV Show | 679 |
| TV-14 | TV Show | 660 |
| R | Movie | 506 |

---

## 12. Visual Dashboard

All visualizations are generated from the query result CSV files in `results/data/` using `visualization/visualize.py`:

- **Unified 6-Panel Dashboard:** `results/charts/netflix_analysis_dashboard.png`
- **Standalone Charts:**
  1. `01_movies_vs_tv_shows.png`: Donut chart of catalog breakdown
  2. `02_releases_by_year.png`: Trendline of titles from 2000 to 2020
  3. `03_top_10_countries.png`: Bar chart of top content-producing nations
  4. `04_ratings_distribution.png`: Bar chart of maturity classifications
  5. `05_top_10_genres.png`: Bar chart of most popular catalog genres
  6. `06_titles_added_by_year.png`: Ingestion velocity over the last decade

---

## 13. Project Folder Structure

```text
Netflix-Hadoop-Hive/
│
├── dataset/
│   ├── netflix_titles.csv          # Full verified dataset (6,234 records, 2.4 MB)
│   ├── sample_netflix_titles.csv   # 25-row sample for quick testing
│   ├── download_dataset.py         # Dataset verification/download script
│   └── dataset_info.md             # Schema and attribute dictionary
│
├── hadoop/
│   ├── mapper.py                   # Hadoop Streaming Mapper (Content Type & Release Year)
│   ├── reducer.py                  # Hadoop Streaming Reducer (Type & Year Aggregation)
│   ├── mapper_genre.py             # Hadoop Streaming Mapper for Exploded Genres
│   ├── reducer_genre.py            # Hadoop Streaming Reducer for Genre Frequencies
│   └── run_local_mapreduce.py      # Local MapReduce pipeline simulator (Local Demo Mode)
│
├── hdfs/
│   ├── hdfs_commands.sh            # Parameterized HDFS operations script
│   └── setup_hadoop_env.sh         # Environment variable verification helper
│
├── hive/
│   ├── 01_create_database.sql      # Hive database initialization (netflix_db)
│   ├── 02_create_external_table.sql# External table with OpenCSVSerde (netflix_raw)
│   ├── 03_data_cleaning.sql        # Data cleansing & ORC managed table (netflix_cleaned)
│   ├── 04_analysis_queries.sql     # 18+ comprehensive HiveQL analytical queries
│   ├── 05_export_results.sql       # Query result export to CSV
│   └── run_all_hive.sh             # Linux automated pipeline runner
│
├── web/
│   ├── index.html                  # Modern dark-themed Big Data web application
│   ├── styles.css                  # Custom styling (glassmorphism, dark cards, terminal UI)
│   └── app.js                      # Live query runner, mode switcher, and visualizer logic
│
├── results/
│   ├── README.md                   # Analytical findings and executive report
│   ├── data/                       # Exported query results (CSV format)
│   │   ├── q1_content_type_distribution.csv
│   │   ├── q2_releases_by_year.csv
│   │   ├── q3_top_10_countries.csv
│   │   ├── q4_top_ratings.csv
│   │   ├── q5_top_genres.csv
│   │   ├── q6_added_by_year.csv
│   │   ├── q7_top_directors.csv
│   │   └── q8_movie_duration_stats.csv
│   └── charts/                     # Rendered high-resolution PNG charts
│       ├── 01_movies_vs_tv_shows.png
│       ├── 02_releases_by_year.png
│       ├── 03_top_10_countries.png
│       ├── 04_ratings_distribution.png
│       ├── 05_top_10_genres.png
│       ├── 06_titles_added_by_year.png
│       └── netflix_analysis_dashboard.png
│
├── visualization/
│   ├── visualize.py                # Python chart generator (Matplotlib / Seaborn)
│   └── requirements.txt            # Matplotlib, Pandas, Seaborn
│
├── docs/
│   ├── project_documentation.md    # Full academic project report (13 sections)
│   ├── viva_questions.md           # 35+ Viva questions and answers
│   └── architecture_diagram.md     # Architectural pipeline documentation
│
├── app.py                          # Dual-mode backend server & API (Local + Cluster)
├── run_dashboard.bat               # Windows 1-Click launcher for Web Dashboard
├── run_dashboard.sh                # Linux/Ubuntu 1-Click launcher for Web Dashboard
├── run_project.bat                 # Windows 1-Click pipeline runner
├── run_project.py                  # Master CLI pipeline runner (--web, --mapreduce, --cli)
└── README.md                       # Master project guide (this file)
```

---

## 14. Future Scope
1. **In-Memory Acceleration with Apache Spark:** Porting queries to PySpark / Spark SQL to process data directly in memory for 10x speed improvements.
2. **Automated Pipeline Scheduling:** Employing Apache Airflow DAGs to orchestrate daily ingestion, transformation, and alerting.
3. **Machine Learning Recommendation Engine:** Implementing Collaborative Filtering or Content-Based Recommendation using Spark MLlib.
4. **Interactive BI Dashboards:** Connecting Apache Superset or Tableau to Hive Metastore via JDBC.

---

## 15. Conclusion
This project successfully demonstrates an enterprise Big Data architecture for streaming media analysis. By storing the Netflix catalog in Hadoop HDFS and analyzing it with Apache Hive and HiveQL, the project resolves critical semi-structured data ingestion challenges, demonstrates schema-on-read modeling, performs robust data cleansing, and executes distributed analytical queries. The project delivers valuable business insights into Netflix's global expansion, content curation, and demographic focus, serving as an ideal practical project for academic evaluation.

---

## 16. Academic Documentation & Viva Guide
- For the full 13-section academic project report, refer to [project_documentation.md](file:///C:/Netflix-Hadoop-Hive/docs/project_documentation.md).
- For the complete 35-question oral viva preparation guide, refer to [viva_questions.md](file:///C:/Netflix-Hadoop-Hive/docs/viva_questions.md).
- For detailed architecture blueprints and Mermaid flowcharts, refer to [architecture_diagram.md](file:///C:/Netflix-Hadoop-Hive/docs/architecture_diagram.md).
