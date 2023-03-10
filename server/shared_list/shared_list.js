const BASE = "http://127.0.0.1:5000/";

// Shared List
async function get_lists(household_id){
	const response = await fetch(BASE + "shared_list/" + household_id);
	if (response.ok){
		const response_array = JSON.parse(await response.json());
		console.log(response_array);

		for (let i = 0; i < response_array.length; i++) {
			const obj = JSON.parse(response_array[i]);

			const spanElement = document.createElement("span");
			spanElement.setAttribute("id", obj.id);
			spanElement.innerHTML = `<u><b>List${i+1} Name: ${obj.name}</b></u>`;
			document.getElementById('lists').appendChild(spanElement);
			document.getElementById('lists').appendChild(document.createElement("br"));
			get_list_event(obj.id);
		}
	}else{
		const response_error = await response.json();
		console.log(response_error.error);
	}
}

// async function post_list(household_id){
// 	// body...
// }

async function delete_list(list_id){
	const response = await fetch(`${BASE}list_details/${list_id}`, {method: 'DELETE'});
	const response_error = await response.json();
	console.log(response_error.error);
	location.reload();
}

// async function patch_list(list_id){
// 	// body...
// }

// List Events
async function get_list_event(list_id){
	const response = await fetch(BASE + "list_events/" + list_id);
	if (response.ok){
		const response_array = JSON.parse(await response.json());
		console.log(response_array);

		for (let i = 0; i < response_array.length; i++) {
			const obj = JSON.parse(response_array[i]);

			const spanElement = document.createElement("span");
			spanElement.setAttribute("id", obj.id);
			spanElement.innerHTML = `List Event ${i+1} Name: ${obj.task_name}.<br>` +
			                        `Description: ${obj.description_of_task}.<br>` +
			                        `Checked_off: ${obj.checked_off_by_user == null}.<br>`;
			document.getElementById(list_id).appendChild(document.createElement("br"));
			document.getElementById(list_id).appendChild(spanElement);
		}
	}else{
		const response_error = await response.json();
		console.log(response_error.error);
	}
}

// async function post_list_event(list_id){
// 	// body...
// }

async function delete_list_event(list_event_id){
	const response = await fetch(`${BASE}list_events/${list_event_id}`, {method: 'DELETE'});
	const response_error = await response.json();
	console.log(response_error.error);
	location.reload();
}

// async function patch_list_event(list_event_id){
// 	// body...
// }

// async function put_list_event(list_event_id){
// 	// body...	
// }
