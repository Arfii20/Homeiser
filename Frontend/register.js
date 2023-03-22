const BASE = "http://127.0.0.1:5000/";
const logged_in_hrefs = document.querySelector(".if-logged-in");
const not_logged_in_hrefs = document.querySelector(".if-not-logged-in");
const hamburger = document.querySelector(".hamburger");

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

// const user_id = getCookie("user_id");
// const house_id = getCookie("household_id");
const user_id = 630;
const house_id = 620;
let prev_values = {};

if (user_id === null || user_id === undefined) {
  not_logged_in_hrefs.style.display = "";
  logged_in_hrefs.style.display = "none";
  hamburger.style.display = "none";
  window.location.href = "./login.html";
}
if (house_id === null || house_id === undefined) {
  window.location.href = "./group";
}

not_logged_in_hrefs.style.display = "none";
logged_in_hrefs.style.display = "";
hamburger.style.display = "";



function setFormMessage(formElement, type, message) {
    const messageElement = formElement.querySelector(".form__message");

    messageElement.textContent = message;
    messageElement.classList.remove("form__message-success", "form__message--error");
    messageElement.classList.add(`form__message--${type}`);
}

function setInputError(inputElement, message) {
    inputElement.classList.add("form__input--error");
    inputElement.parentElement.querySelector(".form__input-error-message").textContent = message;
}

function clearInputError(inputElement) {
    inputElement.classList.remove("form__input--error");
    inputElement.parentElement.querySelector(".form__input-error-message").textContent = "";
}

function isValidEmail(email) {
    // const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const emailRegex = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return emailRegex.test(email);
}

document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.querySelector("#login");
    const createAccountForm = document.querySelector("#createAccount");

    loginForm.addEventListener("submit", e => {
        e.preventDefault();

        //Perform your AJAX/Fetch login

        setFormMessage(loginForm, "error", "Invalid username/password combination");
    });

    document.querySelectorAll(".form__input").forEach(inputElement => {
        inputElement.addEventListener("blur", e => {
            if (e.target.id === "signupUsername" && e.target.value.length > 0 && e.target.value.length < 10) {
                setInputError(inputElement, "Username must be at least 10 characters in length");
            }
        });

        inputElement.addEventListener("input", e => {
            clearInputError(inputElement);
        });
    });
});


document.querySelectorAll(".form__input").forEach(inputElement => {
    inputElement.addEventListener("blur", e => {
        if (e.target.id === "signupEmail" && !isValidEmail(e.target.value)) {
            setInputError(inputElement, "Wrong email address");
        }
    });

    inputElement.addEventListener("input", e => {
        clearInputError(inputElement);
    });
});

document.querySelectorAll(".form__input").forEach(inputElement => {
    inputElement.addEventListener("blur", e => {
        if (e.target.id === "signupPassword2" && e.target.value !== document.querySelector("#signupPassword1").value) {
            setInputError(inputElement, "Incorrect password");
        }
    });

    inputElement.addEventListener("input", e => {
        clearInputError(inputElement);
    });
});



//
async function postRegister(event){
	event.preventDefault();
    console.log("sis");
	const button = event.target;

	const form = button.closest('form');
	const register_FnameElement = form.querySelector('input[placeholder*="First Name"]');
	const register_LnameElement = form.querySelector('input[placeholder*="Last Name"]');
	const register_EmailElement = form.querySelector('input[placeholder*="Email Address"]');
	const register_PasswordElement = form.querySelector('input[placeholder*="Password"]');
	const register_ConfirmElement = form.querySelector('input[placeholder*="Confirm Password"]');
	const register_BirthElement = form.querySelector('input[placeholder*="Date of Birth"]');
// console.log(register_BirthElement);
	// const register_FnameID = 0;
	// const register_LnameID = 0;
	const register_Fname = register_FnameElement.value;
	const register_Lname = register_LnameElement.value;
	const register_Email = register_PasswordElement.value;
    const register_Password = register_PasswordElement.value;
	const register_Confirm = register_ConfirmElement.value;
	const register_Birth = register_BirthElement.value;

	console.log(register_Birth);
	// const register_Paid = "false";
	// const register_HouseId = house_id;

	if (register_Fname === "") {
		setInputError(register_FnameElement, 'Please enter First Name');
		return;
	}
	else{
		clearInputError(register_FnameElement);
	}

	
	if (register_Lname === "") {
		setInputError(register_LnameElement, 'Please enter Last Name');
		return;
	}
	else{
		clearInputError(register_Lname);
	}


	if (register_Birth === "") {
		setInputError(register_BirthElement, 'Please enter birthday');
		return;
	}
	else if (!isValidDate(register_Birth)){
		setInputError(register_BirthElement, "Date must be valid and in yyyy-mm-dd format");
		return;
	}
	else{
		clearInputError(register_BirthElement);
	}


	if (register_Email === "") {
		setInputError(register_EmailElement, 'Please enter Email');
		return;
	}
	else if (!isValidEmail(register_Email)) {
		setInputError(register_EmailElement, 'The email address is invalid');
		return;
	}
	else{
		clearInputError(register_EmailElement);
	}


	if (register_Password === "") {
		setInputError(register_PasswordElement, 'Please enter password');
		return;
	}
	else{
		clearInputError(register_PasswordElement);
	}


	if (register_Confirm !== register_Password) {
		setInputError(register_ConfirmElement, 'Passwords don\'t match');
		return;
	}
	else{
		clearInputError(register_ConfirmElement);
	}



	fetch(BASE + "register", {
	  	method: 'POST',
	  	headers: {
	    	'Content-Type': 'application/json'
	  	},
	  	body: JSON.stringify({
			user_id: null,
	    	first_name: register_Fname,
	    	surname: register_Lname,
			email: register_Email,
			password: register_Password,
			dob: register_Birth,
	    	// confirm: register_Confirm,
			household_id: null,
			color: null,
	  	})
	})
	.then(response => {
	  	if (response.ok) {
	    	console.log({message: "Registration successful"});
			ContinueButton.innerText = "Register";
			getLedgerResources(user_id);
	  	} else {
	    	throw new Error('Request failed.');
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

function isValidDate(register_Birth) {
	const regex = /^\d{4}-\d{2}-\d{2}$/;
	if (!regex.test(register_Birth)) {
		return false;
	}
	const date = new Date(register_Birth);
	if (isValidDate(date.getTime())) {
		return false;
	}
	return true;
}



function isValidEmail(register_Email) {
	const regee = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
	if (!regee.test(register_Email)) {
		return false;
	}
	const date = new Date(register_Email);
	if (isValidEmail(date.getEmail())) {
		return false;
	}
	return true;
}

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