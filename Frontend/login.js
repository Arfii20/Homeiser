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
	// else if (!isValidDate(login_Password)){
	// 	setInputError(login_PasswordElement, "The password is invalid");
	// 	return;
	// }
	// else{
	// 	clearInputError(login_PasswordElement);
	// }


    if (login_Password === "") {
        setInputError(login_PasswordElement, 'Please enter password');
        return;
    }
    clearInputError(login_PasswordElement);
    


	fetch(BASE + "login", {
	  	method: 'POST',
	  	headers: {
	    	'Content-Type': 'application/json'
	  	},
	  	body: JSON.stringify({

	  	})
	})
	.then(response => {
	  	if (response.ok) {
	    	console.log({message: "Login successful"});
			// rightContainer.innerHTML = "";
			// rightContainer.style.display = "none";
			// ContinueButton.innerText = "login";
			getLedgerResources(user_id);
	  	} else {
	    	throw new Error('Login failed.');
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

function isValidEmail(login_Email) {
    const register_Email = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return register_Email.test(login_Email);
}