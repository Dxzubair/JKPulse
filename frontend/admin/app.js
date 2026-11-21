const API_BASE = "http://127.0.0.1:8000/api/v1";

function checkAuth() {
    const token = localStorage.getItem("jkpulse_admin_token");

    if (!token) {
        window.location.href = "login.html";
        return null;
    }

    return token;
}

async function loadDashboard() {
    const token = checkAuth();
    if (!token) return;

    try {
        const response = await fetch(`${API_BASE}/admin/stats`, {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (response.status === 401 || response.status === 403) {
            localStorage.removeItem("jkpulse_admin_token");
            window.location.href = "login.html";
            return;
        }

        if (!response.ok) {
            throw new Error("Unable to load statistics");
        }

        const stats = await response.json();

        document.getElementById("total-articles").textContent = stats.total_articles;
        document.getElementById("published-articles").textContent = stats.published_articles;
        document.getElementById("draft-articles").textContent = stats.draft_articles;
        document.getElementById("verified-articles").textContent = stats.verified_articles;
        document.getElementById("total-categories").textContent = stats.total_categories;
        document.getElementById("total-sources").textContent = stats.total_sources;

        document.querySelector(".status").textContent = "Connected to JK Pulse API.";
    } catch (error) {
        document.querySelector(".status").textContent = "Unable to connect to the backend API.";
    }
}

loadDashboard();


const logoutBtn = document.getElementById("logout-btn");

if (logout_btn) {
    logout_btn.addEventListener("click", () => {
        localStorage.removeItem("jkpulse_admin_token");
        window.location.href = "login.html";
    });
}
