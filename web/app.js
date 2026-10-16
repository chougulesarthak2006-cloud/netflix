/**
 * app.js
 * ------
 * Frontend interactive logic for Netflix Big Data Analytics Platform.
 */

const DEFAULT_QUERIES = [
    {
        "id": 1,
        "title": "Total Number of Titles",
        "category": "Catalog Overview",
        "sql": "SELECT COUNT(*) AS total_titles FROM netflix_cleaned;",
        "hiveql": "SELECT COUNT(*) AS total_titles FROM netflix_cleaned;",
        "explanation": "Calculates total media records cataloged in Netflix data warehouse.",
        "expected": "6,234 titles"
    },
    {
        "id": 2,
        "title": "Number of Movies",
        "category": "Catalog Overview",
        "sql": "SELECT COUNT(*) AS total_movies FROM netflix_cleaned WHERE type = 'Movie';",
        "hiveql": "SELECT COUNT(*) AS total_movies FROM netflix_cleaned WHERE type = 'Movie';",
        "explanation": "Filters catalog by type = 'Movie' to measure feature film library volume.",
        "expected": "4,265 movies"
    },
    {
        "id": 3,
        "title": "Number of TV Shows",
        "category": "Catalog Overview",
        "sql": "SELECT COUNT(*) AS total_tv_shows FROM netflix_cleaned WHERE type = 'TV Show';",
        "hiveql": "SELECT COUNT(*) AS total_tv_shows FROM netflix_cleaned WHERE type = 'TV Show';",
        "explanation": "Filters catalog by type = 'TV Show' to count serial content.",
        "expected": "1,969 TV shows"
    },
    {
        "id": 4,
        "title": "Movies vs TV Shows Comparison",
        "category": "Catalog Overview",
        "sql": "SELECT type, COUNT(*) AS count, ROUND(COUNT(*) * 100.0 / 6234, 2) AS percentage FROM netflix_cleaned GROUP BY type;",
        "hiveql": "SELECT type, COUNT(*) AS count, ROUND(COUNT(*) * 100.0 / 6234, 2) AS percentage FROM netflix_cleaned GROUP BY type;",
        "explanation": "Computes proportion and market share of Movies vs TV Shows in catalog.",
        "expected": "Movies: 68.42%, TV Shows: 31.58%"
    },
    {
        "id": 5,
        "title": "Titles by Release Year (Recent 15 Years)",
        "category": "Temporal Trends",
        "sql": "SELECT release_year, COUNT(*) AS title_count FROM netflix_cleaned GROUP BY release_year ORDER BY release_year DESC LIMIT 15;",
        "hiveql": "SELECT release_year, COUNT(*) AS title_count FROM netflix_cleaned GROUP BY release_year ORDER BY release_year DESC LIMIT 15;",
        "explanation": "Aggregates production year velocity over recent calendar years.",
        "expected": "High volume concentrated between 2016-2019"
    },
    {
        "id": 6,
        "title": "Top 10 Content Producing Countries",
        "category": "Geographical Analysis",
        "sql": "SELECT country, COUNT(*) AS total_titles FROM netflix_cleaned WHERE country != 'Unknown Country' GROUP BY country ORDER BY total_titles DESC LIMIT 10;",
        "hiveql": "SELECT country, COUNT(*) AS total_titles FROM netflix_cleaned WHERE country != 'Unknown Country' GROUP BY country ORDER BY total_titles DESC LIMIT 10;",
        "explanation": "Identifies top national origins for streaming content, excluding missing entries.",
        "expected": "United States (2,032), India (777), United Kingdom (348)"
    },
    {
        "id": 7,
        "title": "Most Common Maturity Ratings",
        "category": "Audience & Ratings",
        "sql": "SELECT rating, COUNT(*) AS total_titles FROM netflix_cleaned GROUP BY rating ORDER BY total_titles DESC LIMIT 10;",
        "hiveql": "SELECT rating, COUNT(*) AS total_titles FROM netflix_cleaned GROUP BY rating ORDER BY total_titles DESC LIMIT 10;",
        "explanation": "Evaluates content suitability across TV-MA, TV-14, TV-PG, R, and PG tiers.",
        "expected": "TV-MA leads with 2,027 titles, followed by TV-14 with 1,698"
    },
    {
        "id": 8,
        "title": "Top 10 Genres / Categories",
        "category": "Genre Analytics",
        "sql": "SPECIAL_GENRE",
        "hiveql": "SELECT TRIM(genre) AS genre, COUNT(*) AS total_titles FROM netflix_cleaned LATERAL VIEW explode(split(listed_in, ',')) t AS genre GROUP BY TRIM(genre) ORDER BY total_titles DESC LIMIT 10;",
        "explanation": "Explodes comma-separated genre arrays into distinct rows using Hive UDTF explode().",
        "expected": "International Movies, Dramas, Comedies, International TV Shows"
    },
    {
        "id": 9,
        "title": "Titles Added to Netflix by Year",
        "category": "Temporal Trends",
        "sql": "SELECT added_year, COUNT(*) AS titles_added FROM netflix_cleaned WHERE added_year IS NOT NULL GROUP BY added_year ORDER BY added_year ASC;",
        "hiveql": "SELECT added_year, COUNT(*) AS titles_added FROM netflix_cleaned WHERE added_year IS NOT NULL GROUP BY added_year ORDER BY added_year ASC;",
        "explanation": "Examines platform acquisition velocity from 2008 through 2020.",
        "expected": "Exponential platform expansion starting after 2015"
    },
    {
        "id": 10,
        "title": "Oldest Titles in Catalog",
        "category": "Historical Analysis",
        "sql": "SELECT title, type, release_year, country FROM netflix_cleaned ORDER BY release_year ASC LIMIT 5;",
        "hiveql": "SELECT title, type, release_year, country FROM netflix_cleaned ORDER BY release_year ASC LIMIT 5;",
        "explanation": "Identifies vintage historical cinema preservation in the database.",
        "expected": "WWII-era historical documentaries and classics (1942-1945)"
    },
    {
        "id": 11,
        "title": "Newest Titles Based on Release Year",
        "category": "Catalog Overview",
        "sql": "SELECT title, type, release_year, country FROM netflix_cleaned ORDER BY release_year DESC LIMIT 5;",
        "hiveql": "SELECT title, type, release_year, country FROM netflix_cleaned ORDER BY release_year DESC LIMIT 5;",
        "explanation": "Retrieves the most recent additions released in 2020.",
        "expected": "Recent 2020 releases"
    },
    {
        "id": 12,
        "title": "Directors with Highest Number of Titles",
        "category": "Talent & Cast",
        "sql": "SELECT director, COUNT(*) AS total_titles FROM netflix_cleaned WHERE director != 'Unknown Director' GROUP BY director ORDER BY total_titles DESC LIMIT 10;",
        "hiveql": "SELECT director, COUNT(*) AS total_titles FROM netflix_cleaned WHERE director != 'Unknown Director' GROUP BY director ORDER BY total_titles DESC LIMIT 10;",
        "explanation": "Finds most prolific film and TV directors on the platform.",
        "expected": "Raúl Campos, Jan Suter, Marcus Raboy, Jay Karas"
    },
    {
        "id": 13,
        "title": "Average Duration of Movies (in minutes)",
        "category": "Runtime & Duration",
        "sql": "SELECT ROUND(AVG(duration_value), 2) AS avg_movie_duration_min FROM netflix_cleaned WHERE type = 'Movie' AND duration_unit = 'min';",
        "hiveql": "SELECT ROUND(AVG(duration_value), 2) AS avg_movie_duration_min FROM netflix_cleaned WHERE type = 'Movie' AND duration_unit = 'min';",
        "explanation": "Calculates arithmetic mean runtime for feature films using parsed integer durations.",
        "expected": "Approximately 99.1 minutes (~1 hour 39 min)"
    },
    {
        "id": 14,
        "title": "Movies Grouped by Duration Range",
        "category": "Runtime & Duration",
        "sql": "CASE WHEN binning of duration_value into Short, Standard, Feature, and Epic categories.",
        "hiveql": "CASE WHEN binning of duration_value into Short, Standard, Feature, and Epic categories.",
        "explanation": "Segments feature films into runtime bins for programming scheduling analysis.",
        "expected": "Feature (91-120 min) is the dominant category"
    },
    {
        "id": 15,
        "title": "TV Shows with Multiple Seasons",
        "category": "Runtime & Duration",
        "sql": "SELECT title, duration_value AS seasons, country FROM netflix_cleaned WHERE type = 'TV Show' AND duration_value > 3 ORDER BY seasons DESC LIMIT 10;",
        "hiveql": "SELECT title, duration_value AS seasons, country FROM netflix_cleaned WHERE type = 'TV Show' AND duration_value > 3 ORDER BY seasons DESC LIMIT 10;",
        "explanation": "Queries long-running franchise series with more than 3 seasons.",
        "expected": "Grey's Anatomy (16 seasons), Supernatural (14 seasons), NCIS (15 seasons)"
    },
    {
        "id": 16,
        "title": "Content Added in the Year 2019",
        "category": "Temporal Trends",
        "sql": "SELECT type, COUNT(*) AS count_2019 FROM netflix_cleaned WHERE added_year = 2019 GROUP BY type;",
        "hiveql": "SELECT type, COUNT(*) AS count_2019 FROM netflix_cleaned WHERE added_year = 2019 GROUP BY type;",
        "explanation": "Measures catalog additions during peak growth year 2019 by content type.",
        "expected": "Movies: 1,385, TV Shows: 664"
    },
    {
        "id": 17,
        "title": "Top Release Years for Movies",
        "category": "Temporal Trends",
        "sql": "SELECT release_year, COUNT(*) AS movie_count FROM netflix_cleaned WHERE type = 'Movie' GROUP BY release_year ORDER BY movie_count DESC LIMIT 5;",
        "hiveql": "SELECT release_year, COUNT(*) AS movie_count FROM netflix_cleaned WHERE type = 'Movie' GROUP BY release_year ORDER BY movie_count DESC LIMIT 5;",
        "explanation": "Pinpoints the peak production calendar years represented in the movie collection.",
        "expected": "2018 (1,063 titles), 2017 (959 titles), 2019 (843 titles)"
    },
    {
        "id": 18,
        "title": "Content Distribution by Rating and Format",
        "category": "Audience & Ratings",
        "sql": "SELECT rating, type, COUNT(*) AS count FROM netflix_cleaned GROUP BY rating, type ORDER BY count DESC LIMIT 10;",
        "hiveql": "SELECT rating, type, COUNT(*) AS count FROM netflix_cleaned GROUP BY rating, type ORDER BY count DESC LIMIT 10;",
        "explanation": "Bivariate cross-tabulation of maturity ratings across Movies and TV Shows.",
        "expected": "TV-MA Movies (1,348), TV-14 Movies (1,038), TV-MA TV Shows (679)"
    }
];

