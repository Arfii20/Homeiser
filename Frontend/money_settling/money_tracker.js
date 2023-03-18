const BASE = "http://127.0.0.1:5000/";
const rightContainer = document.querySelector(".container-right");
const mainTable = document.querySelector(".main-table");
const detailsTable = document.querySelector(".detailsTable");

async function getLedgerResources(userID){
	var returnedData;
	mainTable.setAttribute('id', userID);

	const response = fetch(BASE + "ledger/" + userID);

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
				                <th class="header">
				                  Paid
				                </th>
				              </thead>`

		const response_array = await JSON.parse(response.json());
		for (let i = 0; i < response_array.length; i++) {
			const obj = await JSON.parse(response_array[i]);

			console.log(obj.paid);
			var paid;
			if (obj.paid){
				mainTable.innerHTML += `<tbody id="data-output">
							              	<tr id="${transaction_id}" onlick=getTransaction(event) style="text-decoration: line-through; color: gray;">
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
							              	<tr id="${transaction_id}" onlick=getTransaction(event)>
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
  		mainTable.innerHTML = "<tbody><tr style='text-decoration: none;'><td style='border: none;'><h2 style='text-align: center; color: purple;' >No Transaction Pending</h2></td></td></tbody>";
    	throw new Error('Error retrieving ledger.');
    	return;
	}
}


async function getTransaction (event) {
	transactionID = event.target.id;

	fetch(BASE + "transaction/" + transactionID)
	.then(response => {
	  	if (response.ok) {
	    	const returnedData = response.json();
	  	} else {
	    	throw new Error('Error retrieving transaction.');
	  	}
	})
	.then(data => {
	  	console.log(data);
	})
	.catch(error => {
	  	console.log(error);
	});

	console.log(returnedData);

	const obj = await JSON.parse(response_array[i]);
		var paidButton;
		if (obj.paid){
			paidButton = "Mark as Unpaid";
		}
		else{
			paidButton = "Mark as Paid";
		}
	rightContainer.innerHTML =  `<div class="container1">
								  <form class="text" id="transactions">
								    <h1 class="form__title">Transaction: </h1>
								    <div class="form__message form__message--error"></div>
								    <div class="form__input-group">
								      <input type="text" class="form__input" autofocus placeholder=" Full Name of Source User: ${obj.src} " readonly>
								      <div class="form__input-error-message"></div>
								    </div>
								    <div class="form__input-group">
								      <input type="password" class="form__input" autofocus placeholder=" Full Name of Destination User: ${obj.dest} " readonly>
								      <div class="form__input-error-message"></div>
								    </div>
								    <div class="form__input-group">
								      <input type="text" class="form__input" autofocus placeholder=" Amount: ${obj.amount} " readonly>
								      <div class="form__input-error-message"></div>
								    </div>
								    <div class="form__input-group">
								      <input type="text" class="form__input" autofocus placeholder=" Description: ${obj.description} " readonly>
								      <div class="form__input-error-message"></div>
								    </div>
								    <div class="form__input-group">
								      <input type="text" class="form__input" autofocus placeholder=" Due Date: ${obj.due_date} " readonly>
								      <div class="form__input-error-message"></div>
								    </div>
								    <button id="${obj.id}" class="form__button" type="submit" onlick=paidUnpaidCreateButton(event)> ${paidButton} </button>
								    <button id="${obj.id}" class="form__button" type="submit" onclick=deleteTransaction(event)> Delete </button>
								  </form>
								</div>`;
}

async function createTransactionRightContainer(event){

}


async function createcloseRightContainer(event){
	let innerText = event.target.innerText;
	if (innerText === "Create Transaction"){
		rightContainer.innerHTML =  `<div class="container1">
						  <form class="text" id="transactions">
						    <h1 class="form__title">Transaction: </h1>
						    <div class="form__message form__message--error"></div>
						    <div class="form__input-group">
						      <input type="text" class="form__input" autofocus placeholder=" Full Name of Source User: ">
						      <div class="form__input-error-message"></div>
						    </div>
						    <div class="form__input-group">
						      <input type="password" class="form__input" autofocus placeholder=" Full Name of Destination User: ">
						      <div class="form__input-error-message"></div>
						    </div>
						    <div class="form__input-group">
						      <input type="text" class="form__input" autofocus placeholder=" Amount: ">
						      <div class="form__input-error-message"></div>
						    </div>
						    <div class="form__input-group">
						      <input type="text" class="form__input" autofocus placeholder=" Description: ">
						      <div class="form__input-error-message"></div>
						    </div>
						    <div class="form__input-group">
						      <input type="text" class="form__input" autofocus placeholder=" Due Date: ">
						      <div class="form__input-error-message"></div>
						    </div>
						    <button class="form__button" type="submit" onlick=paidUnpaidCreateButton(event)> Create Transaction </button>
						  </form>
						</div>`;
		event.target.innerText = "Close Transaction Window";
	}
	else{
		rightContainer.innerHTML = "";
		event.target.innerText = "Create Transaction";
	}
}



getLedgerResources(630);
