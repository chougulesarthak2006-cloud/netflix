# Netflix Big Data Project: Comprehensive Viva Questions & Answers

This guide contains **35 essential viva questions and answers** prepared specifically for college students defending this project. The answers are written in clear, simple, and technically accurate language that is easy to recall and speak during an oral examination.

---

### Q1. What is Big Data?
**Answer:**
Big Data refers to extremely large, complex, and fast-growing datasets that cannot be stored, processed, or analyzed efficiently using traditional database systems like MySQL. Big Data is characterized by the **5 V's**:
1. **Volume:** Immense amount of data (Gigabytes, Terabytes, Petabytes).
2. **Velocity:** Speed at which new data is generated.
3. **Variety:** Different data formats (Structured, Semi-Structured like CSV/JSON, Unstructured like video).
4. **Veracity:** Trustworthiness and quality of the data.
5. **Value:** Actionable business insights extracted from the data.

---

### Q2. What is Apache Hadoop?
**Answer:**
Apache Hadoop is an open-source software framework designed for distributed storage and distributed processing of very large datasets across clusters of commodity hardware (standard computers). It allows hundreds or thousands of computers to work together as a single supercomputer.

---

### Q3. What are the core components of Apache Hadoop?
**Answer:**
Hadoop has three core components:
1. **HDFS (Hadoop Distributed File System):** The distributed storage layer that stores data across multiple machines.
2. **YARN (Yet Another Resource Negotiator):** The cluster resource management layer that allocates CPU and RAM.
3. **MapReduce:** The distributed computational processing engine that processes data in parallel using Map and Reduce phases.

---

### Q4. What is HDFS and how does it work?
**Answer:**
HDFS stands for **Hadoop Distributed File System**. It is a distributed file system inspired by the Google File System (GFS). It breaks large files into fixed-size chunks called **data blocks** (default 128 MB) and distributes them across multiple machines (DataNodes) with replication for fault tolerance.

---

### Q5. What is the architecture of HDFS?
**Answer:**
HDFS follows a **Master-Worker (Master-Slave) Architecture**:
- **NameNode (Master):** Manages the file system namespace, directory hierarchy, and tracks which blocks belong to which file and on which DataNodes they reside.
- **DataNodes (Workers):** Store the actual data blocks on local physical disks and perform read/write requests instructed by the NameNode.
- **Secondary NameNode:** Periodically merges the NameNode's edit log (`edits`) with the file system image (`fsimage`) to keep the metadata clean and prevent NameNode startup delays.

---

### Q6. What is a Block in HDFS? What is the default block size?
**Answer:**
A block is the minimum continuous unit of data storage in HDFS.
- In Hadoop 1.x, the default block size was **64 MB**.
- In Hadoop 2.x and 3.x, the default block size is **128 MB** (configurable to 256 MB or higher).
Large block sizes minimize the disk seek overhead and keep the NameNode's RAM metadata footprint small.

---

### Q7. What is Replication and the Replication Factor in HDFS?
**Answer:**
Replication is the process of making multiple copies of each data block to protect against hardware failure.
- The default **Replication Factor** in a production Hadoop cluster is **3**.
- In a production cluster, Block 1 is stored on DataNode A (local rack), a second copy on DataNode B (different rack), and a third copy on DataNode C (same remote rack).
- In a student single-node setup (pseudo-distributed mode), the replication factor is set to **1** because only one DataNode exists.

---

### Q8. What happens when a file is uploaded to HDFS using `hdfs dfs -put`?
**Answer:**
1. The client contacts the **NameNode** requesting to create a new file.
2. The NameNode checks permissions and returns a list of healthy DataNodes that can receive the first block.
3. The client splits the local file into 128 MB blocks and streams the first block directly to the first DataNode.
4. The first DataNode pipelines and replicates the block to the second and third DataNodes.
5. Once all replicas are acknowledged, the NameNode records the block locations in its metadata.

---

### Q9. What happens if a DataNode fails in HDFS?
**Answer:**
Each DataNode sends a **heartbeat signal** to the NameNode every 3 seconds. If the NameNode stops receiving heartbeats from a DataNode for 10 minutes, it marks that node as dead. The NameNode immediately identifies the blocks that were on that failed node, locates healthy copies on other DataNodes, and instructs them to replicate those blocks to restore the desired replication factor. No data is lost.

