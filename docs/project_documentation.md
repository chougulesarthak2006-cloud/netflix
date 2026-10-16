# Academic Project Documentation

## Project Title
**Netflix Movies and TV Shows Data Analysis using Hadoop and Hive**

---

## 1. Abstract
The exponential growth of digital entertainment platforms has generated vast volumes of catalog and viewership data, presenting challenges for conventional relational database management systems. This academic micro-project demonstrates an end-to-end Big Data analytical pipeline using Apache Hadoop and Apache Hive to store, process, and analyze the global Netflix Movies and TV Shows dataset. The dataset comprises 6,234 media titles spanning 12 distinct attributes including content type, release year, country of production, duration, and maturity ratings.

The project implements a distributed storage architecture on Hadoop Distributed File System (HDFS), followed by schema mapping using Hive’s specialized `OpenCSVSerde` to handle text fields with embedded commas. An Extract-Load-Transform (ELT) methodology is employed: raw data is staged in an external table, cleaned to resolve missing values and compound durations, and stored in an Optimized Row Columnar (ORC) managed table. Over 18 analytical HiveQL queries are executed to extract key insights regarding content distribution, geographic production hubs, temporal acquisition trends, and audience ratings. The results showcase the power and efficiency of distributed SQL engines on Big Data clusters, providing undergraduate students with practical experience in enterprise data warehouse design.

---

## 2. Problem Statement
Traditional relational databases (such as MySQL, PostgreSQL, or Oracle) are optimized for transactional processing (OLTP) on structured data with ACID compliance. However, modern entertainment streaming providers generate semi-structured, continuously evolving, and high-volume media catalogs that require analytical processing (OLAP). Relational databases face severe performance degradation, storage bottlenecks, and vertical scaling limitations when querying multi-gigabyte or terabyte-scale datasets.

Furthermore, real-world media catalogs contain semi-structured text fields with embedded quotation marks, multiple comma-separated entries (such as composite directors and international co-productions), missing attributes, and hybrid string metrics (such as `"90 min"` versus `"3 Seasons"`). There is a critical academic and engineering need to understand how distributed storage systems (HDFS) and distributed SQL query engines (Apache Hive) solve these real-world data engineering bottlenecks in a scalable, fault-tolerant manner.

---

## 3. Project Objectives
The key objectives of this micro-project are:
1. **Understand Distributed Data Storage:** Deploy and configure the Hadoop Distributed File System (HDFS) to store and manage semi-structured CSV datasets reliably across cluster nodes.
2. **Implement Schema-on-Read Mechanics:** Design an Apache Hive External Table using `OpenCSVSerde` to parse RFC-4180 compliant CSV files with embedded commas and quotes without data corruption.
3. **Execute Data Cleansing & Normalization:** Implement ELT data-cleaning pipelines in HiveQL to standardize null/empty strings, cast data types, extract calendar years from date strings, and decompose compound durations into numeric runtimes and unit dimensions.
4. **Conduct In-Depth Analytical Querying:** Formulate and execute 18+ complex HiveQL queries to uncover meaningful business insights regarding content distribution, top producing countries, and viewer maturity demographics.
5. **Evaluate Distributed vs Relational Systems:** Analyze the architectural advantages of Hive's distributed execution (MapReduce/Tez) over standard relational databases for analytical workloads.
6. **Synthesize Reports & Visualizations:** Export distributed query aggregations to generate clear academic visual dashboards and summary reports for presentation and defense.

---

## 4. Scope of the Project
- **In Scope:**
  - Deployment and management of dataset files in HDFS directories (`/user/hadoop/netflix/`).
  - Creation and administration of Hive databases (`netflix_db`) and metadata schemas.
  - Implementation of both External (`netflix_raw`) and Managed (`netflix_cleaned`) Hive tables.
  - Conversion of text data into columnar ORC storage with Snappy compression for query acceleration.
  - Multi-dimensional data analysis using HiveQL aggregation, filtering, grouping, and user-defined table-generating functions (`LATERAL VIEW explode`).
  - Exporting analytical outputs to CSV format and generating presentation-grade charts.
- **Out of Scope:**
  - Real-time stream processing (Apache Kafka / Spark Streaming).
  - Machine learning recommendation engines (Collaborative Filtering / Matrix Factorization).
  - Multi-terabyte hardware cluster deployment (demonstrated on single-node pseudo-distributed cluster).

---

## 5. Methodology
The project follows an iterative Big Data engineering life cycle:

```
[ Data Collection ] ──> [ HDFS Ingestion ] ──> [ External Table Mapping ]
                                                         │
[ Visual Dashboards ] <── [ HiveQL Analytics ] <── [ Managed ORC Cleaning ]
```

