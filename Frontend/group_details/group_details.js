const BASE = "http://127.0.0.1:5000/";
const container = document.querySelector(".container");
const logged_in_hrefs = document.querySelector(".if-logged-in");
const not_logged_in_hrefs = document.querySelector(".if-not-logged-in");
const hamburger = document.querySelector(".hamburger");

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

const user_id = localStorage.getItem("user_id");
const house_id = localStorage.getItem("house_id");
// const user_id = 630;
// const house_id = 620;
let prev_values = {};

if (user_id === null || user_id === undefined || user_id === "undefined") {
  not_logged_in_hrefs.style.display = "";
  logged_in_hrefs.style.display = "none";
  hamburger.style.display = "none";
  window.location.href = "../login.html";
}
if (house_id === null || house_id === "undefined" || house_id === "undefined") {
  window.location.href = "../group.html";
}

not_logged_in_hrefs.style.display = "none";
logged_in_hrefs.style.display = "";
hamburger.style.display = "";

getDetails(user_id);

async function getDetails(user_id){
	try{
		const response = await fetch(BASE + "group_details/" + house_id);
		
		if (response.ok) {
			console.log({message: "Profile Received"});
			const obj = await response.json();
			let stringToBeAdded = "";
			stringToBeAdded += `<form class="form">
							        <h1 class="form__title" style="color:#a220a4;">Details</h1>
							        <div class="form__message form__message--error"></div>
							        <div class="form__input-group">
							            <input type="text" id="first_name" class="form__input" value="Group Name: ${obj.house_name}" readonly>
							            <div class="form__input-error-message"></div>
							        </div>
							        <div class="detailsTable">
										      <table class="main-table" style="width:100%">
										      		<thead class="fixed">
					                				<th class="header">
					                  					Members
					                				</th>
					                		</thead>`

			for (let i = 0; i < obj.users.length; i++){
				await Promise.resolve(); 
				stringToBeAdded += `<tbody id="data-output">
										          	<tr>
											              <td class="table-data"> ${obj.users[i]} </td>
											         	<tr>
										        </tbody>`;
			}

			stringToBeAdded += `</table>
											      </div>
											      <button class="form__button" type="submit" onclick=leaveGroup(event) style="margin-top:1rem;">Leave Group</button>
											    </form>`;
			container.innerHTML = stringToBeAdded;
		}
		else {
	    	throw new Error('Error retrieving ledger.');
	    	return;
		}
	}
	catch (error) {
    console.error(error);
    if (error.message === 'Failed to fetch') {
        createMockUpHTMLofGroup();
    }
  }
}

async function leaveGroup(event){
	event.preventDefault();

	fetch(BASE + "transaction/" + user_id, {
	method: 'DELETE',
	headers: {
		'Content-Type': 'application/json'
		}
	})
	.then(response => {
		if (response.ok) {
			document.cookie = "house_id=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=../";
			window.location.href = "../group.html"
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
	
}

function createMockUpHTMLofGroup(){
	container.innerHTML = `<form class="form">
							        <h1 class="form__title" style="color:#a220a4;">Group Details</h1>
							        <div class="form__message form__message--error"></div>
							        <div class="form__input-group">
							            <input type="text" id="first_name" class="form__input" placeholder="Group Name: Mockup Group" readonly="">
							            <div class="form__input-error-message"></div>
							        </div>
							        <div class="detailsTable">
										      <table class="main-table" style="width:100%">
										      		<thead class="fixed">
					                				<tr><th class="header">
					                  					Members
					                				</th>
					                		</tr></thead><tbody id="data-output">
										          	<tr>
											              <td class="table-data"> Mockup User 1 </td>
											         	</tr><tr>
										        </tr></tbody><tbody id="data-output">
										          	<tr>
											              <td class="table-data"> Mockup User 2 </td>
											         	</tr><tr>
										        </tr></tbody><tbody id="data-output">
										          	<tr>
											              <td class="table-data"> Mockup User 3 </td>
											         	</tr><tr>
										        </tr></tbody><tbody id="data-output">
										          	<tr>
											              <td class="table-data"> Mockup User 4 </td>
											         	</tr><tr>
										        </tr></tbody></table>
											      </div>
											      <button class="form__button">Leave Group</button>
											    </form>`;
}



function logout(){
	// Get all cookies and split them into an array
	localStorage.clear();
  
	console.log("Local Storage cleared");
	window.location.href = "login.html";
}