const DEFAULT_VIVA = [
    {"q": "What is Big Data?", "a": "Big Data refers to extremely large, complex datasets characterized by the 5 V's: Volume, Velocity, Variety, Veracity, and Value, which cannot be processed efficiently using traditional relational databases.", "category": "Fundamentals"},
    {"q": "What is Apache Hadoop?", "a": "Apache Hadoop is an open-source framework designed for distributed storage (HDFS) and distributed parallel processing (MapReduce) across clusters of commodity hardware.", "category": "Fundamentals"},
    {"q": "What is HDFS and how does it work?", "a": "HDFS (Hadoop Distributed File System) stores large files by breaking them into 128 MB blocks and distributing them across multiple DataNodes with a replication factor (typically 3) for fault tolerance.", "category": "HDFS"},
    {"q": "What is the role of the NameNode and DataNode?", "a": "The NameNode is the Master node managing the file system namespace, directory hierarchy, and block-to-DataNode mappings. DataNodes are Worker nodes storing actual data blocks on local disks.", "category": "HDFS"},
    {"q": "What is Replication Factor in HDFS?", "a": "The number of copies stored for each data block. In production it defaults to 3 for fault tolerance; in single-node/pseudo-distributed setups it is set to 1.", "category": "HDFS"},
    {"q": "What is Apache Hive?", "a": "Apache Hive is a distributed data warehouse software built on Hadoop. It allows users to write SQL-like queries (HiveQL) that are automatically translated into distributed MapReduce or Tez jobs.", "category": "Hive"},
    {"q": "Hadoop vs Hive: What is the core difference?", "a": "Hadoop is the underlying distributed platform (HDFS + YARN + MapReduce). Hive is a data warehousing layer on top of Hadoop that provides SQL abstraction so developers do not need to write complex Java MapReduce code.", "category": "Hive"},
    {"q": "Why use Hive instead of MySQL for this dataset?", "a": "MySQL is an OLTP engine for transactional row operations on a single server. Hive is an OLAP data warehouse for scalable analytical aggregation across distributed multi-terabyte data blocks in HDFS.", "category": "Architecture"},
    {"q": "What is an External Table vs a Managed Table in Hive?", "a": "Managed Tables (Internal): Hive manages both metadata and data; dropping the table deletes both. External Tables: Hive manages only metadata; dropping the table preserves the raw HDFS data files.", "category": "Hive"},
    {"q": "Why was OpenCSVSerde required for this Netflix dataset?", "a": "The Netflix CSV contains quoted fields with embedded commas (e.g. composite directors or country lists like 'United States, India'). OpenCSVSerde correctly respects quotes, preventing column corruption.", "category": "Hive"},
    {"q": "What is Schema-on-Read in Hive?", "a": "Hive does not validate or transform data when uploading into HDFS. Instead, it applies the schema structure only when the data is read during query execution.", "category": "Hive"},
    {"q": "What is MapReduce and its phases?", "a": "MapReduce is a distributed programming paradigm. The Map phase processes input records into key-value pairs; Shuffle & Sort groups values by key; the Reduce phase aggregates the values per key.", "category": "MapReduce"},
    {"q": "What is Local Demo Mode vs Hadoop Cluster Mode in this project?", "a": "Local Demo Mode executes Python mappers, reducers, and in-memory SQL for instant viva demonstration without pre-installed Hadoop. Hadoop Cluster Mode connects to HDFS and Hive on a live cluster.", "category": "Project Specific"},
    {"q": "How did we clean duration values like '90 min' and '3 Seasons'?", "a": "We split the string into a numeric duration_value (e.g. 90 or 3) and a text duration_unit ('min' or 'Seasons') in table netflix_cleaned, enabling numerical AVG() for movies and multi-season filters for TV.", "category": "Data Cleaning"},
    {"q": "What is the ORC file format and why use it in Hive?", "a": "ORC (Optimized Row Columnar) is a columnar storage format with Snappy compression that drastically speeds up queries by reading only requested columns and skipping irrelevant stripes.", "category": "Performance"}
];

