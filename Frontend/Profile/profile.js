const BASE = "http://127.0.0.1:5000/";
const container = document.querySelector(".container");
const logged_in_hrefs = document.querySelector(".if-logged-in");
const not_logged_in_hrefs = document.querySelector(".if-not-logged-in");
const hamburger = document.querySelector(".hamburger");

const user_id = localStorage.getItem("user_id");
const house_id = localStorage.getItem("house_id");
// const user_id = 630;
// const house_id = 620;
let prev_values = {};

if (user_id === null || user_id === undefined) {
  not_logged_in_hrefs.style.display = "";
  logged_in_hrefs.style.display = "none";
  hamburger.style.display = "none";
  window.location.href = "../login.html";
}

not_logged_in_hrefs.style.display = "none";
logged_in_hrefs.style.display = "";
hamburger.style.display = "";

getDetails();

async function getDetails(){

	try{
		const response = await fetch(BASE + "user_profile/" + user_id);
		
		if (response.ok) {
			console.log({message: "Profile Received"});
			const obj = await response.json();
			container.innerHTML = `<form class="form">
							        <h1 class="form__title" style="color:#a220a4;">Your Details</h1>
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
	const cancel_button = document.querySelector(".rem_button");

	if (event.target.innerText === "Edit Details"){
		prev_values.first_name = profile_FnameElement.placeholder.split(": ")[1].trim();
		prev_values.surname = profile_LnameElement.placeholder.split(": ")[1].trim();
		prev_values.email = profile_EmailElement.placeholder.split(": ")[1].trim();
		prev_values.birth = profile_BirthElement.placeholder.split(": ")[1].trim();

		container.innerHTML = `<form class="form" id="createAccount">
				        <h1 class="form__title" style="color:#a220a4;">Update Your Details</h1>
				        <h6 class="form__title" style="margin-top:-30px">Leave it blank if you don't want to change that field</h6>
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
				        <button class="form__button rem_button" type="submit" style="margin-top:0.8rem">Cancel</button>
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
		if (profile_Fname != "") {
			prev_values.first_name = profile_Fname;
		}

		// Validating last name
		if (profile_Lname != "") {
			prev_values.surname = profile_Lname;
		}

		// Validating email
		if (profile_Email != "" && isValidEmail(profile_Email)) {
			prev_values.email = profile_Email;
		}
		else if (profile_Email != "" && !isValidEmail(profile_Email)) {
			setInputError(profile_EmailElement, 'The email address is invalid');
			return;
		}
		else{
			clearInputError(profile_EmailElement);
		}

		// Validating dob
		if (profile_Birth != "" && isValidDate(profile_Birth)) {
			prev_values.birth = profile_Birth;
		}
		else if (profile_Birth != "" && !isValidDate(profile_Birth)){
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
	    data.append('first_name', prev_values.first_name.replace(/'/g, "\\'"));
	    data.append('surname', prev_values.surname.replace(/'/g, "\\'"));
	    data.append('email', prev_values.email.replace(/'/g, "\\'"));
	    data.append('date_of_birth', prev_values.birth.replace(/'/g, "\\'"));

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
			cancel_button.remove();

			form.querySelector(".form__title").innerText = "Your Details";

			profile_FnameElement.setAttribute("placeholder", "First Name: " + prev_values.first_name);
			profile_LnameElement.setAttribute("placeholder", "Last Name: " + prev_values.surname);
			profile_EmailElement.setAttribute("placeholder", "Email Address: " + prev_values.email);
			profile_BirthElement.setAttribute("placeholder", "Date of Birth: " + prev_values.birth);

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
							        <h1 class="form__title" style="color:#a220a4;">Your Details</h1>
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
							        <button class="form__button" onclick=createMockUpHTMLofEditProfile()>Edit Details</button>
							    </form>`;
}

function createMockUpHTMLofEditProfile(){
	container.innerHTML = `<form class="form" id="createAccount">
				        <h1 class="form__title" style="color:#a220a4;">Update Your Details</h1>
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
				        <button class="form__button" type="submit">Save</button>
				        <button class="form__button" type="submit" style="margin-top:0.8rem">Cancel</button>
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
	localStorage.clear();
  
	console.log("Local Storage cleared");
	window.location.href = "login.html";
}
