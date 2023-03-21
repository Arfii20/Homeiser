const BASE = "http://127.0.0.1:5000/";
const container = document.querySelector(".container");
const logged_in_hrefs = document.querySelector(".if-logged-in");
const not_logged_in_hrefs = document.querySelector(".if-not-logged-in");

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

// const user_id = getCookie("user_id");
// const house_id = getCookie("household_id");
const user_id = 630;
const house_id = 620;

if (user_id === null || user_id === undefined) {
  not_logged_in_hrefs.style.display = "";
  logged_in_hrefs.style.display = "none";
  window.location.href = "../login.html";
}
if (house_id === null || house_id === undefined) {
  window.location.href = "../group";
}

not_logged_in_hrefs.style.display = "none";
logged_in_hrefs.style.display = "";
getDetails(user_id);

async function getDetails(user_id){

	try{
		const response = await fetch(BASE + "user_profile/" + user_id);
		
		if (response.ok) {
			console.log({message: "Profile Received"});
			const obj = await response.json();
			container.innerHTML = `<form class="form" id="createAccount">
							        <h1 class="form__title">Your Details</h1>
							        <div class="form__message form__message--error"></div>
							        <div class="form__input-group">
							            <input type="text" id="first_name" class="form__input" placeholder="First Name: ${obj.first_name}" readonly>
							            <div class="form__input-error-message"></div>
							        </div>
							        <div class="form__input-group">
							            <input type="text" id="surname" class="form__input" placeholder="Last Name: ${obj.surname}" readonly>
							            <div class="form__input-error-message"></div>
							        </div>
							        <div class="form__input-group">
							            <input type="text" id="email" class="form__input" placeholder="Email Address: ${obj.email}" readonly>
							            <div class="form__input-error-message"></div>
							        </div>
							        <div class="form__input-group">
							            <input type="text" id="date_of_birth" class="form__input" placeholder="Date of Birth: ${obj.date_of_birth}" readonly>
							            <div class="form__input-error-message"></div>
							        </div>
							        <button class="form__button" type="submit" onclick=postDetails(event)>Edit Details</button>
							    </form>`;
		}
		else {
	    	throw new Error('Error retrieving ledger.');
	    	return;
		}
	}
	catch (error) {
    console.error(error);
    if (error.message === 'Failed to fetch') {
        createMockUpHTMLofProfile();
    }
  }
}

