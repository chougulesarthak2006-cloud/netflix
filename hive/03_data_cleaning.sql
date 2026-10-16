-- ==============================================================================
-- Script: 03_data_cleaning.sql
-- Project: Netflix Movies and TV Shows Data Analysis using Hadoop and Hive
-- Purpose: Clean raw HDFS data, standardize missing/empty values, split duration,
--          and persist into an optimized Hive Managed Table (`netflix_cleaned`).
-- ==============================================================================

USE netflix_db;

-- ------------------------------------------------------------------------------
-- CLEANING RATIONALE FOR ACADEMIC DOCUMENTATION & VIVA:
-- 1. Empty Strings vs NULL: Raw CSV entries without values are parsed by SerDe
--    as empty strings (""). We use CASE / COALESCE to standardize them.
-- 2. Missing Attributes:
--    - Missing director  -> 'Unknown Director'
--    - Missing cast      -> 'Unknown Cast'
--    - Missing country   -> 'Unknown Country'
--    - Missing rating    -> 'Unrated'
-- 3. Data Type Casting:
--    - release_year      -> INT (Enables range filtering and numerical sorting)
-- 4. Derived Temporal Feature (added_year):
--    - date_added        -> e.g. "September 9, 2019" -> Extract 2019 as INT
-- 5. Compound Duration Normalization:
--    - Movies: "90 min"    -> duration_value = 90, duration_unit = 'min'
--    - TV:     "3 Seasons" -> duration_value = 3,  duration_unit = 'Seasons'
--    This enables mathematical operations like AVG(duration_value) for movies
--    and multi-season filtering for TV series.
-- ------------------------------------------------------------------------------

DROP TABLE IF EXISTS netflix_cleaned;

CREATE TABLE IF NOT EXISTS netflix_cleaned (
    show_id         STRING,
    type            STRING,
    title           STRING,
    director        STRING,
    cast            STRING,
    country         STRING,
    date_added      STRING,
    added_year      INT,
    release_year    INT,
    rating          STRING,
    duration_raw    STRING,
    duration_value  INT,
    duration_unit   STRING,
    listed_in       STRING,
    description     STRING
)
STORED AS ORC
TBLPROPERTIES (
    "orc.compress" = "SNAPPY",
    "comment" = "Cleaned and optimized managed table for analytical HiveQL queries"
);

-- Ingest, clean, transform, and load into netflix_cleaned
INSERT OVERWRITE TABLE netflix_cleaned
SELECT
    TRIM(show_id) AS show_id,
    
    -- Normalize content type
    TRIM(type) AS type,
    
    -- Clean title
    TRIM(title) AS title,
    
    -- Clean director: replace blank/empty string with 'Unknown Director'
    CASE 
        WHEN director IS NULL OR TRIM(director) = '' THEN 'Unknown Director'
        ELSE TRIM(director)
    END AS director,
    
    -- Clean cast: replace blank/empty string with 'Unknown Cast'
    CASE 
        WHEN cast IS NULL OR TRIM(cast) = '' THEN 'Unknown Cast'
        ELSE TRIM(cast)
    END AS cast,
    
    -- Clean country: replace blank/empty string with 'Unknown Country'
    CASE 
        WHEN country IS NULL OR TRIM(country) = '' THEN 'Unknown Country'
        ELSE TRIM(country)
    END AS country,
    
    -- Retain raw date_added
    TRIM(date_added) AS date_added,
    
    -- Extract added_year from date_added string (e.g. "September 9, 2019" -> 2019)
    CASE 
        WHEN date_added IS NOT NULL AND INSTR(date_added, ',') > 0 
        THEN CAST(TRIM(SPLIT(TRIM(date_added), ',')[1]) AS INT)
        ELSE NULL
    END AS added_year,
    
    -- Cast release year safely to integer
    CAST(TRIM(release_year) AS INT) AS release_year,
    
    -- Clean rating: replace blank/empty with 'Unrated'
    CASE 
        WHEN rating IS NULL OR TRIM(rating) = '' THEN 'Unrated'
        ELSE TRIM(rating)
    END AS rating,
    
    -- Retain original duration string
    TRIM(duration) AS duration_raw,
    
    -- Extract numeric duration value (e.g. "90 min" -> 90, "3 Seasons" -> 3)
    CAST(SPLIT(TRIM(duration), ' ')[0] AS INT) AS duration_value,
    
    -- Extract duration unit ('min', 'Season', 'Seasons')
    SPLIT(TRIM(duration), ' ')[1] AS duration_unit,
    
    -- Clean genres and plot synopsis
    TRIM(listed_in) AS listed_in,
    TRIM(description) AS description

FROM netflix_raw
WHERE show_id IS NOT NULL AND TRIM(show_id) != '';

-- ==============================================================================
-- Verification of Cleaned Table
-- ==============================================================================

-- 1. Inspect schema and ORC storage
DESCRIBE FORMATTED netflix_cleaned;

-- 2. Verify total cleaned count
SELECT COUNT(*) AS total_cleaned_records FROM netflix_cleaned;

-- 3. Check parsed duration and extracted year on sample records
SELECT show_id, type, title, release_year, added_year, duration_value, duration_unit 
FROM netflix_cleaned 
LIMIT 10;

-- 4. Verify no remaining empty strings in categorical columns
SELECT 
    COUNT(CASE WHEN director = 'Unknown Director' THEN 1 END) AS missing_directors_handled,
    COUNT(CASE WHEN country = 'Unknown Country' THEN 1 END) AS missing_countries_handled,
    COUNT(CASE WHEN rating = 'Unrated' THEN 1 END) AS unrated_titles_handled
FROM netflix_cleaned;