let allQueries = DEFAULT_QUERIES;
let allVivaQuestions = DEFAULT_VIVA;
let currentQueryId = 1;
let currentActiveMode = "local";

document.addEventListener("DOMContentLoaded", () => {
    initTabs();
    renderQueryList(allQueries);
    selectQuery(1);
    renderVivaQuestions(allVivaQuestions);

    fetchDiagnostics();
    fetchStats();
    fetchQueries();
    fetchVivaQuestions();
});

// ==============================================================================
// Tab Navigation
// ==============================================================================
function initTabs() {
    const tabButtons = document.querySelectorAll(".nav-btn");
    tabButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            tabButtons.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");

            const targetTab = btn.getAttribute("data-tab");
            document.querySelectorAll(".tab-content").forEach(content => {
                content.classList.remove("active");
            });
            const activeContent = document.getElementById(targetTab);
            if (activeContent) {
                activeContent.classList.add("active");
            }
        });
    });
}

// ==============================================================================
// Mode Switching (Local Demo Mode vs Hadoop Cluster Mode)
// ==============================================================================
async function switchMode(mode) {
    currentActiveMode = mode;
    try {
        await fetch("/api/mode", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ mode })
        });
    } catch (err) {
        console.warn("API mode toggle warning:", err);
    }

    updateModeUI(mode);
}

