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
			const inputElementH1Id = 'input-element-h1-' + obj.id;
			const inputElementH1 = document.createElement('input');
			inputElementH1.setAttribute('type', 'text');
			inputElementH1.setAttribute('class', 'text');
			inputElementH1.setAttribute('id', inputElementH1Id);
			inputElementH1.setAttribute('value', obj.name);
			inputElementH1.setAttribute('readonly', '');
			inputElementH1.setAttribute('maxlength', '100')

			// Append the input element to the content div element
			contentDivElement.appendChild(inputElementH1);

			// Create a new div element and set its class
			const actionsDivElement = document.createElement('div');
			actionsDivElement.setAttribute('class', 'actions');

			// Create a new button element and set its class and text content
			const editButtonId = 'edit-button-list-' + obj.id;
			const editButtonElement = document.createElement('button');
			editButtonElement.setAttribute('class', 'edit');
			editButtonElement.setAttribute('id', editButtonId);
			editButtonElement.textContent = 'Edit';
			editButtonElement.setAttribute('onclick', 'patch_list(event)');

			// Create a new button element and set its class and text content
			const deleteButtonElement = document.createElement('button');
			deleteButtonElement.setAttribute('class', 'delete');
			deleteButtonElement.textContent = 'Delete';
			deleteButtonElement.setAttribute('onclick', 'delete_list(event)');

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
			const hrID = 'hr-' + obj.id
			const hrElement = document.createElement('hr');
			hrElement.className = 'hr-element';
			hrElement.setAttribute('id', hrID)

			// Create a new form element and set its attributes
			const new_task_form_id = 'new-task-form-' + obj.id;
			const formElement = document.createElement('form');
			formElement.setAttribute('class', 'new-task-form');
			formElement.setAttribute('id', new_task_form_id);
			formElement.setAttribute('onsubmit', 'post_list_event(event)')

			// Create a new input element and set its attributes
			const new_task_input_id = 'new-task-input-' + obj.id;
			const inputElement = document.createElement('input');
			inputElement.setAttribute('type', 'text');
			inputElement.setAttribute('name', 'new-task-input');
			inputElement.setAttribute('class', 'new-task-input');
			inputElement.setAttribute('id', new_task_input_id);
			inputElement.setAttribute('placeholder', 'Enter new task name');
			inputElement.setAttribute('maxlength', '100');

			// Create a new input element and set its attributes
			const new_task_description_id = 'new-task-description-' + obj.id;
			const inputElementDescription = document.createElement('input');
			inputElementDescription.setAttribute('type', 'text');
			inputElementDescription.setAttribute('name', 'new-task-description');
			inputElementDescription.setAttribute('class', 'new-task-description');
			inputElementDescription.setAttribute('id', new_task_description_id);
			inputElementDescription.setAttribute('placeholder', 'Enter new task description');
			inputElementDescription.setAttribute('maxlength', '100');

			// Create a new input element and set its attributes
			const new_task_submit_id = 'new-task-submit-' + obj.id;
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
			formElement.appendChild(inputElementDescription);
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

