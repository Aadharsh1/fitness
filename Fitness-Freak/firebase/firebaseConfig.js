// firebaseConfig.js
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-app.js";

const firebaseConfig = {
    // Your Firebase configuration object
    apiKey: "AIzaSyDzm7l9LUW5vKSIZddGMNDShKvMirdnRN4",
    authDomain: "fitness-freak-94e2d.firebaseapp.com",
    projectId: "fitness-freak-94e2d",
    storageBucket: "fitness-freak-94e2d.appspot.com",
    messagingSenderId: "187581241780",
    appId: "1:187581241780:web:2b424800cd26d69259fae1",
    measurementId: "G-LZK993K4RC"
};

const firebaseApp = initializeApp(firebaseConfig);
export default firebaseApp;