async function postGroup(event){
	event.preventDefault();
    console.log("sis");
	const CGbutton = event.target;

	const form = CGbutton.closest('form');
	const group_CGElement = form.querySelector('input[placeholder*="Create Group name"]');
	const group_CGPassElement = form.querySelector('input[placeholder*="Create Group password"]');
	const group_MaxuserElement = form.querySelector('input[placeholder*="Max Users"]');


	const group_CG = group_CGElement.value;
	const group_CGPass = group_CGPassElement.value;
	const group_Maxuser = group_MaxuserElement.value;


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


    if (group_Maxuser === "") {
		setInputError(group_MaxuserElement, 'Please enter max users');
		return;
	}
	else if (!isMaxUserValid(parseInt(group_Maxuser))) {
		setInputError(group_MaxuserElement, 'The number of user should greater than 1');
		return;
	}
	else{
		clearInputError(group_MaxuserElement);
	}




	fetch(BASE + "group", {
	  	method: 'POST',
	  	headers: {
	    	'Content-Type': 'application/json'
	  	},
	  	body: JSON.stringify({
	
	  	})
	})
	.then(response => {
	  	if (response.ok) {
	    	console.log({message: "Registration successful"});
			// rightContainer.innerHTML = "";
			// rightContainer.style.display = "none";
			ContinueButton.innerText = "group";
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


// function isMaxUserValid(group_Maxuser, group_MaxuserElement) {
//     const regex = /^[1-9]\d*$/;
//     if (!regex.test(group_Maxuser)) {
//       setInputError(group_MaxuserElement, 'The number of users should be a positive integer');
//       return false;
//     }
//     const num = parseInt(group_Maxuser);
//     if (num <= 0) {
//       setInputError(group_MaxuserElement, 'The number of users should be greater than 0');
//       return false;
//     }
//     clearInputError(group_MaxuserElement);
//     return true;
//   }
  
//   if (group_Maxuser === "") {
//     setInputError(group_MaxuserElement, 'Please enter max users');
//     return;
//   }
  


async function patchGroup(event){
	event.preventDefault();
    console.log("sis");
	const JGbutton = event.target;

    const form = JGbutton.closest('form');
    const group_JGElement = form.querySelector('input[placeholder*="Join Group name"]');
    const group_JGPassElement = form.querySelector('input[placeholder*="Join Group password"]');

    const group_JG = group_JGElement.value;
    const group_JGPass = group_JGPassElement.value;

    if (group_JG === "") {
		setInputError(group_JGElement, 'Please enter Group Name');
		return;
	}
	else{
		clearInputError(group_JGElement);
	}

    if (group_JGPass === "") {
		setInputError(group_JGPassElement, 'Please enter Group Password');
		return;
	}
	else{
		clearInputError(group_JGPassElement);
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


// function Maxuser(group_Maxuser) {
// 	const date = new Date(group_Maxuser);
// 	if (Maxuser(date.getTime())) {
// 		return false;
// 	}
// 	return true;
// }

  

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