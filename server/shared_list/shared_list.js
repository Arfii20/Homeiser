const BASE = "http://127.0.0.1:5000/";

// Shared List
async function get_lists(household_id){
	const response = await fetch(BASE + "shared_list/" + household_id);
	if (response.ok){
		const response_array = JSON.parse(await response.json());
		console.log(response_array);

		for (let i = 0; i < response_array.length; i++) {
			const obj = JSON.parse(response_array[i]);

			// Get the parent element where you want to append the HTML
			const parentElement = document.querySelector('div#lists');

			// Create a new header element
			const headerElement = document.createElement('header');
			headerElement.setAttribute("id", obj.id);

			// Create a new h1 element and set its text content
			const h1Element = document.createElement('h1');
			h1Element.textContent = obj.name;

			// Create a new form element and set its attributes
			const new_task_form_id = 'new-task-form-' + obj.list_id;
			const formElement = document.createElement('form');
			formElement.setAttribute('class', 'new-task-form');
			formElement.setAttribute('id', 'new-task-form');

			// Create a new input element and set its attributes
			const new_task_input_id = 'new-task-input-' + obj.list_id;
			const inputElement = document.createElement('input');
			inputElement.setAttribute('type', 'text');
			inputElement.setAttribute('name', 'new-task-input');
			inputElement.setAttribute('class', 'new-task-input');
			inputElement.setAttribute('id', new_task_input_id);
			inputElement.setAttribute('placeholder', 'What do you have planned?');

			// Create a new input element and set its attributes
			const new_task_submit_id = 'new-task-submit-' + obj.list_id;
			const submitElement = document.createElement('input');
			submitElement.setAttribute('type', 'submit');
			submitElement.setAttribute('class', 'new-task-submit');
			submitElement.setAttribute('id', new_task_submit_id);
			submitElement.setAttribute('value', 'Add task');

			// Append the input elements to the form element
			formElement.appendChild(inputElement);
			formElement.appendChild(submitElement);

			// Append the h1 element and the form element to the header element
			headerElement.appendChild(h1Element);
			headerElement.appendChild(formElement);

			// Append the header element to the parent element
			parentElement.appendChild(headerElement);

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