---

### Q10. What is Apache Hive?
**Answer:**
Apache Hive is a distributed data warehouse software built on top of Apache Hadoop. It provides data summarization, ad-hoc querying, and analysis of large datasets stored in HDFS using an SQL-like query language called **HiveQL (HQL)**.

---

### Q11. What is the difference between Hadoop and Hive?
**Answer:**
- **Hadoop** is the foundational infrastructure framework providing the distributed file system (HDFS) and compute engine (MapReduce/YARN).
- **Hive** is a data warehousing abstraction layer that sits *on top* of Hadoop. Instead of writing 100+ lines of complex Java MapReduce code, Hive allows developers to write simple SQL queries which it automatically converts into MapReduce/Tez jobs.

---

### Q12. Why did we use Hive instead of MySQL for this project?
**Answer:**
| Feature | MySQL (RDBMS) | Apache Hive (Big Data Warehouse) |
|---|---|---|
| **Primary Workload** | OLTP (Online Transaction Processing) | OLAP (Online Analytical Processing) |
| **Data Size** | Gigabytes (single server) | Terabytes to Petabytes (distributed cluster) |
| **Scalability** | Vertical Scaling (expensive bigger hardware) | Horizontal Scaling (add cheap commodity PCs) |
| **Transactions** | High-speed single-row INSERT/UPDATE | Batch processing / Full table scans |
| **Storage** | Local structured database engine | Distributed files in HDFS (CSV, ORC, Parquet) |

MySQL is meant for day-to-day transaction processing (like booking a ticket or logging in). Hive is meant for massive historical batch analytics (like analyzing 10 years of Netflix streaming patterns across 50 countries).

---

### Q13. Why use the Netflix dataset for a Big Data project?
**Answer:**
The Netflix dataset contains a realistic mix of structured columns (`release_year`, `rating`), semi-structured text (`listed_in`, `cast`, `director`), missing fields, and composite strings (`"90 min"` and `"3 Seasons"`). It perfectly demonstrates real-world data engineering challenges: Schema-on-Read, handling embedded delimiters, custom SerDes, and multi-dimensional aggregations.

---

### Q14. What is HiveQL?
**Answer:**
HiveQL (Hive Query Language) is Hive’s dialect of SQL. It supports standard SQL clauses like `SELECT`, `FROM`, `WHERE`, `GROUP BY`, `ORDER BY`, `JOIN`, and aggregations (`COUNT`, `AVG`, `MAX`), as well as Big Data features like `LATERAL VIEW explode()`, partitioning, and bucketing.

---

### Q15. What is the Hive Metastore?
**Answer:**
The Hive Metastore is a central repository (database) that stores metadata about Hive tables, such as table names, column names, data types, SerDe properties, and the physical HDFS file location. Hive typically uses an RDBMS like Derby or MySQL to store this metadata.

---

### Q16. What is Schema-on-Read vs Schema-on-Write?
**Answer:**
- **Schema-on-Write (Traditional RDBMS like MySQL):** The schema is enforced when data is inserted. If an inserted row has the wrong data type or too many columns, the write operation is rejected.
- **Schema-on-Read (Apache Hive):** The raw file is stored in HDFS without checking schema rules. The schema is applied only when the query reads the data. This allows rapid ingestion of large unstructured/semi-structured files.

---

### Q17. What is an External Table in Hive?
**Answer:**
An **External Table** points to a specific directory in HDFS. Hive manages only the metadata (schema definition), but does **NOT** own the underlying files.
- If you drop an External Table using `DROP TABLE netflix_raw;`, only the metadata in Hive is deleted. **The original CSV file in HDFS remains completely intact and safe.**

---

### Q18. What is a Managed (Internal) Table in Hive?
**Answer:**
A **Managed Table** is fully owned and managed by Hive. Hive stores its data in its internal warehouse directory (`/user/hive/warehouse/dbname.db/tablename`).
- If you drop a Managed Table using `DROP TABLE netflix_cleaned;`, Hive deletes **both** the schema metadata AND the underlying data files from HDFS.

---

