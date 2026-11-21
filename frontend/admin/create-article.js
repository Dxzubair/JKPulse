const API_BASE = "http://127.0.0.1:8000/api/v1";
const token = localStorage.getItem("jkpulse_admin_token");

if (!token) {
    window.location.href = "login.html";
}

async function loadCategories() {
    const select = document.getElementById("category");

    try {
        const response = await fetch(`${API_BASE}/categories`);
        if (!response.ok) throw new Error();

        const categories = await response.json();
        select.replaceChildren();

        const placeholder = document.createElement("option");
        placeholder.value = "";
        placeholder.textContent = "Select category";
        select.appendChild(placeholder);

        categories.forEach(category => {
            const option = document.createElement("option");
            option.value = category.id;
            option.textContent = category.name;
            select.appendChild(option);
        });
    } catch {
        select.replaceChildren();
        const option = document.createElement("option");
        option.value = "";
        option.textContent = "Unable to load categories";
        select.appendChild(option);
    }
}

document.getElementById("article-form").addEventListener("submit", async function(event) {
    event.preventDefault();

    const message = document.getElementById("message");
    const button = this.querySelector('button[type="submit"]');
    button.disabled = true;
    message.textContent = "Saving draft...";
    message.style.color = "#64748b";

    const payload = {
        title: document.getElementById("title").value.trim(),
        summary: document.getElementById("summary").value.trim(),
        content: document.getElementById("content").value.trim(),
        category_id: Number(document.getElementById("category").value),
        organization: document.getElementById("organization").value.trim() || null,
        source_url: document.getElementById("source-url").value.trim() || null,
        official_pdf_url: document.getElementById("pdf-url").value.trim() || null,
        application_url: document.getElementById("application-url").value.trim() || null
    };

    try {
        const response = await fetch(`${API_BASE}/admin/articles`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(typeof data.detail === "string" ? data.detail : "Failed to save article");
        }

        message.textContent = "Draft saved successfully.";
        message.style.color = "#15803d";
        this.reset();
    } catch (error) {
        message.textContent = error.message || "Unable to save draft.";
        message.style.color = "#dc2626";
    } finally {
        button.disabled = false;
    }
});

document.getElementById("cancel-btn").addEventListener("click", () => {
    window.location.href = "articles.html";
});

document.getElementById("logout-btn")?.addEventListener("click", () => {
    localStorage.removeItem("jkpulse_admin_token");
    window.location.href = "login.html";
});

loadCategories();
