import {auth,signInWithEmailAndPassword}from "../firebase/auth.js";


const submit = document.getElementById('submit')
submit.addEventListener('click',function(event){
    event.preventDefault()
    const email = document.getElementById('email').value
    const password = document.getElementById('password').value
    signInWithEmailAndPassword(auth,email,password)
    .then((userCredential) => {
        //Logged in
        const user = userCredential.user;
        // get user id 
        console.log(user.uid)
        window.location.href = 'home.html'
    })
    .catch((error) => {
        const errorCode = error.code;
        const errorMessage = error.message;
    })
})