function updateModeUI(mode) {
    const localCard = document.getElementById("modeCardLocal");
    const clusterCard = document.getElementById("modeCardCluster");
    const badgeLocal = document.getElementById("badgeLocal");
    const badgeCluster = document.getElementById("badgeCluster");
    const headerModeLabel = document.getElementById("currentModeLabel");
    const engineTag = document.getElementById("execEngineTag");

    if (mode === "local") {
        if (localCard) localCard.classList.add("active-mode");
        if (clusterCard) clusterCard.classList.remove("active-mode");
        if (badgeLocal) {
            badgeLocal.className = "mode-badge active-badge";
            badgeLocal.textContent = "ACTIVE";
        }
        if (badgeCluster) {
            badgeCluster.className = "mode-badge inactive-badge";
            badgeCluster.textContent = "INACTIVE";
        }
        if (headerModeLabel) headerModeLabel.textContent = "LOCAL DEMO MODE";
        if (engineTag) engineTag.textContent = "Active Engine: Local Python / SQLite Simulation";
    } else {
        if (clusterCard) clusterCard.classList.add("active-mode");
        if (localCard) localCard.classList.remove("active-mode");
        if (badgeCluster) {
            badgeCluster.className = "mode-badge active-badge";
            badgeCluster.textContent = "ACTIVE";
        }
        if (badgeLocal) {
            badgeLocal.className = "mode-badge inactive-badge";
            badgeLocal.textContent = "INACTIVE";
        }
        if (headerModeLabel) headerModeLabel.textContent = "HADOOP CLUSTER MODE";
        if (engineTag) engineTag.textContent = "Active Engine: Apache Hive & HDFS Cluster";
    }
}

