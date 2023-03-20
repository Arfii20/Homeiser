async function postGroup(event){
	event.preventDefault();
    console.log("sis");
	const button = event.target;

	const form = button.closest('form');
	const group_CGElement = form.querySelector('input[placeholder*="Create Group name"]');
	const group_JGElement = form.querySelector('input[placeholder*="Join Group name"]');
	const group_CGPassElement = form.querySelector('input[placeholder*="Create Group password"]');
	const group_JGPassElement = form.querySelector('input[placeholder*="Join Group password"]');
	const group_MaxuserElement = form.querySelector('input[placeholder*="Max Users"]');

	// const group_FnameID = 0;
	// const group_LnameID = 0;
	const group_CG = group_CGElement.value;
	const group_JG = group_JGElement.value;
	const group_CGPass = group_CGPassElement.value;
    const group_JGPass = group_JGPassElement.value;
	const group_Maxuser = group_MaxuserElement.value;
	// const group_Paid = "false";
	// const group_HouseId = house_id;

	if (group_CG === "") {
		setInputError(group_CGElement, 'Please enter Group Name');
		return;
	}
	else{
		clearInputError(group_CGElement);
	}

	if (group_JG === "") {
		setInputError(group_JGElement, 'Please enter Group Name');
		return;
	}
	else{
		clearInputError(group_JGElement);
	}



    if (group_Maxuser === "") {
		setInputError(group_MaxuserElement, 'Please enter max users');
		return;
	}
	else if (maxuser(parseInt(group_Maxuser))) {
		setInputError(group_MaxuserElement, 'The number of user should greater than 0');
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
	    	// Fname_id: group_FnameID,
	    	// Lname_id: group_LnameID,
	    	fname: group_Fname,
	    	lname: group_Lname,
	    	// amount: parseInt(group_Amount),
	    	confirm: group_Confirm,
	    	password: group_Password,
            email: group_Email,
            color: null,

	    	// paid: group_Paid,
	    	// house_id: group_HouseId
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


function isValidDate(dateString) {
	const regex = /^\d{4}-\d{2}-\d{2}$/;
	if (!regex.test(dateString)) {
		return false;
	}
	const date = new Date(dateString);
	if (isNaN(date.getTime())) {
		return false;
	}
	return true;
}