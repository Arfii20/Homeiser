const BASE = "http://127.0.0.1:5000/";
const logged_in_hrefs = document.querySelector(".if-logged-in");
const not_logged_in_hrefs = document.querySelector(".if-not-logged-in");
const hamburger = document.querySelector(".hamburger");

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

    if (login_Password === "") {
        setInputError(login_PasswordElement, 'Please enter password');
        return;
    }
    else{
    	clearInputError(login_PasswordElement);
    }

	const response = await fetch(BASE + "login", {
											  	method: 'POST',
											  	headers: {
											    	'Content-Type': 'application/json'
											  	},
											  	body: JSON.stringify({
											  		email: login_Email,
											    	password: login_Password
											  	})
											})

  	if (response.ok) {
    	console.log({message: "Login successful"});
    	const obj = await JSON.parse(await response.json());

    	await setLocalStorage(obj.user_id, obj.household_id, obj.email);
    	alert("Login Successful.");
    	window.location.href = "./welcome.html";
    }
	else {
		setInputError(login_PasswordElement, 'Incorrect Email or Password');
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

function isValidEmail(login_Email) {
    const email = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return email.test(login_Email);
}

function setLocalStorage(user_id, house_id, email_id) {
  localStorage.setItem("user_id", user_id);
  localStorage.setItem("house_id", house_id);
  localStorage.setItem("email_id", email_id);
}

function logout(){
	// Get all cookies and split them into an array
	localStorage.clear();
  
	console.log("Local Storage cleared");
	window.location.href = "login.html";
}
