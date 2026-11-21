const API_BASE = "http://127.0.0.1:8000/api/v1";

async function loadArticles() {
    const token = localStorage.getItem("jkpulse_admin_token");

    if (!token) {
        window.location.href = "login.html";
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/admin/articles`, {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (response.status === 401 || response.status === 403) {
            localStorage.removeItem("jkpulse_admin_token");
            window.location.href = "login.html";
            return;
        }

        if (!response.ok) throw new Error("Failed to load articles");

        const articles = await response.json();
        const tbody = document.getElementById("article-table-body");

        tbody.replaceChildren();

        if (!articles.length) {
            const row = tbody.insertRow();
            const cell = row.insertCell();
            cell.colSpan = 3;
            cell.textContent = "No articles found.";
            return;
        }

        articles.forEach(article => {
            const row = tbody.insertRow();

            const titleCell = row.insertCell();
            titleCell.textContent = article.title || "Untitled";

            const statusCell = row.insertCell();
            const badge = document.createElement("span");
            badge.className = "status-badge";
            badge.textContent = article.status || "draft";
            statusCell.appendChild(badge);

            const verifiedCell = row.insertCell();
            verifiedCell.textContent = article.is_verified ? "Yes" : "No";
        });
    } catch (error) {
        document.getElementById("article-table-body").textContent =
            "Unable to load articles. Check backend connection.";
    }
}

const logoutBtn = document.getElementById("logout-btn");
if (logoutBtn) {
    logoutBtn.addEventListener("click", () => {
        localStorage.removeItem("jkpulse_admin_token");
        window.location.href = "login.html";
    });
}

const newArticleBtn = document.getElementById("new-article-btn");
if (newArticleBtn) {
    newArticleBtn.addEventListener("click", () => {
        window.location.href = "create-article.html";
    });
}

loadArticles();
