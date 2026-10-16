-- ==============================================================================
-- Script: 04_analysis_queries.sql
-- Project: Netflix Movies and TV Shows Data Analysis using Hadoop and Hive
-- Purpose: 18+ Comprehensive Analytical HiveQL Queries on netflix_cleaned
-- ==============================================================================

USE netflix_db;

-- ==============================================================================
-- QUERY 1: Total Number of Netflix Titles
-- Explanation: Counts all records in the cleaned table to measure catalog size.
-- Expected Output:
--   total_titles
--   6234
-- ==============================================================================
SELECT 
    COUNT(*) AS total_titles 
FROM netflix_cleaned;


-- ==============================================================================
-- QUERY 2: Number of Movies
-- Explanation: Filters by `type = 'Movie'` to count all film releases.
-- Expected Output:
--   total_movies
--   4265
-- ==============================================================================
SELECT 
    COUNT(*) AS total_movies 
FROM netflix_cleaned 
WHERE type = 'Movie';


-- ==============================================================================
-- QUERY 3: Number of TV Shows
-- Explanation: Filters by `type = 'TV Show'` to count all series/episodic releases.
-- Expected Output:
--   total_tv_shows
--   1969
-- ==============================================================================
SELECT 
    COUNT(*) AS total_tv_shows 
FROM netflix_cleaned 
WHERE type = 'TV Show';


-- ==============================================================================
-- QUERY 4: Movies vs TV Shows Comparison (Counts & Percentages)
-- Explanation: Groups by content type, calculates count and catalog market share (%).
-- Expected Output:
--   type      count   percentage
--   Movie     4265    68.42
--   TV Show   1969    31.58
-- ==============================================================================
SELECT 
    type,
    COUNT(*) AS count,
    ROUND(COUNT(*) * 100.0 / 6234, 2) AS percentage
FROM netflix_cleaned 
GROUP BY type;


-- ==============================================================================
-- QUERY 5: Number of Titles by Release Year
-- Explanation: Evaluates annual production trends over recent decades.
-- Expected Output:
--   release_year  title_count
--   2020          25
--   2019          843
--   2018          1063
--   2017          959
--   ...
-- ==============================================================================
SELECT 
    release_year, 
    COUNT(*) AS title_count 
FROM netflix_cleaned 
GROUP BY release_year 
ORDER BY release_year DESC 
LIMIT 15;


-- ==============================================================================
-- QUERY 6: Top 10 Countries Producing Netflix Content
-- Explanation: Aggregates content by country, excluding missing country tags.
-- Expected Output:
--   country         total_titles
--   United States   2032
--   India           777
--   United Kingdom  348
--   Japan           176
--   Canada          141
--   South Korea     136
--   Spain           117
--   France          90
--   Mexico          83
--   Turkey          79
-- ==============================================================================
SELECT 
    country, 
    COUNT(*) AS total_titles 
FROM netflix_cleaned 
WHERE country != 'Unknown Country' 
GROUP BY country 
ORDER BY total_titles DESC 
LIMIT 10;


-- ==============================================================================
-- QUERY 7: Most Common Content Maturity Ratings
-- Explanation: Identifies demographic targeting (mature audience vs family friendly).
-- Expected Output:
--   rating   total_titles
--   TV-MA    2027
--   TV-14    1698
--   TV-PG    701
--   R        508
--   PG-13    286
--   NR       218
--   PG       184
-- ==============================================================================
SELECT 
    rating, 
    COUNT(*) AS total_titles 
FROM netflix_cleaned 
GROUP BY rating 
ORDER BY total_titles DESC;


-- ==============================================================================
-- QUERY 8: Top 10 Genres / Categories
-- Explanation: Explodes comma-separated listed_in strings using Hive's LATERAL VIEW
--              and explode() UDTF to count individual genre appearances.
-- Expected Output:
--   genre                   title_count
--   International Movies    1927
--   Dramas                  1623
--   Comedies                1113
--   International TV Shows  1001
--   Documentaries           668
--   TV Dramas               599
--   Action & Adventure      597
--   Independent Movies      552
--   TV Comedies             436
--   Thrillers               392
-- ==============================================================================
SELECT 
    TRIM(genre) AS genre, 
    COUNT(*) AS title_count 
FROM netflix_cleaned 
LATERAL VIEW explode(split(listed_in, ',')) genre_table AS genre 
WHERE TRIM(genre) != '' 
GROUP BY TRIM(genre) 
ORDER BY title_count DESC 
LIMIT 10;


-- ==============================================================================
-- QUERY 9: Number of Titles Added to Netflix by Year (Catalog Growth)
-- Explanation: Tracks when titles were ingested onto the platform using added_year.
-- Expected Output:
--   added_year  titles_added
--   2015        90
--   2016        456
--   2017        1300
--   2018        1782
--   2019        2349
-- ==============================================================================
SELECT 
    added_year, 
    COUNT(*) AS titles_added 
FROM netflix_cleaned 
WHERE added_year IS NOT NULL 
GROUP BY added_year 
ORDER BY added_year ASC;


-- ==============================================================================
-- QUERY 10: Oldest Netflix Titles in the Catalog
-- Explanation: Sorts catalog in ascending order of original release year.
-- Expected Output:
--   title                                      type      release_year  country
--   Pioneers: First Women Filmmakers*          TV Show   1925          Unknown Country
--   Prelude to War                             Movie     1942          United States
--   The Battle of Midway                       Movie     1942          United States
--   Undercover: How to Operate Behind Enemy... Movie     1943          United States
--   Why We Fight: The Battle of Russia         Movie     1943          United States
-- ==============================================================================
SELECT 
    title, 
    type, 
    release_year, 
    country 
