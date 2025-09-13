import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-app.js";
import { getAuth, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-auth.js";

// Firebase Configuration


// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// Function to handle career search
async function searchCareer() {
    let career = document.getElementById('career').value;
    if (!career) {
        alert("Enter a career!");
        return;
    }

    // Get logged-in user
    auth.onAuthStateChanged(async function(user) {
        if (user) {
            let user_id = user.uid;

            let response = await fetch('/search', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ career: career, user_id: user_id })
            });

            let result = await response.json();
            alert(result.message);
            loadHistory();  // Reload history after search
        } else {
            alert("Please log in first!");
        }
    });
}

// Function to load search history
async function loadHistory() {
    auth.onAuthStateChanged(async function(user) {
        if (user) {
            let user_id = user.uid;

            let response = await fetch('/history', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: user_id })
            });

            let result = await response.json();
            let historyList = document.getElementById('historyList');
            historyList.innerHTML = "";

            if (result.history) {
                result.history.forEach(entry => {
                    let li = document.createElement('li');
                    li.innerText = entry.career;
                    historyList.appendChild(li);
                });
            }
        }
    });
}

// Add event listener to "My History" button in loggedin.html
document.addEventListener("DOMContentLoaded", function () {
    let historyBtn = document.getElementById("historyButton"); // Ensure the button has this ID
    if (historyBtn) {
        historyBtn.addEventListener("click", loadHistory);
    }
});

// Load history when the page loads
window.onload = loadHistory;
