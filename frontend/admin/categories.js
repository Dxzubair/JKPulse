const API_BASE = "http://127.0.0.1:8000/api/v1";
const token = localStorage.getItem("jkpulse_admin_token");

if (!token) {
    window.location.href = "login.html";
}

const tbody = document.getElementById("category-table-body");
const form = document.getElementById("category-form");
const toggleFormBtn = document.getElementById("toggle-form");
const message = document.getElementById("message");

function headers() {
    return {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
    };
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

async function loadCategories() {
    try {
        const response = await fetch(`${API_BASE}/categories`);
        if (!response.ok) throw new Error("Failed");

        const categories = await response.json();
        tbody.innerHTML = "";

        if (!categories.length) {
            tbody.innerHTML = '<tr><td colspan="3">No categories found.</td></tr>';
            return;
        }

        categories.forEach(category => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${escapeHTML(category.name)}</td>
                <td>${escapeHTML(category.slug)}</td>
                <td>${escapeHTML(category.description || "")}</td>
            `;
            tbody.appendChild(row);
        });
    } catch (error) {
        tbody.innerHTML = '<tr><td colspan="3">Unable to load categories.</td></tr>';
    }
}

toggleFormBtn.addEventListener("click", () => {
    form.classList.toggle("hidden");
});

document.getElementById("category-name").addEventListener("input", event => {
    const slugInput = document.getElementById("category-slug");
    if (!slugInput.dataset.edited) {
        slugInput.value = event.target.value
            .toLowerCase()
            .trim()
            .replace(/[^a-z0-9]+/g, "-")
            .replace(/^-|-$/g, "");
    }
});

document.getElementById("category-slug").addEventListener("input", event => {
    event.target.dataset.edited = "true";
});

form.addEventListener("submit", async event => {
    event.preventDefault();
    message.textContent = "Saving category...";

    const payload = {
        name: document.getElementById("category-name").value.trim(),
        slug: document.getElementById("category-slug").value.trim(),
        description: document.getElementById("category-description").value.trim()
    };

    try {
        const params = new URLSearchParams(payload);
        const response = await fetch(`${API_BASE}/admin/categories?${params}`, {
            method: "POST",
            headers: headers()
        });

        const result = await response.json();

        if (!response.ok) {
            message.textContent = result.detail || "Unable to save category.";
            return;
        }

        message.textContent = "Category created successfully.";
        form.reset();
        document.getElementById("category-slug").dataset.edited = "";
        form.classList.add("hidden");
        await loadCategories();
    } catch (error) {
        message.textContent = "Connection error.";
    }
});

document.getElementById("logout-btn").addEventListener("click", () => {
    localStorage.removeItem("jkpulse_admin_token");
    window.location.href = "login.html";
});

loadCategories();