1. **Acquisition:** The Kaggle Netflix Movies & TV Shows dataset is procured and verified on the local Linux file system.
2. **Ingestion:** Shell scripts invoke Hadoop CLI commands to upload the dataset into HDFS namespace blocks.
3. **Staging:** A Hive external table is created to define metadata schemas over the HDFS files using `OpenCSVSerde`.
4. **Transformation:** HiveQL scripts perform cleaning transformations, casting strings, populating defaults for missing values, and persisting clean data into an ORC-formatted managed table.
5. **Analytics:** Analytical queries translate declarative HiveQL into MapReduce/Tez execution plans to compute descriptive statistics.
6. **Reporting:** Query outputs are extracted and visualized as charts illustrating streaming market trends.

---

## 6. Hardware & Software Requirements

### Hardware Requirements
- **Processor:** Intel Core i3 / i5 / i7 or AMD Ryzen 5 (Minimum 2 Cores, 4 Threads; Recommended: 4+ Cores).
- **RAM:** Minimum 8 GB (Recommended: 16 GB for running Hadoop NameNode, DataNode, ResourceManager, and Hive Metastore concurrently).
- **Storage:** Minimum 20 GB free disk space (HDD or SSD; SSD highly recommended for fast I/O).

### Software Requirements
- **Operating System:** Ubuntu Linux 20.04 LTS / 22.04 LTS (or Windows 10/11 running WSL2 / VMware / VirtualBox).
- **Java Development Kit:** OpenJDK 8 (Java 1.8) or OpenJDK 11.
- **Hadoop Framework:** Apache Hadoop 2.10.x or 3.3.x.
- **Data Warehouse Software:** Apache Hive 2.3.x or 3.1.x.
- **Metastore Database:** Apache Derby (Embedded) or MySQL 8.x (Remote Metastore).
- **Scripting & Visualization:** Bash Shell, Python 3.8+, Matplotlib, Pandas.

---

## 7. System Architecture
The system follows a multi-tiered decoupled architecture separating storage from computation:

1. **Storage Tier (Hadoop HDFS):**
   - **NameNode (Master):** Maintains the directory tree and metadata mapping files to data blocks.
   - **DataNode (Worker):** Stores raw physical block files on the local filesystem and handles read/write requests.
   - **Block Architecture:** High fault tolerance via replication and sequential block scanning.

2. **Metadata Tier (Hive Metastore):**
   - Stores schema definitions, column data types, table properties, and HDFS physical URIs in an RDBMS catalog (Derby or MySQL).

3. **Compute & Query Tier (Hive Driver & Execution Engine):**
   - **Parser & Semantic Analyzer:** Validates HiveQL syntax against the Metastore catalog.
   - **Query Optimizer:** Generates optimized logical and physical execution DAG plans.
   - **Execution Engine:** Submits tasks to YARN (MapReduce or Apache Tez) for parallel distributed compute.

4. **Presentation Tier:**
   - Command-line interfaces (`hive`, `beeline`), file export drivers, and Matplotlib visualization pipelines.

---

## 8. Data Flow
1. `netflix_titles.csv` is validated on the host machine.
2. `hdfs dfs -put` streams the CSV bytes to the cluster DataNodes; NameNode records block locations.
3. `CREATE EXTERNAL TABLE` maps tabular schema to the HDFS folder without moving data.
4. `INSERT OVERWRITE TABLE netflix_cleaned SELECT ...` scans raw CSV blocks, applies data cleansing functions, and writes optimized columnar ORC files to the Hive warehouse (`/user/hive/warehouse/netflix_db.db/netflix_cleaned`).
5. Analytical HiveQL queries scan the ORC columns, aggregate data using parallel Map and Reduce tasks, and return tabular results.
6. Selected results are saved to `results/data/*.csv` and rendered into graphical plots in `results/charts/`.

---

## 9. Project Modules

### Module 1: Data Collection & Preparation
- Procured the verified Netflix Movies & TV Shows dataset comprising 6,234 records and 12 columns.
- Designed `dataset/download_dataset.py` to automate verification and generate lightweight testing samples.

### Module 2: HDFS Storage Management
- Scripted `hdfs/hdfs_commands.sh` to start Hadoop daemons, verify daemons with `jps`, create `/user/hadoop/netflix/`, stream datasets to HDFS, and check replication status.

