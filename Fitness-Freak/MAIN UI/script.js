import {auth, signOut} from "../firebase/auth.js";

window.uid = null

const logoutBtn = document.getElementById('logoutBtn');
logoutBtn.addEventListener('click', () => {
  // Call the signOut method to sign the user out
  signOut(auth)
    .then(() => {
      // Sign-out successful, redirect to the login page or perform other actions
      console.log("User signed out");
      window.location.href = 'login.html'; // Redirect to the login page
    })
    .catch((error) => {
      // An error occurred while signing out
      console.error("Error signing out:", error.message);
      // You can handle errors here, such as displaying an error message to the user
    });
});

// Listen for authentication state changes
auth.onAuthStateChanged((user) => {
    if (user) {
      // User is signed in, redirect to home.html
      window.uid = user.uid
      console.log("User is signed in:", user.uid);
      
    } else {
      // No user is signed in
      console.log("No user is signed in");
    }
  });


function fetchWorkoutPlans() {
    // var userId = 'Dxmg1VHpYHeWnGkIShfV';
    // hardcoded the userId cause idk how we gonna manage like user session and get the userid of the currently logged in user
    // this function will call the complex microsrvice, getworkouplan with the user id and pass in the returned workout plan into the displayWorkoutPlan function below
    fetch(`http://127.0.0.1:5002/get_workout_plan/${uid}`)
        .then(response => response.json())
        .then(data => {
            displayWorkoutPlans(data); 
        });
}

window.fetchWorkoutPlans = fetchWorkoutPlans;

function displayWorkoutPlans(data) {
    // this one is to display the data of the response from the function on top to the ui
    // CLARISE if u change the structure of how the workout plan is returned, u need to change this
    const plansContainer = document.getElementById('plans-container');
    plansContainer.innerHTML = ''; 
    Object.keys(data).forEach(day => {
        const dayCard = document.createElement('div');
        dayCard.className = 'card my-3';
        let cardBodyContent = `<div class="card-header">${day}</div><ul class="list-group list-group-flush">`;
        data[day].forEach(activity => {
            cardBodyContent += `<li class="list-group-item">${activity.activity}`;
            if (activity.exercise) {
                cardBodyContent += `: ${activity.exercise}`;
            }
            if (activity.descrptn) {
                cardBodyContent += ` - ${activity.descrptn}`;  
            }
            if (activity.no_of_sets) {
                cardBodyContent += ` - ${activity.no_of_sets}`;
            }
            cardBodyContent += `</li>`;
        });
        cardBodyContent += '</ul>';
        dayCard.innerHTML = cardBodyContent;
        plansContainer.appendChild(dayCard);
    });
}

function fetchChallenges() {
    //fetch all available challenges and pass the response to the displaychallenges function below
    fetch(`http://127.0.0.1:5000/challenge`)
        .then(response => response.json())
        .then(data => {
            displayChallenges(data.data.challenges); 
        });
}

window.fetchChallenges = fetchChallenges;

