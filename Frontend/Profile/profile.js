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
							        <button class="form__button" type="submit">Edit Details</button>
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