### Q19. Why did our project use BOTH an External Table and a Managed Table?
**Answer:**
This is the standard **ELT (Extract-Load-Transform)** data lake architecture:
1. **External Table (`netflix_raw`):** Maps directly to the immutable raw CSV file in HDFS. It prevents accidental deletion of the original data.
2. **Managed Table (`netflix_cleaned`):** Stores the transformed, cleaned, and type-cast data in an optimized columnar format (**ORC with Snappy compression**) for fast analytical queries.

---

### Q20. What is a SerDe in Hive? Why did we use `OpenCSVSerde`?
**Answer:**
SerDe stands for **Serializer / Deserializer**. It tells Hive how to interpret and parse formatted bytes from HDFS files into table rows and columns.
- Standard Hive uses `LazySimpleSerDe` with `FIELDS TERMINATED BY ','`. However, in the Netflix dataset, text fields like `director` (`"Richard Finn, Tim Maltby"`) and `country` (`"United States, India"`) contain commas inside quotation marks.
- Standard CSV parsing splits on every comma, which corrupts the column alignment.
- **`OpenCSVSerde`** properly adheres to RFC-4180 CSV specifications, respecting quotation marks (`"`) and escape characters (`\`).

---

### Q21. What happens behind the scenes when a HiveQL query is executed?
**Answer:**
1. **Parsing:** The Hive compiler checks query syntax and keywords.
2. **Semantic Analysis:** The compiler verifies table and column names against the Hive Metastore.
3. **Logical Optimization:** The optimizer creates an execution plan (e.g., filter pushdown, pruning).
4. **Physical Plan Generation:** Hive translates the query into an executable DAG of **MapReduce** or **Tez** jobs.
5. **Execution:** YARN allocates containers across the cluster, DataNodes read the HDFS blocks in parallel (Map phase), aggregate counts/sums (Reduce phase), and return the final output to the user.

---

### Q22. What is ORC format and why is it used?
**Answer:**
ORC stands for **Optimized Row Columnar**. It is a columnar file storage format optimized for Hadoop workloads.
- Instead of storing entire rows together, it stores data by columns.
- **Advantages:**
  - Dramatically improves query speed because queries reading only 2 columns skip reading the other 10 columns entirely.
  - High compression ratio (Snappy compression reduces file size by 50%–75%).
  - Contains built-in index stripes and statistics (`min`, `max`, `sum`) inside the file headers.

---

### Q23. What is Partitioning in Hive?
**Answer:**
Partitioning is a technique where Hive organizes table data into separate physical subdirectories in HDFS based on the value of one or more columns (e.g., partitioning by `release_year` or `type`).
- When a query filters by `WHERE release_year = 2019`, Hive performs **partition pruning**, reading only that specific subdirectory and skipping all other years. This drastically reduces query execution time and disk I/O.

---

### Q24. What is Bucketing in Hive?
**Answer:**
Bucketing decomposes table partitions into fixed-sized physical files called buckets based on a hash function of a column (e.g., `CLUSTERED BY (show_id) INTO 8 BUCKETS`).
- Bucketing provides equal-sized splits and dramatically accelerates map-side `JOIN` operations between large tables.

---

### Q25. How did we clean missing and NULL values in the dataset?
**Answer:**
In HiveQL, empty text entries appear as empty strings (`""`) or NULLs. In our `03_data_cleaning.sql` script:
- We used `CASE WHEN director IS NULL OR TRIM(director) = '' THEN 'Unknown Director' ELSE TRIM(director) END` to supply meaningful defaults.
- Missing cast values were replaced with `'Unknown Cast'`.
- Missing countries were replaced with `'Unknown Country'`.
- Missing ratings were replaced with `'Unrated'`.
- Blank release years and dates were filtered or safely cast.

---

### Q26. How did we handle compound duration values like `"90 min"` and `"3 Seasons"`?
**Answer:**
In raw data, duration is a string combining both quantity and unit.
- We used Hive’s `SPLIT()` function:
  - `duration_value = CAST(SPLIT(TRIM(duration), ' ')[0] AS INT)` (extracts numeric `90` or `3`).
  - `duration_unit = SPLIT(TRIM(duration), ' ')[1]` (extracts `'min'` or `'Seasons'`).
- This allowed us to calculate mathematical metrics like `AVG(duration_value)` for movies and filter multi-season TV shows (`duration_value > 1`).

---

### Q27. What is `LATERAL VIEW explode()` in HiveQL?
**Answer:**
`explode()` is a User-Defined Table-Generating Function (UDTF) in Hive that takes an array and outputs each element as a separate row.
`LATERAL VIEW` is used alongside `explode()` to join the exploded rows back with the original table row.
- In our project, the `listed_in` column had values like `"Comedies, Dramas"`.
- `LATERAL VIEW explode(split(listed_in, ','))` separated each genre into its own row, enabling an accurate top-10 genre frequency calculation.

---

### Q28. What are the key findings from the Netflix analysis?
**Answer:**
1. **Catalog Composition:** 68.42% Movies (4,265 titles) vs 31.58% TV Shows (1,969 titles).
2. **Leading Producer:** United States is #1 (2,032 titles), followed by India (777 titles) and the United Kingdom (348 titles).
3. **Maturity Rating:** TV-MA (2,027) and TV-14 (1,698) account for nearly 60% of all titles, proving Netflix's focus on mature and teen audiences.
4. **Average Movie Runtime:** 99.10 minutes (~1 hour 39 minutes).
5. **Growth Inflection:** Titles added accelerated after 2016 and peaked in 2019 (2,349 titles added).

---

### Q29. What are the main limitations of Apache Hive?
**Answer:**
1. **High Query Latency:** Hive is not designed for sub-second responses. Every query takes several seconds just to initialize and compile tasks.
2. **No Real-Time OLTP:** Hive does not excel at frequent single-record updates or deletes.
3. **Batch-Oriented:** Hive is strictly for offline batch analytics on historical data.

---

### Q30. How can this project be scaled or improved in the future?
**Answer:**
1. **Apache Spark / Spark SQL:** Running queries on Spark instead of MapReduce gives in-memory speedups of 10x to 100x.
2. **Pipeline Scheduling:** Using Apache Airflow to orchestrate automated daily ingestion and transformation.
3. **Interactive BI:** Connecting Apache Superset, Tableau, or Power BI to Hive via JDBC/ODBC for live interactive dashboards.
4. **Machine Learning:** Building a recommendation engine using Spark MLlib on user viewing logs.

---

### Q31. What is the NameNode SafeMode in Hadoop?
**Answer:**
SafeMode is a read-only state that the NameNode enters automatically during cluster startup. In SafeMode, the NameNode does not allow any file modifications (writes or deletes) while it waits for DataNodes to report their block lists (Block Reports). Once 99.9% of blocks are verified and replicated, the NameNode automatically exits SafeMode after 30 seconds.

---

### Q32. What is YARN and what are its components?
**Answer:**
YARN stands for **Yet Another Resource Negotiator**. It is Hadoop’s cluster operating system that decouples resource management from processing. Its core components are:
- **ResourceManager (Master):** Allocates compute resources (memory and CPU cores) across the cluster.
- **NodeManager (Worker):** Runs on each machine, monitoring resource usage and launching task containers.
- **ApplicationMaster:** Negotiates resources from the ResourceManager and works with NodeManagers to execute specific application jobs.

---

### Q33. What is the difference between `ORDER BY` and `SORT BY` in Hive?
**Answer:**
- **`ORDER BY`:** Guarantees total global ordering across all data by forcing all data through a **single reducer**. For large datasets, this can cause severe performance bottlenecks.
- **`SORT BY`:** Orders data locally within each individual reducer. It is much faster and distributed, but the final output is not globally sorted unless combined with `DISTRIBUTE BY`.

---

### Q34. How does Hive know where the data is stored in HDFS?
**Answer:**
When an external table or managed table is created, Hive stores the table’s HDFS URI (e.g., `hdfs://namenode:9000/user/hadoop/netflix/`) inside the **Hive Metastore database** (`TBLS` and `SDS` tables). Whenever a query is executed, the Hive Driver retrieves the storage directory from the Metastore and assigns the corresponding HDFS file split readers.

---

### Q35. What is the significance of the `jps` command in Hadoop?
**Answer:**
`jps` stands for **Java Virtual Machine Process Status Tool**. It lists all active Java processes running on the machine. In Hadoop, it is used to quickly verify that all required daemons are running:
- **NameNode**
- **DataNode**
- **SecondaryNameNode**
- **ResourceManager**
- **NodeManager**
If any of these daemons are missing from the `jps` output, it indicates a startup failure or configuration issue.
