const BASE = "http://127.0.0.1:5000/";
const rightContainer = document.querySelector(".container-right");
const mainTable = document.querySelector(".main-table");
const detailsTable = document.querySelector(".detailsTable");
const leftCreateButton = document.querySelector("#Create-window-button");
const transaction_SrcElement = form.querySelector('input[placeholder*="Full Name of Source User"]');
const transaction_DestElement = form.querySelector('input[placeholder*="Full Name of Destination User"]');
const transaction_AmountElement = form.querySelector('input[placeholder*="Amount"]');
const transaction_DescriptionElement = form.querySelector('input[placeholder*="Amount"]');
const transaction_DueDateElement = form.querySelector('input[placeholder*="Due Date"]');

async function getLedgerResources(userID){
	var returnedData;
	mainTable.setAttribute('id', userID);
	mainTable.innerHTML = "<tbody><tr><td style='border: none;'><h2 style='text-align: center; color: purple;'>No Transaction Pending</h2></td></td></tbody>";

	const response = await fetch(BASE + "ledger/" + userID);
	
	if (response.ok) {
		mainTable.innerHTML = `<thead>
				                <th class="header">
				                  Source User--> Destination User
				                </th>
				                <th class="header">
				                  Due Date
				                </th>
				                <th class="header">
				                  Amount
				                </th>
				              </thead>`

		const response_array = await JSON.parse(await response.json());

		for (let i = 0; i < response_array.length; i++) {
		    const obj = await JSON.parse(response_array[i]);

			console.log(obj);
			var paid;
			if (obj.paid === "true"){
				mainTable.innerHTML += `<tbody id="data-output">
							              	<tr id="${obj.transaction_id}" onclick=getTransaction(event) style="text-decoration: line-through; color: gray;">
								                <td class="table-data"> ${obj.src} --> ${obj.dest}
								                </td>
								                <td class="table-data">
								                  ${obj.due_date}
								                </td>
								                <td class="table-data">
								                  £${obj.amount}
								                </td>
								            <tr>
							              </tbody>`;
			}
			else{
				mainTable.innerHTML +=  `<tbody id="data-output">
							              	<tr id="${obj.transaction_id}" onclick=getTransaction(event)>
								                <td class="table-data"> ${obj.src} --> ${obj.dest}
								                </td>
								                <td class="table-data">
								                  ${obj.due_date}
								                </td>
								                <td class="table-data">
								                  £${obj.amount}
								                </td>
								            <tr>
							              </tbody>`;
			}
		}
	}
	else {
    	throw new Error('Error retrieving ledger.');
    	return;
	}
}


async function getTransaction(event) {
	transactionID = event.target.parentNode.getAttribute("id");
	let returnedData;
	console.log(transactionID);
	console.log(event.target);

	const response = await fetch(BASE + "transaction/" + transactionID)

  	if (response.ok) {
  		// console.log(response.json())
    	const obj = await JSON.parse(await response.json());

		var paidButton;
		if (obj.paid === "true"){
			paidButton = "Mark as Unpaid";
		}
		else{
			paidButton = "Mark as Paid";
		}
		rightContainer.innerHTML =  `<div class="container1">
									  <form class="text" id="transactions">
									    <h1 class="form__title">Transaction: </h1>
									    <div class="form__input-group">
									      <input type="text" class="form__input" placeholder="Full Name of Source User - ${obj.src} " readonly>
									      <div class="form__input-error-message"></div>
									    </div>
									    <div class="form__input-group">
									      <input type="password" class="form__input" placeholder="Full Name of Destination User - ${obj.dest} " readonly>
									      <div class="form__input-error-message"></div>
									    </div>
									    <div class="form__input-group">
									      <input type="text" class="form__input" placeholder="Amount in GBP - ${obj.amount} " readonly>
									      <div class="form__input-error-message"></div>
									    </div>
									    <div class="form__input-group">
									      <input type="text" class="form__input" placeholder="Description - ${obj.description} " readonly>
									      <div class="form__input-error-message"></div>
									    </div>
									    <div class="form__input-group">
									      <input type="text" class="form__input" placeholder="Due Date (yyyy-mm-dd) - ${obj.due_date} " readonly>
									      <div class="form__input-error-message"></div>
									    </div>
									    <button id="${obj.transaction_id}" class="form__button" type="submit" onclick=patchTransaction(event)> ${paidButton} </button>
									    <button id="${obj.transaction_id}" class="form__button" type="submit" onclick=deleteTransaction(event)> Delete </button>
									  </form>
									</div>`;
		leftCreateButton.innerText = "Close Transaction Window";
  	} else {
    	throw new Error('Error retrieving transaction.');
	}
}