function displayChallenges(challengesData) {
    // takes in the array of challanges from the prev function and displays them to the ui
    const challengesContainer = document.getElementById('challenge-container');
    challengesContainer.innerHTML = ''; 

    challengesData.forEach(challenge => {
        const challengeElement = document.createElement('div');
        challengeElement.className = 'card my-3';
        
        let cardBodyContent = `
            <div class="card-header">${challenge.title}</div>
            <div class="card-body">
                <h5 class="card-title">${challenge.description}</h5>
                <p class="card-text">Fitness Level: ${challenge.fitnessLevel}</p>
                <p class="card-text">Reps: ${challenge.reps}</p>
                <p class="card-text">Loyalty Points: ${challenge.loyaltyPoints}</p>
                <button class="btn btn-primary join-challenge-btn">Join Challenge</button>
                <input type="file" class="challenge-photo-upload" style="display: none;" accept="image/*">
                <button class="btn btn-success submit-photo-btn" style="display: none;">Submit Photo</button>
            </div>
        `;
        
        challengeElement.innerHTML = cardBodyContent;
        challengesContainer.appendChild(challengeElement);

        const joinChallengeBtn = challengeElement.querySelector('.join-challenge-btn');
        const fileInput = challengeElement.querySelector('.challenge-photo-upload');
        const submitPhotoBtn = challengeElement.querySelector('.submit-photo-btn');

        joinChallengeBtn.addEventListener('click', function() {
            // code so that when ppl click the join challenge button, the display styling for the upload pic and submit pic becomes visible
            fileInput.style.display = 'block';
            submitPhotoBtn.style.display = 'inline-block';
            joinChallengeBtn.style.display = 'none'; 
        });

        submitPhotoBtn.addEventListener('click', function() {
            //checks if got image selected and passes in the image into the uploadPhoto function below
            if (fileInput.files.length > 0) {
                const file = fileInput.files[0];
                const challengeTitle = `${challenge.title}`;
                const loyaltyPoints = `${challenge.loyaltyPoints}`;
                uploadPhoto(file, challengeTitle, loyaltyPoints, uid); 
                console.log("locked in:", file.name);
                // change back the select pic and submit pic to none so ppl cannot see aft they submit
                fileInput.style.display = 'none';
                submitPhotoBtn.style.display = 'none';
                joinChallengeBtn.style.display = 'inline-block';
            } else {
                alert('please select a picture');
            }
        });
    });
}


function uploadPhoto(file, challengeTitle, loyaltyPoints, uid) {
    const formData = new FormData();
    formData.append('image', file);
    formData.append('challengeTitle', challengeTitle);
    formData.append('loyaltyPoints', loyaltyPoints);
    formData.append('uid', uid);

    fetch('http://localhost:5012/processChallenge', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.hasOwnProperty('error')) {
            console.log('Error:', data);
            const errorMessage = "Error processing your submission. Please try submitting a better photo.";
            displayErrorMessage(challengeTitle, errorMessage);
        } else {
            console.log('Success:', data);
            const pointsAwarded = data.loyaltyPoints || loyaltyPoints;
            const successMessage = `Challenge successfully verified! You've earned ${pointsAwarded} loyalty points.`;
            displaySuccessMessage(challengeTitle, successMessage);
        }
    })
}

function clearMessages(challenge) {
    const errorMessageElement = challenge.querySelector('.error-message');
    if (errorMessageElement) {
        errorMessageElement.remove();
    }

    const successMessageElement = challenge.querySelector('.success-message');
    if (successMessageElement) {
        successMessageElement.remove();
    }
}


function displaySuccessMessage(challengeTitle, message) {
    const challenges = document.querySelectorAll('.card');
    challenges.forEach(challenge => {
        const title = challenge.querySelector('.card-header').textContent;
        if (title === challengeTitle) {
            clearMessages(challenge); 
            
            let successMessageElement = challenge.querySelector('.success-message');
            if (!successMessageElement) {
                successMessageElement = document.createElement('p');
                successMessageElement.className = 'success-message';
                challenge.querySelector('.card-body').appendChild(successMessageElement);
            }
            successMessageElement.style.color = 'green';
            successMessageElement.textContent = message;
            const joinChallengeBtn = challenge.querySelector('.join-challenge-btn');
            joinChallengeBtn.style.display = 'none';
            challenge.style.border = '2px solid green';
        }
    });
}

function displayErrorMessage(challengeTitle, message) {
    const challenges = document.querySelectorAll('.card');
    challenges.forEach(challenge => {
        const title = challenge.querySelector('.card-header').textContent;
        if (title === challengeTitle) {
            clearMessages(challenge); 
            
            let errorMessageElement = challenge.querySelector('.error-message');
            if (!errorMessageElement) {
                errorMessageElement = document.createElement('p');
                errorMessageElement.className = 'error-message';
                challenge.querySelector('.card-body').appendChild(errorMessageElement);
            }
            errorMessageElement.style.color = 'red';
            errorMessageElement.textContent = message;
            const joinChallengeBtn = challenge.querySelector('.join-challenge-btn');
            joinChallengeBtn.style.display = 'inline-block'; 
            challenge.style.border = '2px solid red';
        }
    });
}




