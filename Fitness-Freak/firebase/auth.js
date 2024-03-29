// auth.js
import { getAuth,signInWithEmailAndPassword, onAuthStateChanged, signOut } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-auth.js";
import firebaseApp from "./firebaseConfig.js";

const auth = getAuth(firebaseApp);

auth.onAuthStateChanged((user) => {
    const logoutBtn = document.getElementById('logoutBtn');
    if (user) {
        // If user is signed in, display the logout button
        logoutBtn.style.display = 'block';
    } else {
        // If no user is signed in, hide the logout button
        logoutBtn.style.display = 'none';
    }
});
export { auth, signInWithEmailAndPassword, signOut };