const BASE = "http://127.0.0.1:5000/";

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

	const mainTable = document.querySelector(".main-table");
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

		var paid;
		if (obj.paid){
			paid = "Yes"
		}
		else{
			paid = "No"
		}

		mainTable.innerHTML += `
				              <tbody id="data-output">
				                <td class="table-data"> ${obj.src} --> ${obj.dest}
				                </td>
				                <td class="table-data">
				                  ${obj.due_date}
				                </td>
				                <td class="table-data">
				                  £20.00
				                </td>
				              </tbody>
				              `
		// List of
	    // {   "transaction_id": <int:transaction id>
        //     "src_id": <int: src id>
        //     "src_id": <int: dest id>
        //     "src": <str:src full name>,
        //     "dest": <str:dest full name>,
        //     "amount": <int:amount>,
        //     "description": <str:description>
        //     "due_date": <str:date string in format yyyy-mm-dd>
        //     "paid": <str:boolean>
        // }
	}

}


// async function getTransaction (event) {
// 	transactionID = 234824;

// 	fetch(BASE + "transaction/" + transactionID)
// 	.then(response => {
// 	  	if (response.ok) {
// 	    	const returnedData = response.json();
// 	  	} else {
// 	    	throw new Error('Error retrieving transaction.');
// 	  	}
// 	})
// 	.then(data => {
// 	  	console.log(data);
// 	})
// 	.catch(error => {
// 	  	console.log(error);
// 	});

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


// async function postTransaction(event){

// 	const transaction_ID,
// 		transaction_SrcID,
// 		transaction_DestID,
// 		transaction_Src,
// 		transaction_Dest,
// 		transaction_Amount,
// 		transaction_Description,
// 		transaction_DueDate,
// 		transaction_Paid;




// 	fetch(BASE + "transaction", {
// 	  	method: 'POST',
// 	  	headers: {
// 	    	'Content-Type': 'application/json'
// 	  	},
// 	  	body: JSON.stringify({
// 	    	transaction_id: transaction_ID,
// 	    	src_id: transaction_SrcID,
// 	    	dest_id: transaction_DestID,
// 	    	src: transaction_Src,
// 	    	dest: transaction_Dest,
// 	    	amount: transaction_Amount,
// 	    	description: transaction_Description,
// 	    	due_date: transaction_DueDate,
// 	    	paid: transaction_Paid
// 	  	})
// 	})
// 	.then(response => {
// 	  	if (response.ok) {
// 	    	const returnedData = response.json();
// 	  	} else {
// 	    	throw new Error('Request failed.');
// 	  	}
// 	})
// 	.then(data => {
// 	  	console.log(data);
// 	})
// 	.catch(error => {
// 	  	console.log(error);
// 	});


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
