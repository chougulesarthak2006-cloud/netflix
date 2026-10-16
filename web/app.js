/**
 * app.js
 * ------
 * Frontend interactive logic for Netflix Big Data Analytics Platform.
 */

let allQueries = [];
let allVivaQuestions = [];
let currentQueryId = 1;
let currentActiveMode = "local";

document.addEventListener("DOMContentLoaded", () => {
    initTabs();
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
        localCard.classList.add("active-mode");
        clusterCard.classList.remove("active-mode");
        badgeLocal.className = "mode-badge active-badge";
        badgeLocal.textContent = "ACTIVE";
        badgeCluster.className = "mode-badge inactive-badge";
        badgeCluster.textContent = "INACTIVE";
        headerModeLabel.textContent = "LOCAL DEMO MODE";
        if (engineTag) engineTag.textContent = "Active Engine: Local Python / SQLite Simulation";
    } else {
        clusterCard.classList.add("active-mode");
        localCard.classList.remove("active-mode");
        badgeCluster.className = "mode-badge active-badge";
        badgeCluster.textContent = "ACTIVE";
        badgeLocal.className = "mode-badge inactive-badge";
        badgeLocal.textContent = "INACTIVE";
        headerModeLabel.textContent = "HADOOP CLUSTER MODE";
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

        if (data.hadoop_bin_detected) {
            diagHadoopText.className = "status-success";
            diagHadoopText.textContent = "Detected & Online";
        } else {
            diagHadoopText.className = "status-warning";
            diagHadoopText.textContent = "Not Found on System";
        }

        diagMessage.textContent = data.diagnostics_message;
        diagHadoopHome.textContent = data.hadoop_home;
        diagJava.textContent = data.java_version || "Probed";
    } catch (err) {
        console.error("Diagnostics error:", err);
        diagHadoopText.className = "status-warning";
        diagHadoopText.textContent = "Local Standalone Active";
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
        const originalText = btn.innerHTML;
        btn.innerHTML = "✅ Copied to Clipboard!";
        setTimeout(() => { btn.innerHTML = originalText; }, 2000);
    });
}

// ==============================================================================
// KPIs & Stats
// ==============================================================================
async function fetchStats() {
    try {
        const res = await fetch("/api/stats");
        const data = await res.json();
        document.getElementById("kpiTotal").textContent = Number(data.total_titles).toLocaleString();
        document.getElementById("kpiMovies").textContent = Number(data.movies).toLocaleString();
        document.getElementById("kpiTv").textContent = Number(data.tv_shows).toLocaleString();
        document.getElementById("kpiCountries").textContent = data.countries;
    } catch (err) {
        console.error("Stats fetch error:", err);
    }
}

// ==============================================================================
// HiveQL Query Studio
// ==============================================================================
async function fetchQueries() {
    try {
        const res = await fetch("/api/queries");
        allQueries = await res.json();
        renderQueryList(allQueries);
        if (allQueries.length > 0) {
            selectQuery(allQueries[0].id);
        }
    } catch (err) {
        console.error("Queries fetch error:", err);
    }
}

function renderQueryList(queries) {
    const container = document.getElementById("queryListContainer");
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

    document.getElementById("activeQueryCategory").textContent = query.category;
    document.getElementById("activeQueryTitle").textContent = `Query ${query.id}: ${query.title}`;
    document.getElementById("activeQueryExplanation").textContent = query.explanation;
    document.getElementById("activeQuerySql").textContent = query.hiveql;

    // Reset results table preview
    document.getElementById("resultsStatusText").textContent = `Ready. Expected: ${query.expected}`;
    document.getElementById("execTimeBadge").style.display = "none";
    document.getElementById("tableHeadRow").innerHTML = `<th>Output for Query ${query.id}</th>`;
    document.getElementById("tableBody").innerHTML = `<tr><td class="text-muted">Click "Execute Query" above to compute live results.</td></tr>`;
}

async function executeCurrentQuery() {
    const runBtn = document.getElementById("runQueryBtn");
    runBtn.disabled = true;
    runBtn.textContent = "⏳ Running...";

    try {
        const res = await fetch("/api/run-query", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query_id: currentQueryId })
        });
        const data = await res.json();

        // Update status bar
        document.getElementById("resultsStatusText").textContent = `Completed: ${data.rows.length} rows returned.`;
        const timeBadge = document.getElementById("execTimeBadge");
        timeBadge.textContent = `${data.elapsed_ms} ms`;
        timeBadge.style.display = "inline-block";

        // Render table
        renderTable(data.columns, data.rows);
    } catch (err) {
        console.error("Execute query error:", err);
        document.getElementById("resultsStatusText").textContent = "Error executing query.";
    } finally {
        runBtn.disabled = false;
        runBtn.textContent = "▶ Execute Query";
    }
}

function renderTable(columns, rows) {
    const thead = document.getElementById("tableHeadRow");
    const tbody = document.getElementById("tableBody");

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
    const job = selector.value;
    const btn = document.querySelector(".run-mr-btn");
    btn.disabled = true;
    btn.textContent = "⏳ Running MapReduce Pipeline...";

    try {
        const res = await fetch("/api/run-mapreduce", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ job })
        });
        const data = await res.json();

        document.getElementById("mrMapDesc").textContent = `Emitted ${data.map_count.toLocaleString()} pairs`;
        document.getElementById("mrReduceDesc").textContent = `Aggregated ${data.reduce_count.toLocaleString()} keys (${data.elapsed_ms}ms)`;

        document.getElementById("mrSampleMapOutput").textContent = data.sample_mapped.join("\n") + "\n... (more records streamed)";

        const formattedReduced = data.reduced_records.map(r => r.join("\t")).join("\n");
        document.getElementById("mrSampleReduceOutput").textContent = formattedReduced;
    } catch (err) {
        console.error("MapReduce run error:", err);
    } finally {
        btn.disabled = false;
        btn.textContent = "🚀 Run MapReduce Pipeline";
    }
}

// ==============================================================================
// Viva Voce Flashcards
// ==============================================================================
async function fetchVivaQuestions() {
    try {
        const res = await fetch("/api/viva");
        allVivaQuestions = await res.json();
        renderVivaQuestions(allVivaQuestions);
    } catch (err) {
        console.error("Viva fetch error:", err);
    }
}

function renderVivaQuestions(questions) {
    const container = document.getElementById("vivaGridContainer");
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
    const query = document.getElementById("vivaSearchInput").value.toLowerCase();
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
    event.target.classList.add("active");
    filterVivaQuestions();
}

// ==============================================================================
// High-Res Image Modal
// ==============================================================================
function openModal(src, caption) {
    const modal = document.getElementById("imageModal");
    const modalImg = document.getElementById("modalImg");
    const captionText = document.getElementById("modalCaption");

    modal.classList.add("open");
    modalImg.src = src;
    captionText.textContent = caption;
}

function closeModal() {
    document.getElementById("imageModal").classList.remove("open");
}