async function postDetails(event){
	event.preventDefault();
	const form = event.target.closest('form');
	const profile_FnameElement = form.querySelector('input[placeholder*="First Name"]');
	const profile_LnameElement = form.querySelector('input[placeholder*="Last Name"]');
	const profile_EmailElement = form.querySelector('input[placeholder*="Email Address"]');
	const profile_BirthElement = form.querySelector('input[placeholder*="Date of Birth"]');
	const profile_passwordElement = form.querySelector('input[placeholder*="Enter Password"]');
	const profile_confirmPasswordElement = form.querySelector('input[placeholder*="Confirm Password"]');

	if (event.target.innerText === "Edit Details"){
		container.innerHTML = `<form class="form" id="createAccount">
				        <h1 class="form__title">Your Details</h1>
				        <div class="form__message form__message--error"></div>
				        <div class="form__input-group">
				            <input type="text" id="first_name" class="form__input" autofocus placeholder="First Name: ">
				            <div class="form__input-error-message"></div>
				        </div>
				        <div class="form__input-group">
				            <input type="text" id="surname" class="form__input" autofocus placeholder="Last Name: ">
				            <div class="form__input-error-message"></div>
				        </div>
				        <div class="form__input-group">
				            <input type="text" id="email" class="form__input" autofocus placeholder="Email Address: ">
				            <div class="form__input-error-message"></div>
				        </div>
				        <div class="form__input-group">
							<input type="text" id="date_of_birth" class="form__input" autofocus placeholder="Date of Birth: ">
							<div class="form__input-error-message"></div>
						</div>
						<div class="form__input-group">
				            <input type="password" id="password" class="form__input" autofocus placeholder="Enter Password: ">
				            <div class="form__input-error-message"></div>
				        </div>
				        <div class="form__input-group">
				            <input type="password" id="confirm_password" class="form__input" autofocus placeholder="Confirm Password: ">
				            <div class="form__input-error-message"></div>
				        </div>
				        <button class="form__button" type="submit" onclick=postDetails(event)>Save</button>
				        <button class="form__button" type="submit" style="margin-top:0.8rem">Cancel</button>
				    </form>`;

		profile_FnameElement.removeAttribute("readonly", "readonly");
	    profile_LnameElement.removeAttribute("readonly", "readonly");
	    profile_EmailElement.removeAttribute("readonly", "readonly");
	    profile_BirthElement.removeAttribute("readonly", "readonly");
	   	profile_FnameElement.focus();
	}
	
	else{
		const profile_Fname = profile_FnameElement.value;
		const profile_Lname = profile_LnameElement.value;
		const profile_Email = profile_EmailElement.value;
		const profile_Birth = profile_BirthElement.value;
		const profile_password = profile_passwordElement.value;
		const profile_confirmPassword = profile_confirmPasswordElement.value;

		// Validating first name
		if (profile_Fname === "") {
			setInputError(profile_FnameElement, 'Please enter First Name');
			return;
		}
		else{
			clearInputError(profile_FnameElement);
		}

		// Validating last name
		if (profile_Lname === "") {
			setInputError(profile_LnameElement, 'Please enter Last Name');
			return;
		}
		else{
			clearInputError(profile_LnameElement);
		}

		// Validating email
		if (profile_Email === "") {
			setInputError(profile_EmailElement, 'Please enter Email');
			return;
		}
		else if (!isValidEmail(profile_Email)) {
			setInputError(profile_EmailElement, 'The email address is invalid');
			return;
		}
		else{
			clearInputError(profile_EmailElement);
		}
		// Validating dob
		if (profile_Birth === "") {
			setInputError(profile_BirthElement, 'Please enter birthday');
			return;
		}
		else if (!isValidDate(profile_Birth)){
			setInputError(profile_BirthElement, "Date must be valid and in yyyy-mm-dd format");
			return;
		}
		else{
			clearInputError(profile_BirthElement);
		}

		if (profile_password === "") {
			setInputError(profile_passwordElement, 'Please enter password');
		return;
		}
		else{
			clearInputError(profile_passwordElement);
		}

		if (profile_confirmPassword !== profile_password) {
			setInputError(profile_confirmPasswordElement, 'Passwords don\'t match');
			return;
		}
		else{
			clearInputError(profile_confirmPasswordElement);
		}

		const url = BASE + "user_profile/" + user_id;
	    const data_confirm = new URLSearchParams();

		data_confirm.append('password', profile_password);
	    const response_confirm = await fetch(url, {
	                    method: 'PATCH',
	                    body: data_confirm,
	                    headers: {
	                      'Content-Type': 'application/x-www-form-urlencoded'
	                    }
	                  });

	    if (!response_confirm.ok){
			setInputError(profile_passwordElement, 'Incorrect Password');
			return;
		}
		else{
			clearInputError(profile_passwordElement);
		}

	    const data = new URLSearchParams();
	    data.append('first_name', profile_Fname.replace(/'/g, "\\'"));
	    data.append('surname', profile_Lname.replace(/'/g, "\\'"));
	    data.append('email', profile_Email.replace(/'/g, "\\'"));
	    data.append('date_of_birth', profile_Birth.replace(/'/g, "\\'"));

	    const response = await fetch(url, {
	                    method: 'POST',
	                    body: data,
	                    headers: {
	                      'Content-Type': 'application/x-www-form-urlencoded'
	                    }
	                  });

	    if (response.ok){
			event.target.innerText = "Edit Details";

			profile_FnameElement.setAttribute("readonly", "readonly");
			profile_LnameElement.setAttribute("readonly", "readonly");
			profile_EmailElement.setAttribute("readonly", "readonly");
			profile_BirthElement.setAttribute("readonly", "readonly");

			profile_passwordElement.remove();
			profile_confirmPasswordElement.remove();

			profile_FnameElement.setAttribute("placeholder", "First Name: " + profile_FnameElement.value);
			profile_LnameElement.setAttribute("placeholder", "Last Name: " + profile_LnameElement.value);
			profile_EmailElement.setAttribute("placeholder", "Email Address: " + profile_EmailElement.value);
			profile_BirthElement.setAttribute("placeholder", "Date of Birth: " + profile_BirthElement.value);

			profile_FnameElement.value = "";
			profile_LnameElement.value = "";
			profile_EmailElement.value = "";
			profile_BirthElement.value = "";
	    }
	    console.log(await response.json())
	}
}

function createMockUpHTMLofProfile(){
	container.innerHTML = `<form class="form" id="createAccount">
							        <h1 class="form__title">Your Details</h1>
							        <div class="form__message form__message--error"></div>
							        <div class="form__input-group">
							            <input type="text" id="first_name" class="form__input" autofocus placeholder="First Name: Mock First Name" readonly>
							            <div class="form__input-error-message"></div>
							        </div>
							        <div class="form__input-group">
							            <input type="text" id="surname" class="form__input" autofocus placeholder="Last Name: Mock Surame" readonly>
							            <div class="form__input-error-message"></div>
							        </div>
							        <div class="form__input-group">
							            <input type="text" id="email" class="form__input" autofocus placeholder="Email Address: mock.email@gmail.com" readonly>
							            <div class="form__input-error-message"></div>
							        </div>
							        <div class="form__input-group">
							            <input type="text" id="date_of_birth" class="form__input" autofocus placeholder="Date of Birth: 2000-03-22" readonly>
							            <div class="form__input-error-message"></div>
							        </div>
							        <button class="form__button">Edit Details</button>
							    </form>`;
}

function isValidDate(register_Birth) {
	const regex = /^(?:(?:19|20)[0-9]{2})-(?:(?:0[1-9])|(?:1[0-2]))-(?:(?:0[1-9])|(?:[1-2][0-9])|(?:3[0-1]))$/;
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
	const regex = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
	if (!regex.test(register_Email)) {
		return false;
	}
	return true;
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

  window.location.href = "../login.html";
}