### Module 3: Hive Database & External Table Creation
- Scripted `hive/01_create_database.sql` to initialize `netflix_db`.
- Scripted `hive/02_create_external_table.sql` deploying `org.apache.hadoop.hive.serde2.OpenCSVSerde` to parse RFC-4180 double-quoted CSV fields with embedded commas.

### Module 4: Data Cleansing & Schema Transformation
- Scripted `hive/03_data_cleaning.sql` to create `netflix_cleaned`.
- Resolved blank strings into `'Unknown Director'`, `'Unknown Cast'`, `'Unknown Country'`, and `'Unrated'`.
- Decomposed compound strings (`"90 min"` -> `90`, `'min'`) to enable numeric aggregations.
- Stored table in Snappy-compressed ORC format for storage reduction and scan speedup.

### Module 5: Big Data Analytical Querying
- Scripted `hive/04_analysis_queries.sql` comprising 18+ HiveQL queries addressing catalog composition, national production leaders, genre explosions, runtime statistics, and temporal trends.

### Module 6: Result Exportation & Visualization
- Scripted `hive/05_export_results.sql` to dump query outputs into local CSV files.
- Implemented `visualization/visualize.py` using Python and Matplotlib to render six standalone analytical charts and one unified 6-panel summary dashboard.

### Module 7: Dual-Mode Processing Engine & Interactive Web Dashboard
- Developed `app.py`, `web/index.html`, `web/styles.css`, and `web/app.js` providing an interactive Big Data management portal.
- **Local Demo Mode:** Provides zero-dependency local simulation of Hadoop MapReduce (`hadoop/run_local_mapreduce.py`) and HiveQL query execution, enabling 100% offline demonstration during viva presentations on laptops without Hadoop installed.
- **Hadoop Cluster Mode:** Integrates with physical/virtualized Hadoop clusters, probing daemons, checking `$HADOOP_HOME`, and providing terminal commands for distributed MapReduce and Hive execution.
- **Interactive Query Studio & MapReduce Visualizer:** Allows live execution of all 18 HiveQL queries and visual inspection of Map, Shuffle & Sort, and Reduce phases.

---

## 10. Advantages of the Proposed System
1. **Horizontal Scalability:** The system can expand from 6,000 records to 600,000,000 records by simply adding inexpensive commodity DataNodes, without code redesign.
2. **Schema-on-Read Flexibility:** Raw source files in HDFS remain pristine and untouched; schemas can be redefined or enriched without reloading data.
3. **High Fault Tolerance:** HDFS automatically replicates data blocks across nodes. If a DataNode hardware failure occurs, data is reconstructed from healthy replicas.
4. **Familiar SQL Interface (HiveQL):** Enables business analysts and students with SQL proficiency to harness distributed computing without writing complex low-level Java MapReduce programs.
5. **Columnar Compression:** Storing cleaned data in ORC format with Snappy compression reduces disk storage by up to 75% and accelerates analytical filtering.

---

## 11. Limitations
1. **High Latency for Single-Row Lookups:** Hive is an OLAP data warehousing system. Every query incurs MapReduce/Tez compilation and task initialization overhead, taking 5–15 seconds even for simple queries.
2. **No Real-Time Transaction Support:** Hive is not designed for frequent single-record `UPDATE` or `DELETE` operations (OLTP).
3. **Resource Consumption:** Hadoop daemons (NameNode, DataNode, NodeManager, ResourceManager) require significant baseline RAM (4–6 GB) even when idle.

---

## 12. Future Scope
1. **Apache Spark / PySpark Integration:** Migrating HiveQL queries to Spark SQL to execute processing in-memory (RAM) for 10x–100x faster query execution.
2. **Automated ETL Orchestration:** Scheduling daily data pipeline runs using Apache Airflow or Apache Oozie.
3. **Machine Learning & Recommendation Engine:** Developing a movie recommendation system using Spark MLlib or ALS (Alternating Least Squares) algorithms on the HDFS dataset.
4. **Interactive BI Dashboards:** Connecting Apache Superset, Tableau, or Power BI directly to the Hive Metastore via Hive JDBC/ODBC connectors.

---

## 13. Conclusion
The **Netflix Movies and TV Shows Data Analysis using Hadoop and Hive** micro-project successfully demonstrates how big data technologies solve large-scale data storage and analytics challenges. By combining Hadoop HDFS for reliable distributed storage and Apache Hive for SQL-based analytical transformations, the project transforms raw, semi-structured streaming catalog data into actionable business intelligence. The implementation provides practical mastery of schema-on-read modeling, custom SerDe parsing, ELT data cleansing, columnar ORC optimization, and distributed aggregations—forming an ideal foundation for academic evaluation and real-world data engineering.