// ==============================================================================
// Diagnostics
// ==============================================================================
async function fetchDiagnostics() {
    const diagHadoopText = document.getElementById("diagHadoopBinText");
    const diagMessage = document.getElementById("diagMessage");
    const diagHadoopHome = document.getElementById("diagHadoopHome");
    const diagJava = document.getElementById("diagJava");

    try {
        const res = await fetch("/api/diagnostics");
        const data = await res.json();

        currentActiveMode = data.active_mode || "local";
        updateModeUI(currentActiveMode);

        if (diagHadoopText) {
            if (data.hadoop_bin_detected) {
                diagHadoopText.className = "status-success";
                diagHadoopText.textContent = "Detected & Online";
            } else {
                diagHadoopText.className = "status-warning";
                diagHadoopText.textContent = "Cloud / Local Active";
            }
        }

        if (diagMessage) diagMessage.textContent = data.diagnostics_message;
        if (diagHadoopHome) diagHadoopHome.textContent = data.hadoop_home;
        if (diagJava) diagJava.textContent = data.java_version || "Probed";
    } catch (err) {
        console.warn("Diagnostics error:", err);
        if (diagHadoopText) {
            diagHadoopText.className = "status-warning";
            diagHadoopText.textContent = "Cloud Standalone Active";
        }
    }
}

// ==============================================================================
// Quick Hadoop Terminal Commands Copy
// ==============================================================================
function copyTerminalCommands() {
    const commandsText = `hdfs dfs -mkdir -p /netflix/input
hdfs dfs -put dataset/netflix_titles.csv /netflix/input/
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \\
  -files hadoop/mapper.py,hadoop/reducer.py \\
  -mapper "python3 mapper.py" \\
  -reducer "python3 reducer.py" \\
  -input /netflix/input/netflix_titles.csv \\
  -output /netflix/output
hdfs dfs -cat /netflix/output/part-* | head -n 20`;

    navigator.clipboard.writeText(commandsText).then(() => {
        const btn = document.querySelector(".copy-all-btn");
        if (btn) {
            const originalText = btn.innerHTML;
            btn.innerHTML = "✅ Copied to Clipboard!";
            setTimeout(() => { btn.innerHTML = originalText; }, 2000);
        }
    });
}

// ==============================================================================
// KPIs & Stats
// ==============================================================================
async function fetchStats() {
    try {
        const res = await fetch("/api/stats");
        const data = await res.json();
        const total = document.getElementById("kpiTotal");
        const movies = document.getElementById("kpiMovies");
        const tv = document.getElementById("kpiTv");
        const countries = document.getElementById("kpiCountries");

        if (total) total.textContent = Number(data.total_titles).toLocaleString();
        if (movies) movies.textContent = Number(data.movies).toLocaleString();
        if (tv) tv.textContent = Number(data.tv_shows).toLocaleString();
        if (countries) countries.textContent = data.countries;
    } catch (err) {
        console.warn("Stats fetch fallback:", err);
        // Fallback default stats
        document.getElementById("kpiTotal").textContent = "6,234";
        document.getElementById("kpiMovies").textContent = "4,265";
        document.getElementById("kpiTv").textContent = "1,969";
        document.getElementById("kpiCountries").textContent = "51";
    }
}

