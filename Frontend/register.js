const BASE = "http://127.0.0.1:5000/";
const logged_in_hrefs = document.querySelector(".if-logged-in");
const not_logged_in_hrefs = document.querySelector(".if-not-logged-in");
const hamburger = document.querySelector(".hamburger");

not_logged_in_hrefs.style.display = "";
logged_in_hrefs.style.display = "none";
hamburger.style.display = "none";

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
    const emailRegex = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return emailRegex.test(email);
}

async function postRegister(event){
	event.preventDefault();
	const button = event.target;

	const form = button.closest('form');
	const register_FnameElement = form.querySelector('input[placeholder*="First Name"]');
	const register_LnameElement = form.querySelector('input[placeholder*="Last Name"]');
	const register_BirthElement = form.querySelector('input[placeholder*="Date of Birth"]');	
	const register_EmailElement = form.querySelector('input[placeholder*="Email Address"]');
	const register_PasswordElement = form.querySelector('input[placeholder*="Password"]');
	const register_ConfirmElement = form.querySelector('input[placeholder*="Confirm Password"]');

	const register_Fname = register_FnameElement.value;
	const register_Lname = register_LnameElement.value;
	const register_Birth = register_BirthElement.value;	
	const register_Email = register_EmailElement.value;
    const register_Password = register_PasswordElement.value;
	const register_Confirm = register_ConfirmElement.value;


	console.log(register_Email);

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
		clearInputError(register_LnameElement);
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
		setInputError(register_EmailElement, 'Please enter email');
		return;
	}
	else if (!isValidEmail(register_Email)) {
		setInputError(register_EmailElement, 'The Email address is invalid');
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

	const response = await fetch(BASE + "user", {
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
														household_id: null,
														colour: null,
												  	})
												})
  	if (response.ok) {
    	console.log({message: "Registration successful"});
    	const obj = await JSON.parse(await response.json());

    	setCookies(obj.u_id, obj.household, obj.email);
    	window.location.href = "./welcome.html";
  	} else {
    	throw new Error('Request failed.');
  	}
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

function isValidDate(date_in) {
	const regex = /^(?:(?:19|20)[0-9]{2})-(?:(?:0[1-9])|(?:1[0-2]))-(?:(?:0[1-9])|(?:[1-2][0-9])|(?:3[0-1]))$/;
	if (!regex.test(date_in)) {
		return false;
	}
	const date = new Date(date_in);
	if (isValidDate(date.getTime())) {
		return false;
	}
	return true;
}

function isValidEmail(login_Email) {
    const email = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return email.test(login_Email);
}

function setCookies(user_id, house_id, email_id) {
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
	document.cookie = "user_id=" + user_id + "; expires=" + expires + "; path=" + path;
	document.cookie = "house_id=" + house_id + "; expires=" + expires + "; path=" + path;
	document.cookie = "email_id=" + email_id + "; expires=" + expires + "; path=" + path;
}

function logout(){
	// Get all cookies and split them into an array
	localStorage.clear();
  
	console.log("Local Storage cleared");
	window.location.href = "login.html";
}