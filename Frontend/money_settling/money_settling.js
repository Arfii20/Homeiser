const BASE = "http://127.0.0.1:5000/";

async function getLedgerResources(event){
	userID = 630;

	fetch(BASE + "ledger/" + userID)
	.then(response => {
	  	if (response.ok) {
	    	const returnedData = response.json();
	  	} else {
	    	throw new Error('Error retrieving ledger.');
	  	}
	})
	.then(data => {
	  	console.log(data);
	})
	.catch(error => {
	  	console.log(error);
	});

	console.log(returnedData);

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


async function getTransaction (event) {
	transactionID = 234824;

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

		// {   "transaction_id": <int:transaction id>
        //     "src_id": <int: src id>
        //     "dest_id": <int: dest id>
        //     "src": <str:src full name>,
        //     "dest": <str:dest full name>,
        //     "amount": <int:amount>,
        //     "description": <str:description>
        //     "due_date": <str:date string in format yyyy-mm-dd>
        //     "paid": <str:boolean>
        // }

}


async function postTransaction(event){

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


	console.log(returnedData);

		// {   "transaction_id": <int:transaction id>
        //     "src_id": <int: src id>
        //     "dest_id": <int: dest id>
        //     "src": <str:src full name>,
        //     "dest": <str:dest full name>,
        //     "amount": <int:amount>,
        //     "description": <str:description>
        //     "due_date": <str:date string in format yyyy-mm-dd>
        //     "paid": <str:boolean>
        // }

}



async function patchTransaction(event){
	const transaction_Paid;


	fetch(BASE + "transaction/" + transactionID, {
		method: 'PATCH',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			paid: transaction_Paid,
		})
	})
	.then(response => {
		if (response.ok) {
			const returnedData = response;
		} else {
			throw new Error('Request failed.');
		}
	})
	.catch(error => {
		console.log(error);
	});

	console.log(returnedData);
	

}


async function deleteTransaction(event){

}


