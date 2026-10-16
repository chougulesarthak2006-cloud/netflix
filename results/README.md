# Netflix Big Data Analysis: Results & Findings

This document summarizes the analytical findings obtained from running HiveQL queries on the 6,234 records of the Netflix Movies and TV Shows dataset stored in HDFS.

---

## 1. Executive Summary of Key Metrics

| Metric | Measured Value | Percentage / Context |
|---|---|---|
| **Total Catalog Titles** | **6,234** | 100.0% |
| **Total Feature Movies** | **4,265** | 68.42% of catalog |
| **Total TV Shows / Series** | **1,969** | 31.58% of catalog |
| **Dominant Production Country** | **United States** (2,032 titles) | ~32.6% of single-country catalog |
| **Secondary Production Country** | **India** (777 titles) | Highest Asian content market |
| **Most Frequent Maturity Rating** | **TV-MA** (2,027 titles) | Mature Audience target |
| **Peak Release Year** | **2018** (1,063 titles) | Global entertainment output high |
| **Peak Catalog Ingestion Year** | **2019** (2,349 titles added) | Aggressive platform licensing surge |
| **Average Movie Runtime** | **99.10 minutes** | ~1 Hour 39 Minutes |
| **Longest Running TV Shows** | *Grey's Anatomy*, *NCIS* | 15 Seasons |

---

## 2. In-Depth Query Findings

### Query 1 & 4: Content Type Distribution (Movies vs TV Shows)
- **File:** `results/data/q1_content_type_distribution.csv`
- **Result:**
  - **Movies:** 4,265 titles (68.42%)
  - **TV Shows:** 1,969 titles (31.58%)
- **Insight:** Over two-thirds of Netflix’s catalog consists of standalone films. However, TV shows have seen exponential growth in viewer engagement and subscriber retention hours.

---

### Query 5 & 17: Production Trends by Release Year
- **File:** `results/data/q2_releases_by_year.csv`
- **Top 5 Production Years:**
  1. **2018:** 1,063 titles
  2. **2017:** 959 titles
  3. **2019:** 843 titles
  4. **2016:** 830 titles
  5. **2015:** 517 titles
- **Insight:** Over 70% of the entire Netflix library was released between 2015 and 2020, demonstrating Netflix's pivot toward contemporary media and recent digital productions.

---

### Query 6 & 14: Top Content Producing Countries
- **File:** `results/data/q3_top_10_countries.csv`
- **Ranking:**
  1. **United States:** 2,032 titles
  2. **India:** 777 titles
  3. **United Kingdom:** 348 titles
  4. **Japan:** 176 titles
  5. **Canada:** 141 titles
  6. **South Korea:** 136 titles
  7. **Spain:** 117 titles
  8. **France:** 90 titles
  9. **Mexico:** 83 titles
  10. **Turkey:** 79 titles
- **Insight:** The United States leads as the primary content hub, followed by India. Asian markets (India, Japan, South Korea) together account for over 1,000 titles, highlighting heavy regional investments in Bollywood, Anime, and K-Dramas.

---

### Query 7 & 18: Content Ratings Breakdown
- **File:** `results/data/q4_top_ratings.csv`
- **Ranking:**
  - **TV-MA (Mature Adults):** 2,027 (32.5%)
  - **TV-14 (Parents Strongly Cautioned):** 1,698 (27.2%)
  - **TV-PG (Parental Guidance):** 701 (11.2%)
  - **R (Restricted):** 508 (8.1%)
  - **PG-13 (Teens):** 286 (4.6%)
  - **NR / Unrated:** 218
- **Insight:** Together, TV-MA and TV-14 represent nearly 60% of all content, proving that Netflix's core target audience is young adults and adults rather than children.

---

### Query 8: Top 10 Genres
- **File:** `results/data/q5_top_genres.csv`
- **Top Categories:**
  1. **International Movies:** 1,927
  2. **Dramas:** 1,623
  3. **Comedies:** 1,113
  4. **International TV Shows:** 1,001
  5. **Documentaries:** 668
  6. **TV Dramas:** 599
  7. **Action & Adventure:** 597
  8. **Independent Movies:** 552
  9. **TV Comedies:** 436
  10. **Thrillers:** 392
- **Insight:** "International" films and series rank at the absolute top, demonstrating Netflix’s globalization strategy of acquiring local content for cross-border global streaming.

---

### Query 9: Titles Added by Year (Ingestion Velocity)
- **File:** `results/data/q6_added_by_year.csv`
- **Velocity Timeline:**
  - 2008–2014: ~55 titles total (Early experimentation era)
  - 2015: 90 titles
  - 2016: 456 titles (Global rollout to 130+ countries)
  - 2017: 1,300 titles
  - 2018: 1,782 titles
  - 2019: 2,349 titles (Record acquisition peak)
- **Insight:** The explosive inflection point occurred in 2016 when Netflix expanded internationally, scaling catalog ingestion over 25x within four years.

---

### Query 12: Top Directors
- **File:** `results/data/q7_top_directors.csv`
- **Top Creators:**
  - **Raúl Campos, Jan Suter:** 18 titles (Latin American stand-up specials)
  - **Marcus Raboy:** 14 titles (Stand-up comedy specials)
  - **Jay Karas:** 13 titles
  - **Jay Chapman:** 12 titles
  - **Steven Spielberg:** 9 titles (Iconic Hollywood catalog acquisitions)
  - **Martin Scorsese:** 9 titles (Including Netflix Originals like *The Irishman*)

---

### Query 13: Movie Runtime Metrics
- **File:** `results/data/q8_movie_duration_stats.csv`
- **Average Runtime:** **99.10 minutes** (~1h 39m)
- **Shortest Movie:** 3 minutes (Short animated features)
- **Longest Movie:** 312 minutes (*Black Mirror: Bandersnatch* interactive cuts / mini-documentaries)
- **Standard Deviation:** Most feature films cluster tightly between 85 and 115 minutes.
