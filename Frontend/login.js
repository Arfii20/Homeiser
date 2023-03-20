async function postLogin(event){
	event.preventDefault();
    console.log("sis");
	const button = event.target;

	const form = button.closest('form');
	// const login_FnameElement = form.querySelector('input[placeholder*="First Name"]');
	const login_EmailElement = form.querySelector('input[placeholder*="Email Address"]');
	const login_PasswordElement = form.querySelector('input[placeholder*="Password"]');
	// const login_PasswordElement = form.querySelector('input[placeholder*="Password"]');
	// const login_ConfirmElement = form.querySelector('input[placeholder*="Confirm Password"]');

	// const login_FnameID = 0;
	// const login_LnameID = 0;
	// const login_Fname = login_FnameElement.value;
	// const login_Lname = login_LnameElement.value;
	const login_Email = login_EmailElement.value;
    const login_Password = login_PasswordElement.value;
	// const login_Confirm = login_ConfirmElement.value;
	// const login_Paid = "false";
	// const login_HouseId = house_id;

	// if (login_Fname === "") {
	// 	setInputError(login_FnameElement, 'Please enter Email');
	// 	return;
	// }
	// else{
	// 	clearInputError(login_FnameElement);
	// }

	// if (login_Lname === "") {
	// 	setInputError(login_LnameElement, 'Please enter Password');
	// 	return;
	// }
	// else{
	// 	clearInputError(login_Lname);
	// }

	if (login_Email === "") {
		setInputError(login_EmailElement, 'Please enter email');
		return;
	}
	else if (isNaN(parseInt(login_Email))) {
		setInputError(login_EmailElement, 'The email address is invalid');
		return;
	}
	else{
		clearInputError(login_EmailElement);
	}

	// if (login_Password === "") {
	// 	setInputError(login_PasswordElement, 'Please enter password');
	// 	return;
	// }
	// else{
	// 	clearInputError(login_PasswordElement);
	// }

	if (login_Password === "") {
		setInputError(login_PasswordElement, 'Please enter password');
		return;
	}
	else if (!isValidDate(login_Password)){
		setInputError(login_PasswordElement, "The password is invalid");
		return;
	}
	else{
		clearInputError(login_PasswordElement);
	}

	fetch(BASE + "login", {
	  	method: 'POST',
	  	headers: {
	    	'Content-Type': 'application/json'
	  	},
	  	body: JSON.stringify({
	    	// Fname_id: login_FnameID,
	    	// Lname_id: login_LnameID,
	    	fname: login_Fname,
	    	lname: login_Lname,
	    	// amount: parseInt(login_Amount),
	    	confirm: login_Confirm,
	    	password: login_Password,
            email: login_Email,
            color: null,

	    	// paid: login_Paid,
	    	// house_id: login_HouseId
	  	})
	})
	.then(response => {
	  	if (response.ok) {
	    	console.log({message: "Registration successful"});
			// rightContainer.innerHTML = "";
			// rightContainer.style.display = "none";
			ContinueButton.innerText = "login";
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