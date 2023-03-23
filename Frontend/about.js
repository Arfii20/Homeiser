const BASE = "http://127.0.0.1:5000/";
const logged_in_hrefs = document.querySelector(".if-logged-in");
const not_logged_in_hrefs = document.querySelector(".if-not-logged-in");
const hamburger = document.querySelector(".hamburger");

const user_id = localStorage.getItem("user_id");
const house_id = localStorage.getItem("house_id");
// const user_id = 630;
// const house_id = 620;

if (user_id === null || user_id === undefined || user_id === "undefined") {
  not_logged_in_hrefs.style.display = "";
  logged_in_hrefs.style.display = "none";
  hamburger.style.display = "none";
}
else{
	not_logged_in_hrefs.style.display = "none";
	logged_in_hrefs.style.display = "";
	hamburger.style.display = "";
}

function logout(){
	// Get all cookies and split them into an array
	localStorage.clear();
  
	console.log("Local Storage cleared");
	window.location.href = "login.html";
}