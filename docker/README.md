# Running Hadoop & Hive via Docker

If you have Docker Desktop installed, you can spin up a genuine multi-container cluster containing **Hadoop NameNode, DataNode, PostgreSQL Hive Metastore, and HiveServer2** with one command:

```bash
cd docker
docker compose up -d
```

### 1. Check Container Status
```bash
docker ps
```

### 2. Upload Dataset to HDFS in Container
```bash
docker exec -it netflix_hadoop_namenode hdfs dfs -mkdir -p /user/hadoop/netflix/
docker exec -it netflix_hadoop_namenode hdfs dfs -put -f /dataset/netflix_titles.csv /user/hadoop/netflix/
docker exec -it netflix_hadoop_namenode hdfs dfs -ls /user/hadoop/netflix/
```

### 3. Open Hive Shell and Run Queries
```bash
docker exec -it netflix_hive_server hive
```
Then inside the Hive prompt:
```sql
SOURCE /hive_scripts/01_create_database.sql;
SOURCE /hive_scripts/02_create_external_table.sql;
SOURCE /hive_scripts/03_data_cleaning.sql;
SOURCE /hive_scripts/04_analysis_queries.sql;
```

### 4. Hadoop NameNode Web UI
Open your browser at:
`http://localhost:9870`
