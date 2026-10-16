-- ==============================================================================
-- Script: 05_export_results.sql
-- Project: Netflix Movies and TV Shows Data Analysis using Hadoop and Hive
-- Purpose: Export Hive query results to local filesystem for reporting & visualization.
-- ==============================================================================

USE netflix_db;

-- ------------------------------------------------------------------------------
-- APPROACH 1: INSERT OVERWRITE LOCAL DIRECTORY (Native HiveQL)
-- Exports comma-delimited output files directly into local system directories.
-- (Note: In production or student VMs, replace /tmp with your project path if desired)
-- ------------------------------------------------------------------------------

-- Export 1: Content Type Distribution (Movies vs TV Shows)
INSERT OVERWRITE LOCAL DIRECTORY '/tmp/netflix_exports/q1_content_type'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
SELECT type, COUNT(*) AS count, ROUND(COUNT(*) * 100.0 / 6234, 2) AS percentage
FROM netflix_cleaned
GROUP BY type;

-- Export 2: Releases by Year (Historical Production Trend)
INSERT OVERWRITE LOCAL DIRECTORY '/tmp/netflix_exports/q2_releases_by_year'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
SELECT release_year, COUNT(*) AS count
FROM netflix_cleaned
WHERE release_year >= 2000
GROUP BY release_year
ORDER BY release_year ASC;

-- Export 3: Top 10 Producing Countries
INSERT OVERWRITE LOCAL DIRECTORY '/tmp/netflix_exports/q3_top_10_countries'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
SELECT country, COUNT(*) AS count
FROM netflix_cleaned
WHERE country != 'Unknown Country'
GROUP BY country
ORDER BY count DESC
LIMIT 10;

-- Export 4: Content Ratings Distribution
INSERT OVERWRITE LOCAL DIRECTORY '/tmp/netflix_exports/q4_top_ratings'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
SELECT rating, COUNT(*) AS count
FROM netflix_cleaned
GROUP BY rating
ORDER BY count DESC
LIMIT 10;

-- Export 5: Top 10 Genres
INSERT OVERWRITE LOCAL DIRECTORY '/tmp/netflix_exports/q5_top_genres'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
SELECT TRIM(genre) AS genre, COUNT(*) AS count
FROM netflix_cleaned
LATERAL VIEW explode(split(listed_in, ',')) g_tab AS genre
WHERE TRIM(genre) != ''
GROUP BY TRIM(genre)
ORDER BY count DESC
LIMIT 10;

-- Export 6: Titles Added by Year (Platform Catalog Growth)
INSERT OVERWRITE LOCAL DIRECTORY '/tmp/netflix_exports/q6_added_by_year'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
SELECT added_year, COUNT(*) AS count
FROM netflix_cleaned
WHERE added_year IS NOT NULL
GROUP BY added_year
ORDER BY added_year ASC;

-- Export 7: Top 10 Directors
INSERT OVERWRITE LOCAL DIRECTORY '/tmp/netflix_exports/q7_top_directors'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
SELECT director, COUNT(*) AS count
FROM netflix_cleaned
WHERE director != 'Unknown Director'
GROUP BY director
ORDER BY count DESC
LIMIT 10;

-- ------------------------------------------------------------------------------
-- APPROACH 2: CLI Export via Bash / Hive CLI (Ideal for script automation)
-- Example:
-- hive -S -e "USE netflix_db; SELECT type, COUNT(*) FROM netflix_cleaned GROUP BY type;" | tr "\t" "," > results/data/q1_content_type_distribution.csv
-- ------------------------------------------------------------------------------
