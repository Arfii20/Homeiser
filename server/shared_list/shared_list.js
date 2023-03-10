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

			// // Create a new h1 element and set its text content
			// const h1Element = document.createElement('h1');
			// h1Element.textContent = obj.name;


			// Create a new div element and set its ID
			const divElement = document.createElement('div');
			divElement.setAttribute('id', 'list-desc');
			divElement.setAttribute('class', 'list-name');

			// Create a new div element and set its class
			const taskDivElement = document.createElement('div');
			taskDivElement.setAttribute('class', 'list-name');

			// Create a new div element and set its class
			const contentDivElement = document.createElement('div');
			contentDivElement.setAttribute('class', 'content');

			// Create a new input element and set its attributes
			const inputElementH1 = document.createElement('input');
			inputElementH1.setAttribute('type', 'text');
			inputElementH1.setAttribute('class', 'text');
			inputElementH1.setAttribute('value', obj.name);
			inputElementH1.setAttribute('readonly', '');
			inputElementH1.setAttribute('maxlength', '100')

			// Append the input element to the content div element
			contentDivElement.appendChild(inputElementH1);

			// Create a new div element and set its class
			const actionsDivElement = document.createElement('div');
			actionsDivElement.setAttribute('class', 'actions');

			// Create a new button element and set its class and text content
			const editButtonElement = document.createElement('button');
			editButtonElement.setAttribute('class', 'edit');
			editButtonElement.textContent = 'Edit';

			// Create a new button element and set its class and text content
			const deleteButtonElement = document.createElement('button');
			deleteButtonElement.setAttribute('class', 'delete');
			deleteButtonElement.textContent = 'Delete';

			// Append the button elements to the actions div element
			actionsDivElement.appendChild(editButtonElement);
			actionsDivElement.appendChild(deleteButtonElement);

			// Append the content and actions div elements to the task div element
			taskDivElement.appendChild(contentDivElement);
			taskDivElement.appendChild(actionsDivElement);

			// Append the task div element to the tasks div element
			divElement.appendChild(taskDivElement);

			// Append the h2 and tasks div elements to the section element
			headerElement.appendChild(divElement);

			// Create a horizontal line element
			const hrElement = document.createElement('hr');
			hrElement.className = 'hr-element';

			// Create a new form element and set its attributes
			const new_task_form_id = 'new-task-form-' + obj.list_id;
			const formElement = document.createElement('form');
			formElement.setAttribute('class', 'new-task-form');
			formElement.setAttribute('id', new_task_form_id);

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

			// Create a new h2 element and set its text content
			const h2Element = document.createElement('h2');
			h2Element.textContent = 'Tasks';

			// Append the input elements to the form element
			formElement.appendChild(inputElement);
			formElement.appendChild(submitElement);

			// Append the form element to the header element
			headerElement.appendChild(formElement);
			headerElement.appendChild(h2Element);

			// Append the header element to the parent element
			parentElement.appendChild(headerElement);

			get_list_event(obj.id);

			parentElement.appendChild(hrElement);

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

			const parentElement = document.getElementById(list_id);

			// Create a new div element and set its ID
			const divElement = document.createElement('div');
			divElement.setAttribute('id', 'tasks');
			divElement.setAttribute('class', 'task-list');

			// Create a new div element and set its class
			const taskDivElement = document.createElement('div');
			taskDivElement.setAttribute('class', 'task');
			taskDivElement.setAttribute('id', obj.id);
			taskDivElement.setAttribute('data-added-user-id', obj.added_user_id);
			taskDivElement.setAttribute('data-checked-off-by-user', obj.checked_off_by_user);

			// Create a new div element and set its class
			const contentDivElement = document.createElement('div');
			contentDivElement.setAttribute('class', 'content');

			// Create a new input element and set its attributes
			const inputElement = document.createElement('input');
			inputElement.setAttribute('type', 'text');
			inputElement.setAttribute('class', 'text');
			inputElement.setAttribute('value', obj.task_name);
			inputElement.setAttribute('readonly', '');
			inputElement.setAttribute('maxlength', '100');

			// Cheate a new input element for showing description
			const inputElementName = document.createElement('input');
			inputElementName.setAttribute('type', 'text');
			inputElementName.setAttribute('class', 'text');
			inputElementName.setAttribute('value', obj.description_of_task);
			inputElementName.setAttribute('readonly', '');
			inputElementName.setAttribute('maxlength', '100');

			// Append the input element to the content div element
			contentDivElement.appendChild(inputElement);
			contentDivElement.appendChild(inputElementName);

			// Create a new div element and set its class
			const actionsDivElement = document.createElement('div');
			actionsDivElement.setAttribute('class', 'actions');

			// Create a new button element and set its class and text content
			const editButtonElement = document.createElement('button');
			editButtonElement.setAttribute('class', 'edit');
			editButtonElement.textContent = 'Edit';

			// Create a new button element and set its class and text content
			const deleteButtonElement = document.createElement('button');
			deleteButtonElement.setAttribute('class', 'delete');
			deleteButtonElement.textContent = 'Delete';

			// Create a new checkbox element and set its class and text content
			const checkboxInput = document.createElement('input');
			checkboxInput.type = 'checkbox';
			checkboxInput.className = 'checkbox';

			// Append the button elements to the actions div element
			actionsDivElement.appendChild(editButtonElement);
			actionsDivElement.appendChild(deleteButtonElement);
			actionsDivElement.appendChild(checkboxInput);

			// Append the content and actions div elements to the task div element
			taskDivElement.appendChild(contentDivElement);
			taskDivElement.appendChild(actionsDivElement);

			// Append the task div element to the tasks div element
			divElement.appendChild(taskDivElement);

			// Append the h2 and tasks div elements to the section element
			parentElement.appendChild(divElement);

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