async function createcloseRightContainer(event){
	event.preventDefault();
	if (event.target.innerText === "Create Transaction"){
		rightContainer.innerHTML =  `<div class="container1">
						  <form class="text" id="transactions">
						    <h1 class="form__title">Transaction: </h1>
						    <div class="form__input-group">
						      <input type="text" class="form__input" placeholder="Full Name of Source User: ">
						      <div class="form__input-error-message"></div>
						    </div>
						    <div class="form__input-group">
						      <input type="text" class="form__input" placeholder="Full Name of Destination User: ">
						      <div class="form__input-error-message"></div>
						    </div>
						    <div class="form__input-group">
						      <input type="text" class="form__input" placeholder="Amount in GBP: ">
						      <div class="form__input-error-message"></div>
						    </div>
						    <div class="form__input-group">
						      <input type="text" class="form__input" placeholder="Description: ">
						      <div class="form__input-error-message"></div>
						    </div>
						    <div class="form__input-group">
						      <input type="text" class="form__input" placeholder="Due Date (yyyy-mm-dd): ">
						      <div class="form__input-error-message"></div>
						    </div>
						    <button class="form__button" type="submit" onclick=postTransaction(event)> Create Transaction </button>
						  </form>
						</div>`;
		event.target.innerText = "Close Transaction Window";
	}
	else{
		rightContainer.innerHTML = "";
		event.target.innerText = "Create Transaction";
	}
}


async function patchTransaction(event){
	event.preventDefault();
	const transactionID = event.target.id;

	fetch(BASE + "transaction/" + transactionID, {
		method: 'PATCH',
		headers: {
			'Content-Type': 'application/json'
		}
	})
	.then(response => {
		if (response.ok) {
			console.log(response.json());
			if (event.target.innerText === "Mark as Paid"){
				event.target.innerText = "Mark as Unpaid";
			}
			else{
				event.target.innerText = "Mark as Paid";
			getLedgerResources(mainTable.id);
			}
		} else {
			throw new Error('Request failed.');
		}
	})
	.catch(error => {
		console.log(error);
	});
}

async function deleteTransaction(event){
	event.preventDefault();
	const transactionID = event.target.id;

	fetch(BASE + "transaction/" + transactionID, {
	method: 'DELETE',
	headers: {
		'Content-Type': 'application/json'
		}
	})
	.then(response => {
		if (response.ok) {
			console.log(response.json());
			rightContainer.innerHTML = "";
			getLedgerResources(mainTable.getAttribute('id'));
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


async function postTransaction(event){
	event.preventDefault();
	const button = event.target;

	const form = button.closest('form');

	const transaction_SrcID = 0;
	const transaction_DestID = 0;
	const transaction_Src = transaction_SrcElement.value;
	const transaction_Dest = transaction_DestElement.value;
	const transaction_Amount = transaction_AmountElement.value;
	const transaction_Description = transaction_DescriptionElement.value;
	const transaction_DueDate = transaction_DueDateElement.value;
	const transaction_Paid = "false";
	const transaction_HouseId = 620;

	// if (transaction_Src === "" || transaction_Dest === "" || transaction_Amount === "" || transaction_Description === "" || transaction_DueDate === ""){
	// 	alert("Please add all fields");
	// 	return;
	// }

	if (transaction_Src === "") {
	  setInputError(transaction_SrcElement, 'Please enter source user');
	  return;
	}

	if (transaction_Dest === "") {
	  setInputError(transaction_DestElement, 'Please enter destination user');
	  return;
	}

	if (transaction_Amount === "") {
	  setInputError(transaction_AmountElement, 'Please enter amount');
	  return;
	}

	if (transaction_Description === "") {
	  setInputError(transaction_DescriptionElement, 'Please enter description');
	  return;
	}

	if (transaction_DueDate === "") {
	  setInputError(transaction_DueDateElement, 'Please enter due date');
	  return;
	}


	try {
		parseInt(transaction_Amount);
	}
	catch(error){
		alert("The amount is invalid");
		return;
	}

	const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
	if (!transaction_DueDate.match(dateRegex)){
		alert("Date must be in yyyy-mm-dd format");
		return;
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
	    	const returnedData = response.json();
			rightContainer.innerHTML = "";
			leftCreateButton.innerText = "Create Transaction";
			getLedgerResources(mainTable.id);
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

function setInputError(inputElement, errorMessage) {
	const inputGroupElement = inputElement.parentElement;
	const errorElement = inputGroupElement.querySelector('.form__input');
	inputGroupElement.classList.add('form__input-group--error');
	errorElement.innerText = errorMessage;
}


getLedgerResources(630);
