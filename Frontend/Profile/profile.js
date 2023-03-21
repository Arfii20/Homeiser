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
							            <input type="text" id="first_name" class="form__input" autofocus placeholder="First name: ${obj.first_name}" readonly>
							            <div class="form__input-error-message"></div>
							        </div>
							        <div class="form__input-group">
							            <input type="text" id="surname" class="form__input" autofocus placeholder="Last name: ${obj.surname}" readonly>
							            <div class="form__input-error-message"></div>
							        </div>
							        <div class="form__input-group">
							            <input type="text" id="email" class="form__input" autofocus placeholder="Email address: ${obj.email}" readonly>
							            <div class="form__input-error-message"></div>
							        </div>
							        <div class="form__input-group">
							            <input type="text" id="date_of_birth" class="form__input" autofocus placeholder="Date of Birth: ${obj.date_of_birth}" readonly>
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
	const button = event.target;

	const form = button.closest('form');
	const profile_FnameElement = form.querySelector('input[placeholder*="First Name"]');
	const profile_LnameElement = form.querySelector('input[placeholder*="Last Name"]');
	const profile_EmailElement = form.querySelector('input[placeholder*="Email address"]');
	const profile_BirthElement = form.querySelector('input[placeholder*="Date of Birth"]');

	const profile_Fname = profile_FnameElement.value;
	const profile_Lname = profile_LnameElement.value;
	const profile_Email = profile_PasswordElement.value;
	const profile_Birth = profile_BirthElement.value;

	console.log(profile_Birth);
	// const profile_Paid = "false";
	// const profile_HouseId = house_id;

	if (profile_Fname === "") {
		setInputError(profile_FnameElement, 'Please enter First Name');
		return;
	}
	else{
		clearInputError(profile_FnameElement);
	}

	
	if (profile_Lname === "") {
		setInputError(profile_LnameElement, 'Please enter Last Name');
		return;
	}
	else{
		clearInputError(profile_Lname);
	}


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


	if (profile_Password === "") {
		setInputError(profile_PasswordElement, 'Please enter password');
		return;
	}
	else{
		clearInputError(profile_PasswordElement);
	}


	if (profile_Confirm !== profile_Password) {
		setInputError(profile_ConfirmElement, 'Passwords don\'t match');
		return;
	}
	else{
		clearInputError(profile_ConfirmElement);
	}



	fetch(BASE + "profile", {
	  	method: 'POST',
	  	headers: {
	    	'Content-Type': 'application/json'
	  	},
	  	body: JSON.stringify({
			user_id: null,
	    	first_name: profile_Fname,
	    	surname: profile_Lname,
			email: profile_Email,
			password: profile_Password,
			dob: profile_Birth,
	    	// confirm: profile_Confirm,
			household_id: null,
			color: null,
	  	})
	})
	.then(response => {
	  	if (response.ok) {
	    	console.log({message: "Registration successful"});
			ContinueButton.innerText = "profile";
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



function createMockUpHTMLofProfile(){
	container.innerHTML = `<form class="form" id="createAccount">
							        <h1 class="form__title">Your Details</h1>
							        <div class="form__message form__message--error"></div>
							        <div class="form__input-group">
							            <input type="text" id="first_name" class="form__input" autofocus placeholder="First name: Mock First Name" readonly>
							            <div class="form__input-error-message"></div>
							        </div>
							        <div class="form__input-group">
							            <input type="text" id="surname" class="form__input" autofocus placeholder="Last name: Mock Surame" readonly>
							            <div class="form__input-error-message"></div>
							        </div>
							        <div class="form__input-group">
							            <input type="text" id="email" class="form__input" autofocus placeholder="Email address: mock.email@gmail.com" readonly>
							            <div class="form__input-error-message"></div>
							        </div>
							        <div class="form__input-group">
							            <input type="text" id="date_of_birth" class="form__input" autofocus placeholder="Date of Birth: 2000-03-22" readonly>
							            <div class="form__input-error-message"></div>
							        </div>
							        <button class="form__button" type="submit">Edit Details</button>
							    </form>`;
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