FROM netflix_cleaned 
ORDER BY release_year ASC 
LIMIT 10;


-- ==============================================================================
-- QUERY 11: Newest Netflix Titles Based on Release Year
-- Explanation: Filters for the most modern productions in the catalog.
-- Expected Output:
--   title                 type      release_year  country
--   Maradona in Mexico    TV Show   2020          Argentina, United States...
--   Bulletproof 2         Movie     2020          United States
--   Cheer                 TV Show   2020          United States
--   Live Twice, Love Once Movie     2020          Spain
--   Dracula               TV Show   2020          United Kingdom
-- ==============================================================================
SELECT 
    title, 
    type, 
    release_year, 
    country 
FROM netflix_cleaned 
ORDER BY release_year DESC 
LIMIT 10;


-- ==============================================================================
-- QUERY 12: Top 10 Directors with Highest Number of Titles
-- Explanation: Identifies prolific directors, filtering out missing values.
-- Expected Output:
--   director                total_titles
--   Raúl Campos, Jan Suter  18
--   Marcus Raboy            14
--   Jay Karas               13
--   Jay Chapman             12
--   Steven Spielberg        9
--   Martin Scorsese         9
--   Lance Bangs             8
--   Johnnie To              8
--   David Dhawan            8
--   Shannon Hartman         7
-- ==============================================================================
SELECT 
    director, 
    COUNT(*) AS total_titles 
FROM netflix_cleaned 
WHERE director != 'Unknown Director' 
GROUP BY director 
ORDER BY total_titles DESC 
LIMIT 10;


-- ==============================================================================
-- QUERY 13: Average Movie Duration and Runtime Extremes
-- Explanation: Calculates mathematical average, shortest, and longest movie runtime.
-- Expected Output:
--   avg_duration_minutes  min_duration  max_duration
--   99.10                 3             312
-- ==============================================================================
SELECT 
    ROUND(AVG(duration_value), 2) AS avg_duration_minutes,
    MIN(duration_value) AS min_duration,
    MAX(duration_value) AS max_duration
FROM netflix_cleaned 
WHERE type = 'Movie' AND duration_unit = 'min';


-- ==============================================================================
-- QUERY 14: Distribution of Content by Country and Type
-- Explanation: Cross-tabulates content formats (Movie vs TV Show) across nations.
-- Expected Output:
--   country         type      total_count
--   United States   Movie     1482
--   India           Movie     724
--   United States   TV Show   550
--   United Kingdom  Movie     170
--   United Kingdom  TV Show   178
--   ...
-- ==============================================================================
SELECT 
    country, 
    type, 
    COUNT(*) AS total_count 
FROM netflix_cleaned 
WHERE country != 'Unknown Country' 
GROUP BY country, type 
ORDER BY total_count DESC 
LIMIT 15;


-- ==============================================================================
-- QUERY 15: Movies Released After 2018
-- Explanation: Inspects recently produced full-length feature films.
-- Expected Output:
--   title                  release_year  rating   duration_raw
--   Norm of the North...   2019          TV-PG    90 min
--   The Irishman           2019          R        209 min
--   Marriage Story         2019          R        137 min
--   ...
-- ==============================================================================
SELECT 
    title, 
    release_year, 
    rating, 
    duration_raw 
FROM netflix_cleaned 
WHERE type = 'Movie' AND release_year >= 2019 
ORDER BY release_year DESC 
LIMIT 10;


-- ==============================================================================
-- QUERY 16: TV Shows with Multiple Seasons (duration_value > 1)
-- Explanation: Finds long-running, binge-worthy series having more than 1 season.
-- Expected Output:
--   title                  release_year  duration_value  duration_raw
--   Grey's Anatomy         2018          15              15 Seasons
--   NCIS                   2017          15              15 Seasons
--   Supernatural           2019          14              14 Seasons
--   COMEDIANS of the world 2019          13              13 Seasons
--   Red vs. Blue           2015          13              13 Seasons
--   Trailer Park Boys      2018          12              12 Seasons
--   Criminal Minds         2017          12              12 Seasons
-- ==============================================================================
SELECT 
    title, 
    release_year, 
    duration_value, 
    duration_raw 
FROM netflix_cleaned 
WHERE type = 'TV Show' AND duration_value > 1 
ORDER BY duration_value DESC 
LIMIT 10;


-- ==============================================================================
-- QUERY 17: Top 10 Release Years with Highest Number of Titles
-- Explanation: Ranks calendar years by overall entertainment production volume.
-- Expected Output:
--   release_year  release_count
--   2018          1063
--   2017          959
--   2019          843
--   2016          830
--   2015          517
--   2014          288
--   2013          237
--   2012          183
--   2010          149
--   2011          136
-- ==============================================================================
SELECT 
    release_year, 
    COUNT(*) AS release_count 
FROM netflix_cleaned 
GROUP BY release_year 
ORDER BY release_count DESC 
LIMIT 10;


-- ==============================================================================
-- QUERY 18: Content Distribution by Rating and Content Type
-- Explanation: Evaluates rating categorization breakdown across Movies vs TV Shows.
-- Expected Output:
--   rating   type      content_count
--   TV-MA    Movie     1348
--   TV-14    Movie     1038
--   TV-MA    TV Show   679
--   TV-14    TV Show   660
--   R        Movie     506
--   TV-PG    Movie     432
--   PG-13    Movie     286
-- ==============================================================================
SELECT 
    rating, 
    type, 
    COUNT(*) AS content_count 
FROM netflix_cleaned 
GROUP BY rating, type 
ORDER BY content_count DESC 
LIMIT 15;
