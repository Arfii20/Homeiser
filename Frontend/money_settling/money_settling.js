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

