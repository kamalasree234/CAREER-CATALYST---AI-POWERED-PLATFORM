import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.10/firebase-app.js";
import { getAuth, onAuthStateChanged, signOut } from "https://www.gstatic.com/firebasejs/9.6.10/firebase-auth.js";

const firebaseConfig = {
  
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// Check if user is logged in
onAuthStateChanged(auth, (user) => {
    if (user) {
        document.getElementById("user-email").innerText = user.email;
    } else {
        console.log("No user detected, redirecting...");
        window.location.href = "index.html"; // Redirect immediately
    }
});

// Logout functionality
document.getElementById("logout-btn").addEventListener("click", () => {
    signOut(auth).then(() => {
        window.location.href = "signup.html"; // Redirect to sign-in page
    }).catch((error) => {
        console.error("Logout Error:", error);
    });
});

