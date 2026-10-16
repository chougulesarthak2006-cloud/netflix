-- ==============================================================================
-- Script: 02_create_external_table.sql
-- Project: Netflix Movies and TV Shows Data Analysis using Hadoop and Hive
-- Purpose: Create an External Table in Hive mapped to the raw HDFS dataset.
-- ==============================================================================

USE netflix_db;

-- ------------------------------------------------------------------------------
-- ARCHITECTURAL NOTE FOR VIVA:
-- Why use OpenCSVSerde instead of standard ROW FORMAT DELIMITED?
-- The Netflix CSV contains fields with embedded commas enclosed in quotes,
-- such as: "United States, India, South Korea", "Richard Finn, Tim Maltby".
-- Standard Hive CSV parsing splits strictly on every comma, which corrupts
-- column boundaries. OpenCSVSerde correctly respects quotation marks ("").
-- ------------------------------------------------------------------------------

DROP TABLE IF EXISTS netflix_raw;

CREATE EXTERNAL TABLE IF NOT EXISTS netflix_raw (
    show_id         STRING COMMENT 'Unique ID for each title',
    type            STRING COMMENT 'Movie or TV Show',
    title           STRING COMMENT 'Title of the content',
    director        STRING COMMENT 'Director name(s)',
    cast            STRING COMMENT 'Actors featured in the title',
    country         STRING COMMENT 'Production country',
    date_added      STRING COMMENT 'Date added to Netflix catalog',
    release_year    STRING COMMENT 'Original calendar release year',
    rating          STRING COMMENT 'Content maturity rating',
    duration        STRING COMMENT 'Duration in minutes or seasons',
    listed_in       STRING COMMENT 'Genre categories',
    description     STRING COMMENT 'Plot synopsis'
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
   "separatorChar" = ",",
   "quoteChar"     = "\"",
   "escapeChar"    = "\\"
)
STORED AS TEXTFILE
LOCATION '/user/hadoop/netflix/'
TBLPROPERTIES (
   "skip.header.line.count" = "1",
   "comment" = "Raw external staging table mapping to HDFS Netflix CSV dataset"
);

-- ==============================================================================
-- Table Verification Commands
-- ==============================================================================

-- 1. Show all tables in netflix_db
SHOW TABLES;

-- 2. Inspect table schema and metadata (shows EXTERNAL table type and HDFS location)
DESCRIBE FORMATTED netflix_raw;

-- 3. Sample verification: preview first 10 rows
SELECT show_id, type, title, release_year, rating, duration 
FROM netflix_raw 
LIMIT 10;

-- 4. Count total raw records in the table
SELECT COUNT(*) AS total_raw_records FROM netflix_raw;