function fetchProducts() {
    fetch(`http://127.0.0.1:5004/product`)
        .then(response => response.json())
        .then(data => {
            // console.log(data.data.products);
            displayProducts(data.data.products);
        });
}

window.fetchProducts = fetchProducts;

window.cart = []

function displayProducts(productData) {
    const productContainer = document.getElementById('product-container');
    productContainer.innerHTML = '';

    productData.forEach((product, index) => {
        const productElement = document.createElement('div');
        productElement.className = 'card my-3';
        
        let buttonContent = ''; // Initialize button content
    
        if (product.availability > 0) {
            // If product is available, set button content to "Add to Cart"
            buttonContent = `<button class="btn btn-primary add-cart-btn-${index}">Add to Cart</button>`;
        } else {
            // If product is sold out, set button content to "Sold Out"
            buttonContent = '<button class="btn btn-secondary" disabled>Sold Out</button>';
        }

        let cardBodyContent = `
        <div class="card-header">${product.title}</div>
        <div class="card-body">
            <img src="${product.image}" width='200' height='200'>
            <h5 class="card-title">${product.description}</h5>
            <p class="card-text">Price: ${product.price}</p>
            <p class="card-text">Quantity: ${product.availability}</p>
            <div class="input-group mb-3">
                <input type="number" class="form-control product-quantity-${index}" name="quantity" value="0" min="0" max="${product.availability}">
                ${buttonContent} <!-- Insert button content here -->
            </div>
        </div>
    `;

        productElement.innerHTML = cardBodyContent;
        productContainer.appendChild(productElement);

        // Add event listener to input field to restrict input to maximum quantity
        const quantityInput = document.querySelector(`.product-quantity-${index}`);
        quantityInput.addEventListener('input', () => {
            const enteredValue = parseInt(quantityInput.value);
            const maxQuantity = parseInt(quantityInput.getAttribute('max'));
            if (enteredValue > maxQuantity) {
                quantityInput.value = maxQuantity;
            }
        });

        // Add event listener to "Add to Cart" button
        if (product.availability > 0) {
            const addToCartButton = document.querySelector(`.add-cart-btn-${index}`);
            addToCartButton.addEventListener('click', () => {
                const quantity = document.querySelector(`.product-quantity-${index}`).value;
                if (parseInt(quantity) > 0) {
                    addToCart({ title: product.title, description: product.description, price: product.price, quantity, availability: product.availability, id: product.id });
                } else {
                    alert('Please enter a quantity greater than 0.');
                }
            });
        }
    });
}



function addToCart(product){
    // Check if a product with the same name and description already exists in the cart
    const existingProductIndex = cart.findIndex(item => item.title === product.title && item.description === product.description);

    // Convert the product quantity to a number
    const productQuantity = +product.quantity;

    if (existingProductIndex !== -1) {
        // If the product exists, update its quantity
        cart[existingProductIndex].quantity += productQuantity;
    } else {
        // If the product doesn't exist, add it to the cart
        cart.push({...product, quantity: productQuantity});
    }

    // Calculate total price for the product based on its quantity
    cart.forEach(item => {
        item.totalPrice = item.price * item.quantity;
    });
    updateCartCount();
    // After you add to cart, the availability in the database changes
    const new_availability = product.availability - product.quantity
    const productid = product.id
    // fetch(`http://127.0.0.1:5004/product/modify/${productid}/${new_availability}`, {
    //     method: 'PUT'
    // })
    //     .then(response => response.json())
    //     .then(data => {
    //         fetchProducts()
    //     });

}


function updateCartCount() {
    const cartCountElement = document.getElementById('cartCount');
    if (cartCountElement) {
        cartCountElement.textContent = cart.length; // Update the cart count text
    }
}


