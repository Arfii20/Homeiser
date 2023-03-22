const BASE = "http://127.0.0.1:5000/";
const logged_in_hrefs = document.querySelector(".if-logged-in");
const not_logged_in_hrefs = document.querySelector(".if-not-logged-in");
const hamburger = document.querySelector(".hamburger");

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

not_logged_in_hrefs.style.display = "";
logged_in_hrefs.style.display = "none";
hamburger.style.display = "none";

async function postLogin(event){
	event.preventDefault();
    // console.log("sis");
	const button = event.target;

	const form = button.closest('form');
	const login_EmailElement = form.querySelector('input[placeholder*="Email Address"]');
	const login_PasswordElement = form.querySelector('input[placeholder*="Password"]');



	const login_Email = login_EmailElement.value;
    const login_Password = login_PasswordElement.value;



	if (login_Email === "") {
		setInputError(login_EmailElement, 'Please enter email');
		return;
	}
	else if (!isValidEmail(login_Email)) {
		setInputError(login_EmailElement, 'The Email address is invalid');
		return;
	}
	else{
		clearInputError(login_EmailElement);
	}


	// if (login_Password === "") {
	// 	setInputError(login_PasswordElement, 'Please enter password');
	// 	return;
	// }
	// else if (!isValidDate(login_Password)){
	// 	setInputError(login_PasswordElement, "The password is invalid");
	// 	return;
	// }
	// else{
	// 	clearInputError(login_PasswordElement);
	// }


    if (login_Password === "") {
        setInputError(login_PasswordElement, 'Please enter password');
        return;
    }
    clearInputError(login_PasswordElement);
    


	fetch(BASE + "login", {
	  	method: 'POST',
	  	headers: {
	    	'Content-Type': 'application/json'
	  	},
	  	body: JSON.stringify({

	  	})
	})
	.then(response => {
	  	if (response.ok) {
	    	console.log({message: "Login successful"});
			// rightContainer.innerHTML = "";
			// rightContainer.style.display = "none";
			// ContinueButton.innerText = "login";
			getLedgerResources(user_id);
	  	} else {
	    	throw new Error('Login failed.');
	  	}
	})
	.then(data => {
	  	console.log(data);
	})
	.catch(error => {
	  	console.log(error);
	});
}


function setInputError(inputElement, errorMessage, inputGroupSelector = '.form__input-group') {
	const inputGroupElement = inputElement.closest(inputGroupSelector);
	const errorElement = inputGroupElement.querySelector('.form__input-error-message');
	inputGroupElement.classList.add('form__input-group--error');
	errorElement.innerText = errorMessage;
}

function clearInputError(inputElement, inputGroupSelector = '.form__input-group') {
	const inputGroupElement = inputElement.closest(inputGroupSelector);
	const errorElement = inputGroupElement.querySelector('.form__input-error-message');
	inputGroupElement.classList.remove('form__input-group--error');
	errorElement.innerText = '';
}

function isValidEmail(login_Email) {
    const email = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return email.test(login_Email);
}


// Get the current date
const currentDate = new Date();

// Add one day to the current date
const tomorrowDate = new Date(currentDate);
tomorrowDate.setDate(currentDate.getDate() + 2);

// Set the time to 12:00:00
tomorrowDate.setHours(12);
tomorrowDate.setMinutes(0);
tomorrowDate.setSeconds(0);
tomorrowDate.setMilliseconds(0);

// Convert the date to a UTC string
const expires = tomorrowDate.toUTCString();

// Set the path of the cookie
const path = "/"; 

// Set the cookie with a name, value, expiration date, and path
document.cookie = "userID=SomeValue; expires=" + expires + "; path=" + path;


function logout(){
	// Get all cookies and split them into an array
	const cookies = document.cookie.split(";");
  
	// Loop through all cookies and delete them by setting their expiration date to a date in the past
	for (let i = 0; i < cookies.length; i++) {
	  const cookie = cookies[i];
	  const eqPos = cookie.indexOf("=");
	  const name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
	  document.cookie = name + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
	}
  
	console.log("Cookies cleared");
  
	window.location.href = "login.html";
}