// ==============================================================================
// HiveQL Query Studio
// ==============================================================================
async function fetchQueries() {
    try {
        const res = await fetch("/api/queries");
        const serverQueries = await res.json();
        if (Array.isArray(serverQueries) && serverQueries.length > 0) {
            allQueries = serverQueries;
            renderQueryList(allQueries);
            selectQuery(allQueries[0].id);
        }
    } catch (err) {
        console.warn("Queries fetch fallback to local:", err);
    }
}

function renderQueryList(queries) {
    const container = document.getElementById("queryListContainer");
    if (!container) return;
    container.innerHTML = "";
    queries.forEach(q => {
        const item = document.createElement("div");
        item.className = `query-item ${q.id === currentQueryId ? 'selected' : ''}`;
        item.id = `queryItem_${q.id}`;
        item.onclick = () => selectQuery(q.id);

        item.innerHTML = `
            <div class="qi-num">QUERY ${q.id} • ${q.category}</div>
            <div class="qi-title">${q.title}</div>
        `;
        container.appendChild(item);
    });
}

function selectQuery(id) {
    currentQueryId = id;
    document.querySelectorAll(".query-item").forEach(el => el.classList.remove("selected"));
    const selectedEl = document.getElementById(`queryItem_${id}`);
    if (selectedEl) selectedEl.classList.add("selected");

    const query = allQueries.find(q => q.id === id);
    if (!query) return;

    const catEl = document.getElementById("activeQueryCategory");
    const titleEl = document.getElementById("activeQueryTitle");
    const expEl = document.getElementById("activeQueryExplanation");
    const sqlEl = document.getElementById("activeQuerySql");
    const statusEl = document.getElementById("resultsStatusText");
    const timeBadge = document.getElementById("execTimeBadge");
    const thRow = document.getElementById("tableHeadRow");
    const tBody = document.getElementById("tableBody");

    if (catEl) catEl.textContent = query.category;
    if (titleEl) titleEl.textContent = `Query ${query.id}: ${query.title}`;
    if (expEl) expEl.textContent = query.explanation;
    if (sqlEl) sqlEl.textContent = query.hiveql;

    // Reset results table preview
    if (statusEl) statusEl.textContent = `Ready. Expected: ${query.expected}`;
    if (timeBadge) timeBadge.style.display = "none";
    if (thRow) thRow.innerHTML = `<th>Output for Query ${query.id}</th>`;
    if (tBody) tBody.innerHTML = `<tr><td class="text-muted">Click "Execute Query" above to compute live results.</td></tr>`;
}

async function executeCurrentQuery() {
    const runBtn = document.getElementById("runQueryBtn");
    if (runBtn) {
        runBtn.disabled = true;
        runBtn.textContent = "⏳ Running...";
    }

    try {
        const res = await fetch("/api/run-query", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query_id: currentQueryId })
        });
        const data = await res.json();

        // Update status bar
        const statusEl = document.getElementById("resultsStatusText");
        if (statusEl) statusEl.textContent = `Completed: ${data.rows.length} rows returned.`;
        
        const timeBadge = document.getElementById("execTimeBadge");
        if (timeBadge) {
            timeBadge.textContent = `${data.elapsed_ms} ms`;
            timeBadge.style.display = "inline-block";
        }

        // Render table
        renderTable(data.columns, data.rows);
    } catch (err) {
        console.error("Execute query error:", err);
        const statusEl = document.getElementById("resultsStatusText");
        if (statusEl) statusEl.textContent = "Error executing query.";
    } finally {
        if (runBtn) {
            runBtn.disabled = false;
            runBtn.textContent = "▶ Execute Query";
        }
    }
}

function renderTable(columns, rows) {
    const thead = document.getElementById("tableHeadRow");
    const tbody = document.getElementById("tableBody");
    if (!thead || !tbody) return;

    thead.innerHTML = columns.map(c => `<th>${c}</th>`).join("");
    if (rows.length === 0) {
        tbody.innerHTML = `<tr><td colspan="${columns.length}" class="text-muted">No rows returned.</td></tr>`;
        return;
    }

    tbody.innerHTML = rows.slice(0, 50).map(row => {
        return `<tr>${row.map(val => `<td>${val !== null ? val : '<em>NULL</em>'}</td>`).join("")}</tr>`;
    }).join("");
}