async function post_list(event){
	event.preventDefault();
	house_id = 620;
	const closestForm = event.target.closest('form');

	const inputValue = closestForm.querySelector('.new-list-input').value;

	if (!inputValue){
		alert("NAME of list cannot be empty!");
	}
	else {
		const url = BASE + "shared_list/" + house_id;
		const data = new URLSearchParams();

		data.append('name', inputValue.replace(/'/g, "\\'"));

		await fetch(url, {
		  method: 'POST',
		  body: data,
		  headers: {
		    'Content-Type': 'application/x-www-form-urlencoded'
		  }
		}).then(response => response.json())
		  .then(data => console.log(data))
		  .catch(error => console.error(error));

		const children = document.querySelectorAll('div#lists');
		children.forEach(function(child) {
			child.remove();
		})

		console.clear();
		location.reload()
		closestForm.reset();
	}
}

async function delete_list(event){
	event.preventDefault();
	// handle form submission
	const closestHeader = event.target.closest('header');
	const listID = closestHeader.id;
	closestHeader.remove();

	const closestHr = document.querySelector('hr#hr-' + listID);
	closestHr.remove();

	const response = await fetch(`${BASE}list_details/${listID}`, {method: 'DELETE'});
	const response_error = await response.json();
	console.log(response_error);
}

async function patch_list(event){
	const closestHeader = event.target.closest('header');
	const listID = closestHeader.id;

	const editButtonElement = document.querySelector('#edit-button-list-' + listID);
	const inputElement = document.querySelector('#input-element-h1-' + listID);
	const inputValue = inputElement.value;

	if (editButtonElement.innerText.toLowerCase() == "edit") {
		editButtonElement.innerText = "Save";
		inputElement.removeAttribute("readonly");		
		inputElement.focus();
		inputElement.setSelectionRange(0, inputElement.value.length);
		inputElement.setAttribute('data-previous-data', inputValue);
		

	}
	else {
		editButtonElement.innerText = "Edit";
		inputElement.setAttribute("readonly", "readonly");

		if (!inputValue){
			alert("LIST NAME cannot be empty!");
		}
		else{
		  	const url = BASE + "list_details/" + listID;
			const data = new URLSearchParams();

			data.append('new_name', inputValue.replace(/'/g, "\\'"));

			const response = await fetch(url, {method: 'PATCH',
												body: data,
												headers: {
												'Content-Type': 'application/x-www-form-urlencoded'
												}
											});
			if (!response.ok){
				alert("List name already exists!");
				inputElement.value = inputElement.getAttribute('data-previous-data');
				console.log(await response.json());
			}
			else {
				console.log(await response.json());
			}
		}
	}
}

// All List Event methods start from here
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
			taskDivElement.setAttribute('data-list_id', obj.list);
			taskDivElement.setAttribute('data-added-user-id', obj.added_user_id);
			taskDivElement.setAttribute('data-checked-off-by-user', obj.checked_off_by_user);

			// Create a new div element and set its class
			const contentDivElement = document.createElement('div');
			contentDivElement.setAttribute('class', 'content');

			// Create a new input element and set its attributes
			const inputId = 'input-' + obj.id;
			const inputElement = document.createElement('input');
			inputElement.setAttribute('type', 'text');
			inputElement.setAttribute('class', 'text');
			inputElement.setAttribute('id', inputId)
			inputElement.setAttribute('value', obj.task_name);
			inputElement.setAttribute('readonly', '');
			inputElement.setAttribute('maxlength', '100');

			// Cheate a new input element for showing description
			const inputNameId = 'input-name-' + obj.id;
			const inputElementName = document.createElement('input');
			inputElementName.setAttribute('type', 'text');
			inputElementName.setAttribute('class', 'text');
			inputElementName.setAttribute('id', inputNameId)
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
			const editButtonId = 'edit-' + obj.id;
			const editButtonElement = document.createElement('button');
			editButtonElement.setAttribute('class', 'edit');
			editButtonElement.textContent = 'Edit';
			editButtonElement.setAttribute('id', editButtonId)
			editButtonElement.setAttribute('onclick', 'put_list_event(event)')

			// Create a new button element and set its class and text content
			const deleteButtonElement = document.createElement('button');
			deleteButtonElement.setAttribute('class', 'delete');
			deleteButtonElement.textContent = 'Delete';
			deleteButtonElement.setAttribute('onclick', 'delete_list_event(event)')

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

async function post_list_event(event) {
	event.preventDefault();
	// handle form submission
	const closestForm = event.target.closest('form');
	const closestHeader = closestForm.closest('header');
	const headerId = closestHeader.id;

	const inputValue = closestForm.querySelector('#new-task-input-' + headerId).value;
	const inputDescriptionValue = closestForm.querySelector('#new-task-description-' + headerId).value;

	const added_user = 630;

	if (!inputValue && !inputDescriptionValue){
		alert("NAME and DESCRIPTION cannot be empty!")
	}
	else if (!inputValue){
		alert("NAME cannot be empty!")
	}
	else if (!inputDescriptionValue){
		alert("DESCRIPTION cannot be empty!")
	}
	else{
	  	const url = BASE + "list_events/" + headerId;
		const data = new URLSearchParams();

		data.append('task_name', inputValue.replace(/'/g, "\\'"));
		data.append('description_of_task', inputDescriptionValue.replace(/'/g, "\\'"));
		data.append('added_user_id', parseInt(added_user));

		await fetch(url, {
		  method: 'POST',
		  body: data,
		  headers: {
		    'Content-Type': 'application/x-www-form-urlencoded'
		  }
		}).then(response => response.json())
		  .then(data => console.log(data))
		  .catch(error => console.error(error));

		const header = document.getElementById(headerId);
		const children = header.querySelectorAll('.task-list');
		children.forEach(function(child) {
			child.remove();
		})

		get_list_event(headerId)
		closestForm.reset();
	}
}

async function delete_list_event(event){
	const closestDiv = event.target.closest('div');
  	const listEventID = closestDiv.parentNode.id;
  	closestDiv.parentNode.remove();

	const response = await fetch(`${BASE}list_event_details/${listEventID}`, {method: 'DELETE'});
	const response_error = await response.json();
	console.log(response_error);
}

// async function patch_list_event(event){
// }

async function put_list_event(event){
	const closestDiv = event.target.closest('div');
  	const listEventID = closestDiv.parentNode.id;

	const editButtonElement = document.querySelector('#edit-' + listEventID);
	const inputElement = document.querySelector('#input-' + listEventID);
	const inputName = document.querySelector('#input-name-' + listEventID);

	if (editButtonElement.innerText.toLowerCase() == "edit") {
		editButtonElement.innerText = "Save";
		inputName.removeAttribute("readonly");
		inputElement.removeAttribute("readonly");		
		inputElement.focus();
		inputElement.setSelectionRange(0, inputElement.value.length);
		

	}
	else {
		editButtonElement.innerText = "Edit";

		inputElement.setAttribute("readonly", "readonly");
		inputName.setAttribute("readonly", "readonly");
		const inputValue = inputElement.value;
		const inputDescriptionValue = inputName.value;

		if (!inputValue && !inputDescriptionValue){
			alert("NAME and DESCRIPTION cannot be empty!")
		}
		else if (!inputValue){
			alert("NAME cannot be empty!")
		}
		else if (!inputDescriptionValue){
			alert("DESCRIPTION cannot be empty!")
		}
		else{
		  	const url = BASE + "list_event_details/" + listEventID;
			const data = new URLSearchParams();

			data.append('new_task', inputValue.replace(/'/g, "\\'"));
			data.append('new_description', inputDescriptionValue.replace(/'/g, "\\'"));

			await fetch(url, {
			  method: 'PUT',
			  body: data,
			  headers: {
			    'Content-Type': 'application/x-www-form-urlencoded'
			  }
			}).then(response => response.json())
			  .then(data => console.log(data))
			  .catch(error => console.error(error));
		}
	}
}
