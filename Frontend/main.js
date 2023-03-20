function setFormMessage(formElement, type, message) {
    const messageElement = formElement.querySelector(".form__message");

    messageElement.textContent = message;
    messageElement.classList.remove("form__message-success", "form__message--error");
    messageElement.classList.add(`form__message--${type}`);
}

function setInputError(inputElement, message) {
    inputElement.classList.add("form__input--error");
    inputElement.parentElement.querySelector(".form__input-error-message").textContent = message;
}

function clearInputError(inputElement) {
    inputElement.classList.remove("form__input--error");
    inputElement.parentElement.querySelector(".form__input-error-message").textContent = "";
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.querySelector("#login");
    const createAccountForm = document.querySelector("#createAccount");

    loginForm.addEventListener("submit", e => {
        e.preventDefault();

        //Perform your AJAX/Fetch login

        setFormMessage(loginForm, "error", "Invalid username/password combination");
    });

    document.querySelectorAll(".form__input").forEach(inputElement => {
        inputElement.addEventListener("blur", e => {
            if (e.target.id === "signupUsername" && e.target.value.length > 0 && e.target.value.length < 10) {
                setInputError(inputElement, "Username must be at least 10 characters in length");
            }
        });

        inputElement.addEventListener("input", e => {
            clearInputError(inputElement);
        });
    });
});


document.querySelectorAll(".form__input").forEach(inputElement => {
    inputElement.addEventListener("blur", e => {
        if (e.target.id === "signupEmail" && !isValidEmail(e.target.value)) {
            setInputError(inputElement, "Wrong email address");
        }
    });

    inputElement.addEventListener("input", e => {
        clearInputError(inputElement);
    });
});

document.querySelectorAll(".form__input").forEach(inputElement => {
    inputElement.addEventListener("blur", e => {
        if (e.target.id === "signupPassword2" && e.target.value !== document.querySelector("#signupPassword1").value) {
            setInputError(inputElement, "Incorrect password");
        }
    });

    inputElement.addEventListener("input", e => {
        clearInputError(inputElement);
    });
});



//
async function postRegister(event){
	event.preventDefault();
	const button = event.target;

	const form = button.closest('form');
	const register_FnameElement = form.querySelector('input[placeholder*="First Name"]');
	const register_LnametElement = form.querySelector('input[placeholder*="Last Name"]');
	const register_EmailElement = form.querySelector('input[placeholder*="Email Address"]');
	const register_PasswordElement = form.querySelector('input[placeholder*="Password"]');
	const register_ConfirmElement = form.querySelector('input[placeholder*="Confirm Password"]');

	const register_FnameID = 0;
	const register_LnameID = 0;
	const register_Fname = transaction_FnameElement.value;
	const register_Lname = transaction_LnameElement.value;
	const register_Email = transaction_EmailElement.value;
	const transaction_Password = transaction_PasswordElement.value;
	const transaction_Confirm = transaction_ConfirmElement.value;
	const transaction_Paid = "false";
	const transaction_HouseId = house_id;

	if (transaction_Src === "") {
		setInputError(transaction_SrcElement, 'Please enter source user');
		return;
	}
	else{
		clearInputError(transaction_SrcElement);
	}

	if (transaction_Dest === "") {
		setInputError(transaction_DestElement, 'Please enter destination user');
		return;
	}
	else{
		clearInputError(transaction_DestElement);
	}

	if (transaction_Amount === "") {
		setInputError(transaction_AmountElement, 'Please enter amount');
		return;
	}
	else if (isNaN(parseInt(transaction_Amount))) {
		setInputError(transaction_AmountElement, 'The amount is invalid');
		return;
	}
	else{
		clearInputError(transaction_AmountElement);
	}

	if (transaction_Description === "") {
		setInputError(transaction_DescriptionElement, 'Please enter description');
		return;
	}
	else{
		clearInputError(transaction_DescriptionElement);
	}

	if (transaction_DueDate === "") {
		setInputError(transaction_DueDateElement, 'Please enter due date');
		return;
	}
	else if (!isValidDate(transaction_DueDate)){
		setInputError(transaction_DueDateElement, "Date must be valid and in yyyy-mm-dd format");
		return;
	}
	else{
		clearInputError(transaction_DueDateElement);
	}

	fetch(BASE + "transaction", {
	  	method: 'POST',
	  	headers: {
	    	'Content-Type': 'application/json'
	  	},
	  	body: JSON.stringify({
	    	src_id: transaction_SrcID,
	    	dest_id: transaction_DestID,
	    	src: transaction_Src,
	    	dest: transaction_Dest,
	    	amount: parseInt(transaction_Amount),
	    	description: transaction_Description,
	    	due_date: transaction_DueDate,
	    	paid: transaction_Paid,
	    	house_id: transaction_HouseId
	  	})
	})
	.then(response => {
	  	if (response.ok) {
	    	console.log({message: "Creation successful"});
			rightContainer.innerHTML = "";
			rightContainer.style.display = "none";
			leftCreateButton.innerText = "Create Transaction";
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


// function setInputError(inputElement, errorMessage, inputGroupSelector = '.form__input-group') {
// 	const inputGroupElement = inputElement.closest(inputGroupSelector);
// 	const errorElement = inputGroupElement.querySelector('.form__input-error-message');
// 	inputGroupElement.classList.add('form__input-group--error');
// 	errorElement.innerText = errorMessage;
// }

// function clearInputError(inputElement, inputGroupSelector = '.form__input-group') {
// 	const inputGroupElement = inputElement.closest(inputGroupSelector);
// 	const errorElement = inputGroupElement.querySelector('.form__input-error-message');
// 	inputGroupElement.classList.remove('form__input-group--error');
// 	errorElement.innerText = '';
// }