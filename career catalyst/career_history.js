const API_URL = "http://127.0.0.1:8000"; // FastAPI server URL

// ✅ Fetch Career History from FastAPI
async function fetchHistory() {
    const userId = localStorage.getItem("user_id"); // Retrieve user ID from local storage

    if (!userId) {
        alert("User not logged in!");
        return;
    }

    try {
        const response = await fetch(`${API_URL}/get_history/${userId}`);
        const data = await response.json();

        if (data.history.length === 0) {
            document.getElementById("history-list").innerHTML = "<li>No search history found.</li>";
            return;
        }

        // ✅ Display history in HTML
        let historyHTML = "";
        data.history.forEach(entry => {
            historyHTML += `<li><a href="${entry.link}" target="_blank">${entry.career}</a></li>`;
        });

        document.getElementById("history-list").innerHTML = historyHTML;
    } catch (error) {
        console.error("Error fetching history:", error);
        alert("Failed to load history.");
    }
}

// ✅ Fetch User Email (if needed)
document.addEventListener("DOMContentLoaded", () => {
    const userEmail = localStorage.getItem("user_email");
    if (userEmail) {
        document.getElementById("user-email").innerText = userEmail;
    }
});
