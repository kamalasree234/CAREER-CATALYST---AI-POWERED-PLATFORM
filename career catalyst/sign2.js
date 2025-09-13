import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.10/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword, GoogleAuthProvider } from "https://www.gstatic.com/firebasejs/9.6.10/firebase-auth.js";
import { getFirestore, doc, setDoc } from "https://www.gstatic.com/firebasejs/9.6.10/firebase-firestore.js";

// Firebase Configuration


// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);



document.getElementById("signup-btn").addEventListener("click", async (e) => {
    e.preventDefault();

    let username = document.querySelector(".sign-up input[type='text']").value;
    let email = document.getElementById("signup-email").value;
    let password = document.getElementById("signup-password").value;

    try {
        const userCredential = await createUserWithEmailAndPassword(auth, email, password);
        const user = userCredential.user;

        // ✅ Store user data in Firestore
        await setDoc(doc(db, "users", user.uid), {
            username: username,
            email: email,
            userId: user.uid,
            createdAt: new Date().toISOString()
        });

        alert("Sign up successful! Redirecting...");
        window.location.href = "loggedin.html"; // Redirect after successful sign-up
    } catch (error) {
        alert(error.message);
    }
});



    







