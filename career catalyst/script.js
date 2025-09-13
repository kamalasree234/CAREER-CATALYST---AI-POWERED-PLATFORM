async function fetchHistory(userId) {
    try {
        let response = await fetch(`http://127.0.0.1:8000/history/${userId}`);
        let data = await response.json();
        console.log("User History:", data);
        
        // Display history in HTML
        let historyContainer = document.getElementById("history-container");
        historyContainer.innerHTML = "";
        
        if (data.history.length > 0) {
            data.history.forEach(item => {
                historyContainer.innerHTML += `<p>${item}</p>`;
            });
        } else {
            historyContainer.innerHTML = "<p>Nothing to show here</p>";
        }
    } catch (error) {
        console.error("Error fetching history:", error);
    }
}

// Call function after user logs in
fetchHistory("USER_ID_HERE");

async function fetchInterests(userId) {
    try {
        let response = await fetch(`http://127.0.0.1:8000/interests/${userId}`);
        let data = await response.json();

        let container = document.getElementById("interests-container");
        container.innerHTML = "";

        if (data.interests) {
            data.interests.forEach(interest => {
                container.innerHTML += `<p>Suggested Career: ${interest}</p>`;
            });
        } else {
            container.innerHTML = "<p>Nothing to show here</p>";
        }
    } catch (error) {
        console.error("Error fetching interests:", error);
    }
}

