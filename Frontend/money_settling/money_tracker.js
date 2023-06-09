const BASE = "http://127.0.0.1:5000/";
const rightContainer = document.querySelector(".container-right");
const mainTable = document.querySelector(".main-table");
const detailsTable = document.querySelector(".detailsTable");
const leftCreateButton = document.querySelector("#Create-window-button");
const simplifyButton = document.querySelector(".simplify_button");
const logged_in_hrefs = document.querySelector(".if-logged-in");
const not_logged_in_hrefs = document.querySelector(".if-not-logged-in");
const hamburger = document.querySelector(".hamburger");

const user_id = localStorage.getItem("user_id");
const house_id = localStorage.getItem("house_id");
// const user_id = 630;
// const house_id = 620;

if (user_id === null || user_id === undefined || user_id === "undefined" || user_id === "null") {
  not_logged_in_hrefs.style.display = "";
  logged_in_hrefs.style.display = "none";
  hamburger.style.display = "none";
  window.location.href = "../login.html";
}
if (house_id === null || house_id === "undefined" || house_id === "undefined" || house_id === "null") {
  window.location.href = "../group.html";
}

not_logged_in_hrefs.style.display = "none";
logged_in_hrefs.style.display = "";
hamburger.style.display = "";

rightContainer.style.display = "none";
getLedgerResources(user_id);