function displayCartItems() {
    const cartContainer = document.getElementById('cart');
    cartContainer.innerHTML = ''; // Clear the previous content

    if (cart.length === 0) {
        cartContainer.innerHTML = '<h1>Your cart is empty.</h1>';
        return;
    }

    const cartTable = document.createElement('table');
    cartTable.className = 'table table-bordered'; // Add Bootstrap table class for borders
    
    // Create table header row
    const headerRow = document.createElement('tr');
    headerRow.innerHTML = `
        <th>Item</th>
        <th>Description</th>
        <th>Quantity</th>
        <th>Price</th>
        <th>Total</th>
        <th>Action</th>
    `;
    cartTable.appendChild(headerRow);

// Populate cart items
    cart.forEach((product, index) => {
    const cartItemRow = document.createElement('tr');
    cartItemRow.innerHTML = `
        <td class="item-cell">${product.title}</td>
        <td class="description-cell">${product.description}</td>
        <td class="quantity-cell">
            <input type="number" class="form-control product-quantity" value="${product.quantity}" min="1" max="${product.availability}" data-index="${index}">
        </td>
        <td class="price-cell">$${product.price}</td>
        <td class="total-cell">$${product.price * product.quantity}</td>
        <td class="action-cell">
            <button class="btn btn-danger remove-item-btn" data-index="${index}">Remove</button>
        </td>
    `;
    cartTable.appendChild(cartItemRow);
});

    // Calculate total sum of items
    const totalSum = cart.reduce((sum, product) => sum + (product.price * product.quantity), 0);
    const maximum_total = totalSum * (15/100)
    var lpoints = 0;
    fetch(`http://127.0.0.1:5008/get_user_points/${uid}`)
    .then(response => response.json())
    .then(data => {
        lpoints = data;  // Update lpoints with the fetched data
        console.log(lpoints);

        // Now create footerRow2 here, inside the .then function
        const footerRow2 = document.createElement('tr');
        footerRow2.innerHTML = `
            <td colspan="4">Available Loyalty Points</td>
            <td>${lpoints}</td>
            <td></td> <!-- Leave an empty column for consistency -->
        `;
        cartTable.appendChild(footerRow2);

        // Now create footerRow2 here, inside the .then function
        const footerRow3 = document.createElement('tr');
        footerRow3.innerHTML = `
            <td colspan="4">Enter amount of points to redeem</td>
            <td><label for="pointsToUse" class="form-label">Loyalty Points to Use:</label>
            <input type="number" class="form-control" id="pointsToUse" min="0" max="${maximum_total}" value="0" oninput="calculateTotalAfterDiscount(${totalSum}, ${lpoints})"></td>
            <td></td> <!-- Leave an empty column for consistency -->
        `;
        cartTable.appendChild(footerRow3);

        const footerRow4 = document.createElement('tr');
        footerRow4.innerHTML = `
            <td colspan="4">Sub-Total</td>
            <td><span id='totalAmountAfterDiscount'></span></td>
            <td></td> <!-- Leave an empty column for consistency -->
            `;
        cartTable.appendChild(footerRow4);
    });

    

    // Create footer row for total sum
    const footerRow = document.createElement('tr');
    footerRow.innerHTML = `
        <td colspan="4">Sub-Total</td>
        <td>$${totalSum}</td>
        <td></td> <!-- Leave an empty column for consistency -->
    `;
    cartTable.appendChild(footerRow);


    // Create container for the table and checkout button
    const tableAndCheckoutContainer = document.createElement('div');
    tableAndCheckoutContainer.style.display = 'flex';
    tableAndCheckoutContainer.style.flexDirection = 'column'; // Stack items vertically
    tableAndCheckoutContainer.appendChild(cartTable);

    cartContainer.appendChild(tableAndCheckoutContainer);

    // Add checkout button
    const checkoutButton = document.createElement('button');
    checkoutButton.className = 'btn btn-primary mt-3 align-self-end'; // Bootstrap classes for margin top and alignment
    checkoutButton.textContent = 'Checkout';
    tableAndCheckoutContainer.appendChild(checkoutButton);

    // event listenre for checkot button
    checkoutButton.addEventListener('click', function() {
        console.log('points used:', document.getElementById('pointsToUse').value);
        var discountAmount = document.getElementById('pointsToUse').value;
        const formData = new FormData(); // so this u create a 'list'
        formData.append('discountAmount', discountAmount); // so u append this amount to the list
        formData.append('cart', JSON.stringify(cart)); // then u add the cart to the list
        fetch('http://localhost:5008/create_checkout_session', {
                method: 'POST',
                body: formData,

                })
                .then(function(response) {
                return response.text();
            })
            .then(function(sessionUrl) {
                window.location.href = sessionUrl;
            });

        //test
        fetch('http://localhost:5010/create_order', {
                method: 'POST',
                body: formData,

                })
                .then(function(response) {
                return response.text();
            })
            .then(function(sessionUrl) {
                window.location.href = sessionUrl;
            });
    
    });
    

    // Add event listeners to input fields for quantity
    const quantityInputs = document.querySelectorAll('.product-quantity');
    quantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            const index = parseInt(this.getAttribute('data-index'));
            const newQuantity = parseInt(this.value);
            updateCartItemQuantity(index, newQuantity);
        });
    });

