import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.10/firebase-app.js";
import { getAuth, signInWithPopup, GoogleAuthProvider } from "https://www.gstatic.com/firebasejs/9.6.10/firebase-auth.js";
const firebaseConfig = {
  
};

firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();

const provider = new GoogleAuthProvider();

// Google Sign-In
async function googleSignIn() {
    const provider = new firebase.auth.GoogleAuthProvider();
    try {
        let result = await auth.signInWithPopup(provider);
        let user = result.user;
        let idToken = await user.getIdToken(); // Get JWT token
        console.log("Google Sign-In Success:", user);
        
        // Send token to backend for verification
        await fetch("http://127.0.0.1:8000/register-user", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ uid: user.uid, email: user.email, token: idToken })
        });

        alert("User registered successfully!");
        window.location.href = "loggedin.html"; 
    } catch (error) {
        console.error("Google Sign-In Error:", error);
    }
}
