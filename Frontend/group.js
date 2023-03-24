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

	const regex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W)[a-zA-Z\d\W]{8,}$/;
    if (group_CGPass === "") {
		setInputError(group_CGPassElement, 'Please create Group Password');
		return;
	}
	else if (!regex.test(group_CGPass)) {
		setInputError(group_CGPassElement, 'Password must be minimum 8 characters with a digit, a lowercase, an uppercase and a symbol');
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
			await addBirthdays();
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

	if (!Number.isInteger(Number(group_JoinID)) || (Number(group_JoinID) <= 0)) {
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

	try{
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
			await addBirthdays();
	    	alert("Joined Successfully");
	    	window.location.href = "./welcome.html";
	  	} 
  	}
	catch (error) {
	    if (error.message === 'Failed to fetch') {
	  		setInputError(group_JoinIDElement, 'Group does not exist');
	    	console.log({message: await response.json()});
	  	}
	}
}

async function addBirthdays(){
	const local_house = localStorage.getItem("house_id");
	const response_user = await fetch(`${BASE}user/${email_id}`);

	if (response_user.ok) {
		{message: "User received"}
	}
	else {
		{message: "Error receiving user"}
	}

    const user_obj = await JSON.parse(await response_user.json());

    console.log(user_obj)
    console.log(user_obj.dob)

    const month_day = user_obj.dob.substring(5);

    for (let i = 2023; i < 2030; i++){
		const eventTimeFromConverted = `${i}-${month_day} 00:00:00`;
		const eventTimeToConverted = `${i}-${month_day} 23:59:00`;

		const url = BASE + "shared_calendar/" + local_house;
		const data = new URLSearchParams();

		data.append('title_of_event', `Birthday of ${user_obj.first_name} ${user_obj.surname}`);
		data.append('starting_time', eventTimeFromConverted);
		data.append('ending_time', eventTimeToConverted);
		data.append('additional_notes', "Might have a party");
		data.append('location_of_event', "Common Area");
		data.append('tagged_users', `${user_id}`);   
		data.append('added_by', parseInt(user_id));

		const response = await fetch(url, {
		              method: 'POST',
		              body: data,
		              headers: {
		                'Content-Type': 'application/x-www-form-urlencoded'
		              }
		            });

		if (response.ok){
			console.log({message: "Birthday Added"});
		}
		else {
			console.log({message: "Error Adding Birthday"});
		}
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

function logout(){
	// Get all cookies and split them into an array
	localStorage.clear();
  
	console.log("Local Storage cleared");
	window.location.href = "login.html";
}