// Add event listeners to remove buttons
const removeButtons = document.querySelectorAll('.remove-item-btn');
removeButtons.forEach(button => {
    button.addEventListener('click', function() {
        const index = parseInt(this.getAttribute('data-index'));
        const removedProduct = cart[index];
        removeCartItem(index);
        // fetch(`http://127.0.0.1:5004/product/modify/${removedProduct.id}/${removedProduct.availability}`, {
        //     method: 'PUT'
        // })
        // .then(response => response.json())
        // .then(data => {
        //     // Handle response if needed
        // })
        // .catch(error => {
        //     console.error('Error updating quantity in the database:', error);
        // });
    });
});
}


function calculateTotalAfterDiscount(total, points) {
    const pointsToUseInput = document.getElementById('pointsToUse');
    let max_total = total * 15; // Calculate the maximum total

    if (points < max_total) {
        pointsToUseInput.max = parseInt(points); // Set the max attribute of the input to points
    } else {
        pointsToUseInput.max = parseInt(max_total); // Set the max attribute of the input to max_total
    }

    const pointsToUse = parseInt(pointsToUseInput.value); // Get the current input value

    if (pointsToUse > pointsToUseInput.max) {
        pointsToUseInput.value = parseInt(pointsToUseInput.max); // Reset value to maximum allowed if it's greater
    }



    const totalAmountBeforeDiscount = total;
    const discount = pointsToUseInput.value * 0.01; // 1 point = 1 cent
    const totalAmountAfterDiscount = Math.max(totalAmountBeforeDiscount - discount, 0);
    document.getElementById('totalAmountAfterDiscount').textContent = totalAmountAfterDiscount.toFixed(2);
}


window.calculateTotalAfterDiscount = calculateTotalAfterDiscount;



function updateCartItemQuantity(index, newQuantity) {
    if (newQuantity < 1) {
        // If the new quantity is less than 1, set it to 1
        newQuantity = 1;
    } else if (newQuantity > cart[index].availability) {
        // If the new quantity exceeds the availability, set it to the availability
        newQuantity = cart[index].availability;
    }
    cart[index].quantity = newQuantity;
    displayCartItems(); // Re-display the cart items after updating the quantity
}

function removeCartItem(index) {
    cart.splice(index, 1);
    updateCartCount(); // Update the cart count after removing the item
    displayCartItems(); // Re-display the cart items after removing the item
}


function displayCartOnTabActivation() {
    const cartTab = document.querySelector('a[href="#cart"]'); // Get the cart tab link
    cartTab.addEventListener('shown.bs.tab', function (event) { // Add event listener for tab shown event
        displayCartItems(cart); // Call displayCartItems function with the cart data
    });
}

displayCartOnTabActivation();