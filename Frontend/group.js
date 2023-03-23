const BASE = "http://127.0.0.1:5000/";
const logged_in_hrefs = document.querySelector(".if-logged-in");
const not_logged_in_hrefs = document.querySelector(".if-not-logged-in");
const hamburger = document.querySelector(".hamburger");

const user_id = localStorage.getItem("user_id");
const house_id = localStorage.getItem("house_id");
const email_id = localStorage.getItem("email_id");
// const user_id = 630;
// const house_id = 620;

if (user_id === null || user_id === undefined || user_id === "undefined" || user_id === "null") {
  not_logged_in_hrefs.style.display = "";
  logged_in_hrefs.style.display = "none";
  hamburger.style.display = "none";
  window.location.href = "./login.html";
}
else{
	not_logged_in_hrefs.style.display = "none";
	logged_in_hrefs.style.display = "";
	hamburger.style.display = "";
}

async function postGroup(event){
	event.preventDefault();
	const CGbutton = event.target;

	const form = CGbutton.closest('form');
	const group_CGElement = form.querySelector('input[placeholder*="Group Name"]');
	const group_CGPassElement = form.querySelector('input[placeholder*="Group Password"]');
	const group_MaxuserElement = form.querySelector('input[placeholder*="Max Users"]');
	const group_roadElement = form.querySelector('input[placeholder*="Road Name"]');
	const group_postCodeElement = form.querySelector('input[placeholder*="Post Code"]');

	const group_CG = group_CGElement.value;
	const group_CGPass = group_CGPassElement.value;
	const group_Maxuser = group_MaxuserElement.value;
	const group_road = group_roadElement.value;
	const group_postCode = group_postCodeElement.value;


	if (group_CG === "") {
		setInputError(group_CGElement, 'Please create Group Name');
		return;
	}
	else{
		clearInputError(group_CGElement);
	}


    if (group_CGPass === "") {
		setInputError(group_CGPassElement, 'Please create Group Password');
		return;
	}
	else{
		clearInputError(group_CGPassElement);
	}

    if (group_Maxuser === 0) {
        setInputError(group_MaxuserElement, 'Please enter max users');
        return;
    } else if (!Number.isInteger(Number(group_Maxuser)) || (Number(group_Maxuser) <= 0)) {
        setInputError(group_MaxuserElement, 'The number of users should be a positive integer');
        return;
    } else {
        clearInputError(group_MaxuserElement);
    }

    if (group_road === "") {
		setInputError(group_roadElement, 'Please enter road name');
		return;
	}
	else{
		clearInputError(group_roadElement);
	}

	if (group_postCode === "") {
		setInputError(group_postCodeElement, 'Please enter a post code');
		return;
	}
	else if (group_postCode.length>7) {
		setInputError(group_postCodeElement, 'Invalid Post Code');
		return;
	}
	else{
		clearInputError(group_postCodeElement);
	}

	const response = await fetch(BASE + "house", {
												  	method: 'POST',
												  	headers: {
												    	'Content-Type': 'application/json'
												  	},
												  	body: JSON.stringify({
														h_id: null,
												    	name: group_CG,
														password: group_CGPass,
														max_residents: group_Maxuser,
														road_name: group_road,
														postcode: group_postCode,
												  	})
												})
  	if (response.ok) {
    	console.log({message: "House creation successful"});
    	const obj = await JSON.parse(await response.json());
    	localStorage.setItem("house_id", obj.h_id);
		const responsejoin = await fetch(`${BASE}user/${obj.h_id}/${email_id}/1`, {
						  	method: 'PATCH',
						  	headers: {
						    	'Content-Type': 'application/json'
						  	},
						  	body: {}
							});
		if (responsejoin.ok) {
    		alert("Group Created Successfully. You have been already added to the group.");
		}
		else {
			alert("Group Created Successfully. Please join the group with GROUP ID: " + obj.h_id + ".");
		}

    	window.location.href = "./welcome.html";
  	} else {
    	throw new Error('Request failed.');
  	}
}


async function patchGroup(event){
	event.preventDefault();
	const JGbutton = event.target;

    const form = JGbutton.closest('form');
    const group_JoinIDElement = form.querySelector('input[placeholder*="Group ID"]');
    const group_JGPassElement = form.querySelector('input[placeholder*="Group Password"]');

    const group_JoinID = group_JoinIDElement.value;
    const group_JGPass = group_JGPassElement.value;

	if (group_JoinID === 0) {
        setInputError(group_JoinIDElement, 'Please enter max users');
        return;
    } else if (!Number.isInteger(Number(group_JoinID)) || (Number(group_JoinID) <= 0)) {
        setInputError(group_JoinIDElement, 'Invalid ID');
        return;
    } else {
        clearInputError(group_JoinIDElement);
    }

    if (group_JGPass === "") {
		setInputError(group_JGPassElement, 'Please enter Group Password');
		return;
	}
	else{
		clearInputError(group_JGPassElement);
	}


    if (group_JGPass === "") {
		setInputError(group_JGPassElement, 'Please enter Group Password');
		return;
	}
	else{
		clearInputError(group_JGPassElement);
	}

	const response = await fetch(`${BASE}user/${group_JoinID}/${email_id}/1`, {
							  	method: 'PATCH',
							  	headers: {
							    	'Content-Type': 'application/json'
							  	},
							  	body: {}
								});
  	if (response.ok) {
    	console.log({message: "Joining successful"});
    	const obj = await JSON.parse(await response.json());
		localStorage.setItem("house_id", obj.household_id);
    	alert("Joined Successfully");
    	window.location.href = "./welcome.html";
  	} 
  	else {
    	console.log({message: await response.json()});
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

function isValidEmail(login_Email) {
    const email = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return email.test(login_Email);
}

function logout(){
	// Get all cookies and split them into an array
	localStorage.clear();
  
	console.log("Local Storage cleared");
	window.location.href = "login.html";
}