async function getLedgerResources(user_id){
	mainTable.innerHTML = "<tbody><tr><td style='border: none;'><h2 style='text-align: center; color: purple;'>No Transaction Pending</h2></td></td></tbody>";
	simplifyButton.style.display = "none";

	try{
		const response = await fetch(BASE + "ledger/" + user_id);
		
		if (response.ok) {
			console.log({message: "Ledger Received"});
			simplifyButton.style.display = "";
			mainTable.innerHTML = `<thead class="fixed">
					                <th class="header">
					                  Source User --> Destination User
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

				var paid;
				if (obj.paid === "true"){
					mainTable.innerHTML += `<tbody id="data-output">
								              	<tr id="${obj.transaction_id}" onclick=getTransaction(event) style="color: gray; opacity: 80%">
									                <td class="table-data"> ${obj.src} --> ${obj.dest}
									                </td>
									                <td class="table-data">
									                  ${obj.due_date}
									                </td>
									                <td class="table-data" style="align:center">
									                  £${obj.amount/100}
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
									                  £${obj.amount/100}
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
	catch (error) {
    console.error(error);
    if (error.message === 'Failed to fetch') {
        createMockUpHTMLofLedger();
    }
  }
}

async function getTransaction(event) {
	transactionID = event.target.parentNode.getAttribute("id");
	try {
		const response = await fetch(BASE + "transaction/" + transactionID)

	  	if (response.ok) {
	  		rightContainer.style.display = "";
	  		console.log({message: "transaction Received"});
	    	const obj = await JSON.parse(await response.json());

			var paidButton;
			if (obj.paid === "true"){
				paidButton = "Mark as Unpaid";
			}
			else{
				paidButton = "Mark as Paid";
			}
			rightContainer.innerHTML =  `<div class="container2">
										  <form class="text" id="transactions">
										    <h1 class="form__title" style="color:#a220a4; margin-top:0.5rem; margin-bottom:2rem">Transaction</h1>
										    <div class="form__input-error-message"></div>
										    <div class="form__input-group">
										      <input type="text" class="form__input" placeholder="Source User - ${obj.src} " readonly>
										      <div class="form__input-error-message"></div>
										    </div>
										    <div class="form__input-group">
										      <input type="password" class="form__input" placeholder="Destination User - ${obj.dest} " readonly>
										      <div class="form__input-error-message"></div>
										    </div>
										    <div class="form__input-group">
										      <input type="text" class="form__input" placeholder="Amount - £${obj.amount/100} " readonly>
										      <div class="form__input-error-message"></div>
										    </div>
										    <div class="form__input-group">
										      <input type="text" class="form__input" placeholder="Description - ${obj.description} " readonly>
										      <div class="form__input-error-message"></div>
										    </div>
										    <div class="form__input-group">
										      <input type="text" class="form__input" placeholder="Due Date - ${obj.due_date} " readonly>
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
	catch (error) {
    console.error(error);
    if (error.message === 'Failed to fetch') {
        createMockUpHTMLofTransaction();
    }
  }
}

async function createcloseRightContainer(event){
	event.preventDefault();
	if (event.target.innerText === "Create Transaction"){
		rightContainer.style.display = "";
		console.log({message: "Right container created"});
		rightContainer.innerHTML =  `<div class="container2">
						  <form class="text" id="transactions">
							<h1 class="form__title" style="color:#a220a4">New Transaction</h1>
							<h5 class="form__title" style="margin-bottom: 1.7rem">You can find ID in Group Tab</h5>
						   	<div class="form__input-error-message"></div>
						    <div class="form__input-group">
						      <input type="number" class="form__input" placeholder="ID of User who owes you: ">
						      <div class="form__input-error-message"></div>
						    </div>
						    <div class="form__input-group">
						      <input type="text" class="form__input" placeholder="Name of the User: ">
						      <div class="form__input-error-message"></div>
						    </div>
						    <div class="form__input-group">
						      <input type="number" class="form__input" placeholder="Amount in GBP: " step="0.01">
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
		console.log({message: "Right container closed"});
		rightContainer.innerHTML = "";
		rightContainer.style.display = "none";
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
			if (event.target.innerText === "Mark as Paid"){
				event.target.innerText = "Mark as Unpaid";
				console.log({message: "Marked as Paid"});
			}
			else{
				event.target.innerText = "Mark as Paid";
				console.log({message: "Marked as Unpaid"});
			}
			getLedgerResources(user_id);
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
			rightContainer.innerHTML = "";
			rightContainer.style.display = "none";
			leftCreateButton.innerText = "Create Transaction";
			getLedgerResources(user_id);
			console.log({message: "Transaction deleted"});
		} else {
			throw new Error('Request failed.');
		}
	})
	.then(data => {
	})
	.catch(error => {
		console.log(error);
	});
}

async function postTransaction(event){
	event.preventDefault();
	const button = event.target;

	const form = button.closest('form');
	const transaction_SrcElement = form.querySelector('input[placeholder*="ID of User who owes you"]');
	const transaction_DestElement = form.querySelector('input[placeholder*="Name of the User"]');
	const transaction_AmountElement = form.querySelector('input[placeholder*="Amount"]');
	const transaction_DescriptionElement = form.querySelector('input[placeholder*="Description"]');
	const transaction_DueDateElement = form.querySelector('input[placeholder*="Due Date"]');
	
	const transaction_Src = transaction_SrcElement.value;
	const transaction_Dest = transaction_DestElement.value;
	const transaction_Amount = parseInt(transaction_AmountElement.value*100);
	const transaction_Description = transaction_DescriptionElement.value;
	const transaction_DueDate = transaction_DueDateElement.value;
	const transaction_Paid = "false";

	if (!Number.isInteger(Number(transaction_Src)) || (Number(transaction_Src) <= 0)) {
		setInputError(transaction_SrcElement, 'Invalid source user');
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

	if (transaction_Amount === 0) {
		setInputError(transaction_AmountElement, 'Please enter amount');
		return;
	}
	else if (transaction_Amount <= 0) {
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
	  		transaction_id: 0,
	    	src_id: transaction_Src,
	    	dest_id: user_id,
	    	src: "Does not Matter",
	    	dest: "Does not Matter",
	    	amount: parseInt(transaction_Amount),
	    	description: transaction_Description.replace(/'/g, "\\'"),
	    	due_date: transaction_DueDate,
	    	paid: transaction_Paid,
	    	house_id: 0
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

	})
	.catch(error => {
	  	if (error.message === 'Failed to fetch') {
        	setInputError(transaction_SrcElement, 'Invalid source user');
			return;
    	}
	});
}

async function simplifyDebts(event){
	const url = `${BASE}simplify/${house_id}`;

	await fetch(url, {
	  method: 'POST',
	  headers: {
	    'Content-Type': 'application/json'
	  },
	  body: {}
	})
	.then(response => {
		if (response.ok) {
	  		getLedgerResources(user_id);
	  		console.log({message: "transactions simplified"});
		}
	})
	.catch(error => {
		console.error('Could not simplify', error);
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
	const regex = /^(?:(?:19|20)[0-9]{2})-(?:(?:0[1-9])|(?:1[0-2]))-(?:(?:0[1-9])|(?:[1-2][0-9])|(?:3[0-1]))$/;
	if (!regex.test(dateString)) {
		return false;
	}
	const date = new Date(dateString);
	if (isNaN(date.getTime())) {
		return false;
	}
	return true;
}

function createMockUpHTMLofLedger(){
	mainTable.innerHTML = "<tbody><tr><td style='border: none;'><h2 style='text-align: center; color: purple;'>No Transaction Pending</h2></td></td></tbody>";
	simplifyButton.style.display = "none";
	
	console.log({message: "Ledger Received"});
	simplifyButton.style.display = "";
	mainTable.innerHTML = `<thead class="fixed">
			                <th class="header">
			                  Source User --> Destination User
			                </th>
			                <th class="header">
			                  Due Date
			                </th>
			                <th class="header">
			                  Amount
			                </th>
			              </thead>`

	const response_array =
	[
    {   
    	transaction_id: 51,
      src_id: 40,
      dest_id: 50,
     	src: "Mock Person 1",
      dest: "Mock Person 2",
      amount: 20,
      description: "Description of Mock Transaction 1",
      due_date: "2023-06-25",
      paid: "false",
      house_id: 20
    },
        {   
    	transaction_id: 52,
      src_id: 50,
      dest_id: 40,
     	src: "Mock Person 2",
      dest: "Mock Person 1",
      amount: 10,
      description: "Description of Mock Transaction 2",
      due_date: "2023-05-20",
      paid: "false",
      house_id: 20
    },
        {   
    	transaction_id: 53,
      src_id: 40,
      dest_id: 50,
     	src: "Mock Person 1",
      dest: "Mock Person 2",
      amount: 50,
      description: "Description of Mock Transaction 3",
      due_date: "2023-06-15",
      paid: "true",
      house_id: 20
    },
    {   
    	transaction_id: 54,
      src_id: 40,
      dest_id: 50,
     	src: "Mock Person 1",
      dest: "Mock Person 2",
      amount: 20,
      description: "Description of Mock Transaction 4",
      due_date: "2023-06-0",
      paid: "false",
      house_id: 20
    },
    {   
    	transaction_id: 55,
      src_id: 40,
      dest_id: 50,
     	src: "Mock Person 1",
      dest: "Mock Person 2",
      amount: 20,
      description: "Description of Mock Transaction 5",
      due_date: "2023-06-06",
      paid: "false",
      house_id: 20
    },
        {   
    	transaction_id: 56,
      src_id: 50,
      dest_id: 40,
     	src: "Mock Person 2",
      dest: "Mock Person 1",
      amount: 10,
      description: "Description of Mock Transaction 6",
      due_date: "2023-05-20",
      paid: "false",
      house_id: 20
    },
        {   
    	transaction_id: 57,
      src_id: 40,
      dest_id: 50,
     	src: "Mock Person 1",
      dest: "Mock Person 2",
      amount: 50,
      description: "Description of Mock Transaction 7",
      due_date: "2023-06-21",
      paid: "true",
      house_id: 20
    },
    {   
    	transaction_id: 58,
      src_id: 40,
      dest_id: 50,
     	src: "Mock Person 1",
      dest: "Mock Person 2",
      amount: 20,
      description: "Description of Mock Transaction 8",
      due_date: "2023-05-22",
      paid: "false",
      house_id: 20
    }
	]

	for (let i = 0; i < response_array.length; i++) {
	  const obj = response_array[i];

		var paid;
		if (obj.paid === "true"){
			mainTable.innerHTML += `<tbody id="data-output">
						              	<tr id="${obj.transaction_id}" onclick=getTransaction(event) style="color: gray; opacity: 80%">
							                <td class="table-data"> ${obj.src} --> ${obj.dest}
							                </td>
							                <td class="table-data">
							                  ${obj.due_date}
							                </td>
							                <td class="table-data" style="align:center">
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

function createMockUpHTMLofTransaction(){
	rightContainer.style.display = "";
	console.log({message: "transaction Received"});
	const paidButton = "Mark as Paid";
	rightContainer.innerHTML =  `<div class="container2">
								  <form class="text" id="transactions">
								    <h1 class="form__title" style="color:#a220a4">Transaction</h1>
								    <div class="form__input-error-message"></div>
								    <div class="form__input-group">
								      <input type="text" class="form__input" placeholder="Source User - Mockup User 1 " readonly>
								      <div class="form__input-error-message"></div>
								    </div>
								    <div class="form__input-group">
								      <input type="password" class="form__input" placeholder="Destination User - Mockup User 2 " readonly>
								      <div class="form__input-error-message"></div>
								    </div>
								    <div class="form__input-group">
								      <input type="text" class="form__input" placeholder="Amount - £10 " readonly>
								      <div class="form__input-error-message"></div>
								    </div>
								    <div class="form__input-group">
								      <input type="text" class="form__input" placeholder="Description - Description of Mockup Transaction " readonly>
								      <div class="form__input-error-message"></div>
								    </div>
								    <div class="form__input-group">
								      <input type="text" class="form__input" placeholder="Due Date - 2023-05-25 " readonly>
								      <div class="form__input-error-message"></div>
								    </div>
								    <button class="form__button" type="submit" onclick=patchTransaction(event)> ${paidButton} </button>
								    <button class="form__button" type="submit" onclick=deleteTransaction(event)> Delete </button>
								  </form>
								</div>`;
	leftCreateButton.innerText = "Close Transaction Window";
}

function logout(){
	// Get all cookies and split them into an array
	localStorage.clear();
  
	console.log("Local Storage cleared");
	window.location.href = "login.html";
}
