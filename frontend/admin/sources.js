const API_BASE = "http://127.0.0.1:8000/api/v1";
const token = localStorage.getItem("jkpulse_admin_token");

if (!token) {
    window.location.href = "login.html";
}

const tbody = document.getElementById("source-table-body");
const form = document.getElementById("source-form");
const toggleFormBtn = document.getElementById("toggle-form");
const message = document.getElementById("message");

function headers() {
    return {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
    };
}

async function loadSources() {
    try {
        const response = await fetch(`${API_BASE}/admin/sources`, {
            headers: headers()
        });

        if (response.status === 401 || response.status === 403) {
            localStorage.removeItem("jkpulse_admin_token");
            window.location.href = "login.html";
            return;
        }

        if (!response.ok) throw new Error("Unable to load sources");

        const sources = await response.json();
        tbody.innerHTML = "";

        if (!sources.length) {
            tbody.innerHTML = '<tr><td colspan="6">No sources registered yet.</td></tr>';
            return;
        }

        sources.forEach(source => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${escapeHTML(source.name)}</td>
                <td><a href="${escapeHTML(source.website_url)}" target="_blank" rel="noopener noreferrer">Visit</a></td>
                <td>${escapeHTML(source.source_type)}</td>
                <td>${source.is_active ? "Yes" : "No"}</td>
                <td>${source.monitoring_enabled ? "On" : "Off"}</td>
                <td>
                    <button class="action-btn" data-action="active" data-id="${source.id}">
                        ${source.is_active ? "Deactivate" : "Activate"}
                    </button>
                    <button class="action-btn" data-action="monitor" data-id="${source.id}">
                        ${source.monitoring_enabled ? "Stop Monitoring" : "Monitor"}
                    </button>
                </td>
            `;
            tbody.appendChild(row);
        });
    } catch (error) {
        tbody.innerHTML = '<tr><td colspan="6">Error loading sources.</td></tr>';
    }
}

function escapeHTML(value) {
    return String(value ?? "").replace(/[&<>"']/g, character => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
    }[character]));
}

toggleFormBtn.addEventListener("click", () => {
    form.classList.toggle("hidden");
});

form.addEventListener("submit", async event => {
    event.preventDefault();
    message.textContent = "Saving...";

    const payload = {
        name: document.getElementById("source-name").value.trim(),
        website_url: document.getElementById("source-url").value.trim(),
        source_type: document.getElementById("source-type").value,
        region: document.getElementById("source-region").value.trim()
    };

    try {
        const response = await fetch(`${API_BASE}/admin/sources?${new URLSearchParams(payload)}`, {
            method: "POST",
            headers: headers()
        });

        const result = await response.json();

        if (!response.ok) {
            message.textContent = result.detail || "Failed to save source.";
            return;
        }

        message.textContent = "Source saved successfully.";
        form.reset();
        form.classList.add("hidden");
        await loadSources();
    } catch (error) {
        message.textContent = "Connection error. Please try again.";
    }
});

tbody.addEventListener("click", async event => {
    const button = event.target.closest("button[data-action]");
    if (!button) return;

    const id = button.dataset.id;
    const action = button.dataset.action;

    let endpoint = "";
    if (action === "active") endpoint = `/admin/sources/${id}/active`;
    if (action === "monitor") endpoint = `/admin/sources/${id}/monitoring`;

    const currentText = button.textContent;
    button.disabled = true;
    button.textContent = "Updating...";

    try {
        const response = await fetch(`${API_BASE}${endpoint}?enabled=${action === "active" ? currentText.trim() === "Deactivate" : currentText.trim() === "Stop Monitoring"}`, {
            method: "PATCH",
            headers: headers()
        });

        if (!response.ok) throw new Error("Update failed");
        await loadSources();
    } catch (error) {
        button.disabled = false;
        button.textContent = currentText;
        alert("Unable to update source.");
    }
});

document.getElementById("logout-btn").addEventListener("click", () => {
    localStorage.removeItem("jkpulse_admin_token");
    window.location.href = "login.html";
});

loadSources();
