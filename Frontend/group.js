async function fetchGroup(event){
	event.preventDefault();
    // console.log("sis");
	const button = event.target;

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


async function postGroup(event){
	event.preventDefault();
    // console.log("sis");
	const button = event.target;

	const form = button.closest('form');
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
	else if (!Maxuser(parseInt(group_Maxuser))) {
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

function Maxuser(num) {
    if (typeof num !== "number" || num < 1 || Number.isNaN(num)) {
      console.log("The number must be greater than 1");
      return false;
    }
    return true;
  }
  