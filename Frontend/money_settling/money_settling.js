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


}



	fetch('https://example.com/api/endpoint', {
		method: 'PATCH',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			key1: value1,
			key2: value2
		})
	})
	.then(response => {
		if (response.ok) {
			return response.json();
		} else {
			throw new Error('Request failed.');
		}
	})
		.catch(error => {
			console.log(error);
		});