// ==============================================================================
// MapReduce Runner
// ==============================================================================
async function runMapReduceJob() {
    const selector = document.getElementById("mrJobSelector");
    const job = selector ? selector.value : "type";
    const btn = document.querySelector(".run-mr-btn");
    if (btn) {
        btn.disabled = true;
        btn.textContent = "⏳ Running MapReduce Pipeline...";
    }

    try {
        const res = await fetch("/api/run-mapreduce", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ job })
        });
        const data = await res.json();

        const mapDesc = document.getElementById("mrMapDesc");
        const redDesc = document.getElementById("mrReduceDesc");
        const mapOut = document.getElementById("mrSampleMapOutput");
        const redOut = document.getElementById("mrSampleReduceOutput");

        if (mapDesc) mapDesc.textContent = `Emitted ${data.map_count.toLocaleString()} pairs`;
        if (redDesc) redDesc.textContent = `Aggregated ${data.reduce_count.toLocaleString()} keys (${data.elapsed_ms}ms)`;

        if (mapOut) mapOut.textContent = data.sample_mapped.join("\n") + "\n... (more records streamed)";

        const formattedReduced = data.reduced_records.map(r => r.join("\t")).join("\n");
        if (redOut) redOut.textContent = formattedReduced;
    } catch (err) {
        console.error("MapReduce run error:", err);
    } finally {
        if (btn) {
            btn.disabled = false;
            btn.textContent = "🚀 Run MapReduce Pipeline";
        }
    }
}

// ==============================================================================
// Viva Voce Flashcards
// ==============================================================================
async function fetchVivaQuestions() {
    try {
        const res = await fetch("/api/viva");
        const serverViva = await res.json();
        if (Array.isArray(serverViva) && serverViva.length > 0) {
            allVivaQuestions = serverViva;
            renderVivaQuestions(allVivaQuestions);
        }
    } catch (err) {
        console.warn("Viva fetch fallback to local:", err);
    }
}

function renderVivaQuestions(questions) {
    const container = document.getElementById("vivaGridContainer");
    if (!container) return;
    container.innerHTML = "";

    if (questions.length === 0) {
        container.innerHTML = `<p class="text-muted">No questions found matching your filter.</p>`;
        return;
    }

    questions.forEach((q, idx) => {
        const card = document.createElement("div");
        card.className = "viva-card";
        card.innerHTML = `
            <div>
                <div class="viva-category">Q${idx + 1} • ${q.category}</div>
                <div class="viva-question">${q.q}</div>
            </div>
            <div class="viva-answer">${q.a}</div>
        `;
        container.appendChild(card);
    });
}

function filterVivaQuestions() {
    const searchInput = document.getElementById("vivaSearchInput");
    const query = searchInput ? searchInput.value.toLowerCase() : "";
    const activeFilterBtn = document.querySelector(".filter-btn.active");
    const category = activeFilterBtn ? activeFilterBtn.textContent.split(" ")[0] : "All";

    let filtered = allVivaQuestions;
    if (category !== "All") {
        filtered = filtered.filter(q => q.category === category);
    }
    if (query) {
        filtered = filtered.filter(q => q.q.toLowerCase().includes(query) || q.a.toLowerCase().includes(query));
    }
    renderVivaQuestions(filtered);
}

function filterCategory(category) {
    document.querySelectorAll(".filter-btn").forEach(b => b.classList.remove("active"));
    if (event && event.target) event.target.classList.add("active");
    filterVivaQuestions();
}

// ==============================================================================
// High-Res Image Modal
// ==============================================================================
function openModal(src, caption) {
    const modal = document.getElementById("imageModal");
    const modalImg = document.getElementById("modalImg");
    const captionText = document.getElementById("modalCaption");

    if (modal && modalImg && captionText) {
        modal.classList.add("open");
        modalImg.src = src;
        captionText.textContent = caption;
    }
}

function closeModal() {
    const modal = document.getElementById("imageModal");
    if (modal) modal.classList.remove("open");
}
