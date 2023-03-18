const BASE = "http://127.0.0.1:5000/";
const rightContainer = document.querySelector(".container-right");
const mainTable = document.querySelector(".main-table");

async function getLedgerResources(userID){
	var returnedData;

	fetch(BASE + "ledger/" + userID)
	.then(response => {
	  	if (response.ok) {
	    	returnedData = response.json();
	  	} else {
	    	throw new Error('Error retrieving ledger.');
	  	}
	})
	.then(data => {
	  	console.log(data);
	})
	.catch(error => {
	  	console.log(error);
	  	return;
	});

	console.log(returnedData);

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

	const response_array = await JSON.parse(returnedData);
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
	rightContainer.innerHTML =  `
								<div class="container1">
								  <form class="text" id="transactions">
								    <h1 class="form__title">Transactions: </h1>
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
								      <input type="text" class="form__input" autofocus placeholder=" Amount ${obj.amount} " readonly>
								      <div class="form__input-error-message"></div>
								    </div>
								    <div class="form__input-group">
								      <input type="text" class="form__input" autofocus placeholder=" Description ${obj.description} " readonly>
								      <div class="form__input-error-message"></div>
								    </div>
								    <div class="form__input-group">
								      <input type="text" class="form__input" autofocus placeholder=" Due Date ${obj.due_date} " readonly>
								      <div class="form__input-error-message"></div>
								    </div>
								    <button id="${obj.id}" class="form__button" type="submit"> ${paidButton} </button>
								    <button id="${obj.id}" class="form__button" type="submit"> Delete </button>
								  </form>
								</div>
								`;

}

// async function closeRightContainer(){
// 	rightContainer.innerHTML = "";
// }

async function postTransaction(event){

		{   "transaction_id": <int:transaction id>
            "src_id": <int: src id>
            "dest_id": <int: dest id>
            "src": <str:src full name>,
            "dest": <str:dest full name>,
            "amount": <int:amount>,
            "description": <str:description>
            "due_date": <str:date string in format yyyy-mm-dd>
            "paid": <str:boolean>
        }

	const transaction_ID,
		transaction_SrcID,
		transaction_DestID,
		transaction_Src,
		transaction_Dest,
		transaction_Amount,
		transaction_Description,
		transaction_DueDate,
		transaction_Paid;




	fetch(BASE + "transaction", {
	  	method: 'POST',
	  	headers: {
	    	'Content-Type': 'application/json'
	  	},
	  	body: JSON.stringify({
	    	transaction_id: transaction_ID,
	    	src_id: transaction_SrcID,
	    	dest_id: transaction_DestID,
	    	src: transaction_Src,
	    	dest: transaction_Dest,
	    	amount: transaction_Amount,
	    	description: transaction_Description,
	    	due_date: transaction_DueDate,
	    	paid: transaction_Paid
	  	})
	})
	.then(response => {
	  	if (response.ok) {
	    	const returnedData = response.json();
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


// 	console.log(returnedData);

// 		// {   "transaction_id": <int:transaction id>
//         //     "src_id": <int: src id>
//         //     "dest_id": <int: dest id>
//         //     "src": <str:src full name>,
//         //     "dest": <str:dest full name>,
//         //     "amount": <int:amount>,
//         //     "description": <str:description>
//         //     "due_date": <str:date string in format yyyy-mm-dd>
//         //     "paid": <str:boolean>
//         // }

// }



// async function patchTransaction(event){
// 	const transaction_Paid;


// 	fetch(BASE + "transaction/" + transactionID, {
// 		method: 'PATCH',
// 		headers: {
// 			'Content-Type': 'application/json'
// 		},
// 		body: JSON.stringify({
// 			paid: transaction_Paid,
// 		})
// 	})
// 	.then(response => {
// 		if (response.ok) {
// 			const returnedData = response;
// 		} else {
// 			throw new Error('Request failed.');
// 		}
// 	})
// 	.catch(error => {
// 		console.log(error);
// 	});

// 	console.log({message: returnedData});


// }


// async function deleteTransaction(event){
// 	fetch(BASE + "transaction/" + transactionID, {
// 	method: 'DELETE',
// 	headers: {
// 		'Content-Type': 'application/json'
// 		}
// 	})
// 	.then(response => {
// 		if (response.ok) {
// 			const returnedData = response;
// 		} else {
// 			throw new Error('Request failed.');
// 		}
// 	})
// 	.then(data => {
// 		console.log(data);
// 	})
// 	.catch(error => {
// 		console.log(error);
// 	});

// 	console.log({message: returnedData});
	
// }

getLedgerResources(630);
