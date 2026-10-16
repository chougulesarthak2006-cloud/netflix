# Netflix Movies and TV Shows Dataset Information

## 1. Dataset Overview
This dataset contains metadata about movies and TV shows available on Netflix up to early 2020/2021.
It is widely utilized in academia, industry benchmarks, and big data case studies to analyze streaming content trends, international expansion, and content curation patterns.

- **Primary Source:** Kaggle Netflix Movies and TV Shows Dataset (Curated by Shivam Bansal / Flixable)
- **Local File:** `dataset/netflix_titles.csv`
- **File Format:** Comma-Separated Values (CSV), UTF-8 Encoded
- **Total Records:** 6,234 titles (plus 1 header row)
- **File Size:** ~2.41 MB

## 2. Schema Definition (12 Attributes)

| Attribute | Data Type (Hive) | Description | Example Value |
|---|---|---|---|
| `show_id` | `STRING` | Unique identifier for each Netflix title | `81145628` / `s1` |
| `type` | `STRING` | Category of content (`Movie` or `TV Show`) | `Movie`, `TV Show` |
| `title` | `STRING` | Official title of the movie or television show | `Norm of the North`, `Stranger Things` |
| `director` | `STRING` | Director(s) of the movie/show (can be multiple/comma-separated) | `Richard Finn, Tim Maltby` |
| `cast` | `STRING` | Leading actors/actresses featured in the title | `Alan Marriott, Andrew Toth` |
| `country` | `STRING` | Country or countries where the title was produced | `United States, India, South Korea` |
| `date_added` | `STRING` | Date when the title was officially added to Netflix | `September 9, 2019` |
| `release_year` | `INT` | Calendar year when the film or series originally released | `2019`, `2016`, `1994` |
| `rating` | `STRING` | Official age/content rating assigned to the title | `TV-MA`, `TV-14`, `PG-13`, `R` |
| `duration` | `STRING` | Runtime for movies (in mins) or series (in Seasons) | `90 min`, `1 Season`, `3 Seasons` |
| `listed_in` | `STRING` | Genre categories assigned on the Netflix platform | `Comedies, Dramas, International Movies` |
| `description` | `STRING` | Synopsis and storyline summary | `Before planning an awesome wedding...` |

## 3. Big Data Engineering Considerations
When ingesting and parsing this dataset in Apache Hive over Hadoop HDFS, note the following real-world complexities:
1. **Embedded Commas in Text Fields:** Fields like `cast`, `director`, `country`, `listed_in`, and `description` contain internal commas enclosed in quotation marks (`"`). Standard Hive `FIELDS TERMINATED BY ','` will improperly split these columns. Hive's `org.apache.hadoop.hive.serde2.OpenCSVSerde` must be used.
2. **Missing and Empty Values:** Many older productions or TV series do not list directors or cast, appearing as empty strings (`""`) or blanks. The Hive cleaning layer transforms these into standard `NULL` or `'Unknown'` strings.
3. **Compound Durations:** Movie runtimes are expressed as `X min` while TV series are expressed as `Y Season(s)`. These must be parsed into numeric metrics and unit dimensions for mathematical aggregations.
