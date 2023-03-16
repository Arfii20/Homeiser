const calendar = document.querySelector(".calendar"),
  date = document.querySelector(".date"),
  daysContainer = document.querySelector(".days"),
  prev = document.querySelector(".prev"),
  next = document.querySelector(".next"),
  todayBtn = document.querySelector(".today-btn"),
  gotoBtn = document.querySelector(".goto-btn"),
  dateInput = document.querySelector(".date-input"),
  eventDay = document.querySelector(".event-day"),
  eventDate = document.querySelector(".event-date"),
  eventsContainer = document.querySelector(".events"),
  addEventBtn = document.querySelector(".add-event"),
  addEventWrapper = document.querySelector(".add-event-wrapper "),
  addEventCloseBtn = document.querySelector(".close "),
  addEventTitle = document.querySelector(".event-name "),
  addEventFrom = document.querySelector(".event-time-from "),
  addEventTo = document.querySelector(".event-time-to "),
  addEventNotes = document.querySelector(".additional-notes "),
  addEventLocation= document.querySelector(".event-location "),
  addEventTaggedUsers = document.querySelector(".tagged-users "),
  // addEventAddedBy = document.querySelector(".added-by "),
  addEventSubmit = document.querySelector(".add-event-btn "),
  addEventTagged = document.querySelector(".event-tagged ");

  BASE = "http://127.0.0.1:5000/";

let today = new Date();
let activeDay;
let month = today.getMonth();
let year = today.getFullYear();

const months = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
];

const eventsArr = [];
// getEvents();
get_calendarEvent(620);
console.log(eventsArr);

//function to add days in days with class day and prev-date next-date on previous month and next month days and active on today
function initCalendar() {
  // to get prev month days and current month all days, and remeber next mont days 
  const firstDay = new Date(year, month, 1);
  const lastDay = new Date(year, month + 1, 0);
  const prevLastDay = new Date(year, month, 0);
  const prevDays = prevLastDay.getDate();
  const lastDate = lastDay.getDate();
  const day = firstDay.getDay();
  const nextDays = 7 - lastDay.getDay() - 1;

  //update date at top of calender 
  date.innerHTML = months[month] + " " + year;

  //adding days on dom 

  let days = "";

  //prev month days 

  for (let x = day; x > 0; x--) {
    days += `<div class="day prev-date">${prevDays - x + 1}</div>`;
  }

  //current month days 

  for (let i = 1; i <= lastDate; i++) {
    let event = false;
    eventsArr.forEach((eventObj) => {
      //if event found, also add event class 
      if (
        eventObj.day === i &&
        eventObj.month === month + 1 &&
        eventObj.year === year
      ) {
        event = true;
      }
    });
    //if say is today, add class today
    if (
      i === new Date().getDate() &&
      year === new Date().getFullYear() &&
      month === new Date().getMonth()
    ) {
      activeDay = i;
      getActiveDay(i);
      updateEvents(i);
      if (event) {
        //check if event is present on that day
        days += `<div class="day today active event">${i}</div>`;
      } else {
        days += `<div class="day today active">${i}</div>`;
      }
      //add remaining as it is 
    } else {
      if (event) {
        days += `<div class="day event">${i}</div>`;
      } else {
        days += `<div class="day ">${i}</div>`;
      }
    }
  }

  //next month days 

  for (let j = 1; j <= nextDays; j++) {
    days += `<div class="day next-date">${j}</div>`;
  }
  daysContainer.innerHTML = days;
  addListner();
}

//function to add month and year on prev and next button
function prevMonth() {
  month--;
  if (month < 0) {
    month = 11;
    year--;
  }
  initCalendar();
}

//next month 
function nextMonth() {
  month++;
  if (month > 11) {
    month = 0;
    year++;
  }
  initCalendar();
}

//add event listener on prev and next month 
prev.addEventListener("click", prevMonth);
next.addEventListener("click", nextMonth);

initCalendar();

//function to add active on day
function addListner() {
  const days = document.querySelectorAll(".day");
  days.forEach((day) => {
    day.addEventListener("click", (e) => {
      getActiveDay(e.target.innerHTML);
      updateEvents(Number(e.target.innerHTML));
      activeDay = Number(e.target.innerHTML);
      //remove active from already active day 
      days.forEach((day) => {
        day.classList.remove("active");
      });
      //if clicked prev-date or next-date switch to that month and add active 
      if (e.target.classList.contains("prev-date")) {
        prevMonth();
        //add active to clicked day afte month is change
        setTimeout(() => {
          //add active where no prev-date or next-date
          // select all days of taht month 
          const days = document.querySelectorAll(".day");

          //after going to prev month, add active to date clicked 
          days.forEach((day) => {
            if (
              !day.classList.contains("prev-date") &&
              day.innerHTML === e.target.innerHTML
            ) {
              day.classList.add("active");
            }
          });
        }, 100);
      } else if (e.target.classList.contains("next-date")) {
        nextMonth();
        //add active to clicked day after month is changed
        setTimeout(() => {
          const days = document.querySelectorAll(".day");
          days.forEach((day) => {
            if (
              !day.classList.contains("next-date") &&
              day.innerHTML === e.target.innerHTML
            ) {
              //add active to date clicked on next month 
              day.classList.add("active");
            }
          });
        }, 100);
      } else {
        e.target.classList.add("active");
      }
    });
  });
}

//adding functionality to today button to go to today's date 
todayBtn.addEventListener("click", () => {
  today = new Date();
  month = today.getMonth();
  year = today.getFullYear();
  initCalendar();
});

//validation and functionality to input of date to go to
dateInput.addEventListener("input", (e) => {
  dateInput.value = dateInput.value.replace(/[^0-9/]/g, "");
  if (dateInput.value.length === 2) {
    // add a slash if 2 numbers entered
    dateInput.value += "/";
  }
  if (dateInput.value.length > 7) {
    //don't allow more than 7 characters
    dateInput.value = dateInput.value.slice(0, 7);
  }
  //if backspace pressed
  if (e.inputType === "deleteContentBackward") {
    if (dateInput.value.length === 3) {
      dateInput.value = dateInput.value.slice(0, 2);
    }
  }
});

gotoBtn.addEventListener("click", gotoDate);

//fucntion to go to date entered 
function gotoDate() {
  console.log("here");
  const dateArr = dateInput.value.split("/");
  //date validation
  if (dateArr.length === 2) {
    if (dateArr[0] > 0 && dateArr[0] < 13 && dateArr[1].length === 4) {
      month = dateArr[0] - 1;
      year = dateArr[1];
      initCalendar();
      return;
    }
  }
  //invalid date entered
  alert("Invalid Date");
}

//function get active day day name and date and update eventday eventdate
function getActiveDay(date) {
  const day = new Date(year, month, date);
  const dayName = day.toString().split(" ")[0];
  eventDay.innerHTML = dayName;
  eventDate.innerHTML = date + " " + months[month] + " " + year;
}

//function update events when a day is active and show events of that day
function updateEvents(date) {
  let events = "";
  eventsArr.forEach((event) => {
    //get events of active day only 
    if (
      date === event.day &&
      month + 1 === event.month &&
      year === event.year
    ) {
      //show event on document 
      event.events.forEach((event) => {
        events += `<div class="events-buttons">
            <div class="event" id="${event.id}">
                <div class="title">
                  <i class="fas fa-circle"></i>
                  <h3 class="event-title">${event.title}</h3>
                </div>
                <div class="event-time">
                  <span class="event-time">${event.time}</span>
                </div>
                <div class="event-notes">
                  <span class="event-notes">Description : ${event.notes}</span>
                </div>
                <div class="event-location">
                  <span class="event-location">Location : ${event.location}</span>
                </div>
                <div class="event-tagged">
                  <span class="event-tagged">Users involved : ${event.tagged}</span>
                </div>
            </div>
            <div class="event-buttons">
                <button class="edit-delete-button" onclick=deleteEvent(event)>Delete</button>
                <button class="edit-delete-button">Edit</button>
            </div>
        </div>`;
      });
    }
  });
  //if nothing found 
  if (events === "") {
    events = `<div class="no-event">
            <h3>No Events</h3>
        </div>`;
  }
  eventsContainer.innerHTML = events;
}

//function to add event
addEventBtn.addEventListener("click", () => {
  addEventWrapper.classList.toggle("active");
});

addEventCloseBtn.addEventListener("click", () => {
  addEventWrapper.classList.remove("active");
});

document.addEventListener("click", (e) => {
  if (e.target !== addEventBtn && !addEventWrapper.contains(e.target)) {
    addEventWrapper.classList.remove("active");
  }
});

//allow 50 chars in eventtitle
addEventTitle.addEventListener("input", (e) => {
  addEventTitle.value = addEventTitle.value.slice(0, 60);
});

//allow only time in eventtime from and to
addEventFrom.addEventListener("input", (e) => {
  addEventFrom.value = addEventFrom.value.replace(/[^0-9:]/g, "");
  if (addEventFrom.value.length === 2) {
    addEventFrom.value += ":";
  }
  if (addEventFrom.value.length > 5) {
    addEventFrom.value = addEventFrom.value.slice(0, 5);
  }
});

addEventTo.addEventListener("input", (e) => {
  addEventTo.value = addEventTo.value.replace(/[^0-9:]/g, "");
  if (addEventTo.value.length === 2) {
    addEventTo.value += ":";
  }
  if (addEventTo.value.length > 5) {
    addEventTo.value = addEventTo.value.slice(0, 5);
  }
});

//allow 50 chars in eventLocation
addEventLocation.addEventListener("input", (e) => {
  addEventLocation.value = addEventLocation.value.slice(0, 60);
});

//allow 100 chars in eventNotes
addEventNotes.addEventListener("input", (e) => {
  addEventNotes.value = addEventNotes.value.slice(0, 60);
});

//allow 100 chars in eventNotes
addEventTaggedUsers.addEventListener("input", (e) => {
  addEventTaggedUsers.value = addEventTaggedUsers.value.slice(0, 60);
});

//function to edit event
editEventBtn.editEventListener("click", () => {
  editEventWrapper.classList.toggle("active");
});

editEventCloseBtn.editEventListener("click", () => {
  editEventWrapper.classList.remove("active");
});

document.editEventListener("click", (e) => {
  if (e.target !== editEventBtn && !editEventWrapper.contains(e.target)) {
    editEventWrapper.classList.remove("active");
  }
});

//allow 50 chars in eventtitle
editEventTitle.editEventListener("input", (e) => {
  editEventTitle.value = editEventTitle.value.slice(0, 60);
});

//allow only time in eventtime from and to
editEventFrom.editEventListener("input", (e) => {
  editEventFrom.value = editEventFrom.value.replace(/[^0-9:]/g, "");
  if (editEventFrom.value.length === 2) {
    editEventFrom.value += ":";
  }
  if (editEventFrom.value.length > 5) {
    editEventFrom.value = editEventFrom.value.slice(0, 5);
  }
});

editEventTo.editEventListener("input", (e) => {
  editEventTo.value = editEventTo.value.replace(/[^0-9:]/g, "");
  if (editEventTo.value.length === 2) {
    editEventTo.value += ":";
  }
  if (editEventTo.value.length > 5) {
    editEventTo.value = editEventTo.value.slice(0, 5);
  }
});

//allow 50 chars in eventLocation
editEventLocation.editEventListener("input", (e) => {
  editEventLocation.value = editEventLocation.value.slice(0, 60);
});

//allow 100 chars in eventNotes
editEventNotes.editEventListener("input", (e) => {
  editEventNotes.value = editEventNotes.value.slice(0, 60);
});

//allow 100 chars in eventNotes
editEventTaggedUsers.editEventListener("input", (e) => {
  editEventTaggedUsers.value = editEventTaggedUsers.value.slice(0, 60);
});


function convertTime(time) {
  //convert time to 24 hour format
  let timeArr = time.split(":");
  let timeHour = timeArr[0];
  let timeMin = timeArr[1];
  let timeFormat = timeHour >= 12 ? "PM" : "AM";
  timeHour = timeHour % 12 || 12;
  time = timeHour + ":" + timeMin + " " + timeFormat;
  return time;
}

//function to DELETE event when clicked on event
async function deleteEvent(event){
  // if (e.target.classList.contains("event")) {
  console.log(event);
  const eventID = event.target.parentNode.previousElementSibling.id;
  // if (confirm("Are you sure you want to delete this event?")) {
  //get event title of event, then search in array and delete 
      
  const response = await fetch(`${BASE}calendar_event/${eventID}`, {method: 'DELETE'});

  if (response.ok){
    eventsArr.forEach((event) => {
      if (
        event.day === activeDay &&
        event.month === month + 1 &&
        event.year === year
      ) {
        event.events.forEach((item, index) => {
          if (item.id == eventID) {
            event.events.splice(index, 1);
          }
        });
        //if no events left in a day then remove that day from eventsArr
        if (event.events.length === 0) {
          eventsArr.splice(eventsArr.indexOf(event), 1);
          //remove event class from day
          const activeDayEl = document.querySelector(".day.active");
          if (activeDayEl.classList.contains("event")) {
            activeDayEl.classList.remove("event");
          }
        }
      }
    });
  }
  const response_error = await response.json();
  console.log(response_error);
  //after removing from array , update event
  initCalendar();
  updateEvents(activeDay);
}
  // }
// });

//function to POST events to the database
addEventSubmit.addEventListener("click", async () => {
  const eventTitle = addEventTitle.value;
  const eventTimeFrom = addEventFrom.value;
  const eventTimeTo = addEventTo.value;
  const eventNotes = addEventNotes.value;
  const eventLocation = addEventLocation.value;
  const eventTaggedUsers = addEventTaggedUsers.value;
  const eventAddedBy = 630;

  if (eventTitle === "" || eventTimeFrom === "" || eventTimeTo === "" || eventNotes === "" || eventLocation === "" || eventTaggedUsers === ""){
    alert("Please fill all the fields");
    return;
  }

  //check correct time format 24 hour
  const timeFromArr = eventTimeFrom.split(":");
  const timeToArr = eventTimeTo.split(":");
  if (
    timeFromArr.length !== 2 ||
    timeToArr.length !== 2 ||
    timeFromArr[0] > 23 ||
    timeFromArr[1] > 59 ||
    timeToArr[0] > 23 ||
    timeToArr[1] > 59
  ) {
    alert("Invalid Time Format");
    return;
  }

  const timeFrom = convertTime(eventTimeFrom);
  const timeTo = convertTime(eventTimeTo);

  console.log(timeFrom);
  console.log(timeTo);

  //check if event is already added
  let eventExist = false;
  eventsArr.forEach((event) => {
    if (
      event.day === activeDay &&
      event.month === month + 1 &&
      event.year === year
    ) {
      event.events.forEach((event) => {
        if (event.title === eventTitle) {
          eventExist = true;
        }
      });
    }
  });
  if (eventExist) {
    alert("Event already added");
    return;
  }
  
  const house_id = 620;
  const user_id = 630;
  const eventTimeFromConverted = `${year}-${month + 1}-${activeDay} ${eventTimeFrom}:00`;
  const eventTimeToConverted = `${year}-${month + 1}-${activeDay} ${eventTimeTo}:00`;

  const url = BASE + "shared_calendar/" + house_id;
  const data = new URLSearchParams();

  data.append('title_of_event', eventTitle.replace(/'/g, "\\'"));
  data.append('starting_time', eventTimeFromConverted);
  data.append('ending_time', eventTimeToConverted);
  data.append('additional_notes', eventNotes.replace(/'/g, "\\'"));
  data.append('location_of_event', eventLocation.replace(/'/g, "\\'"));
  data.append('tagged_users', eventTaggedUsers.replace(/'/g, "\\'"));
  data.append('added_by', parseInt(user_id));

  const response = await fetch(url, {
                  method: 'POST',
                  body: data,
                  headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                  }
                });

  if (response.ok){
    //remove active from add event form 
    addEventWrapper.classList.remove("active");
    //clear fields 
    addEventTitle.value = "";
    addEventFrom.value = "";
    addEventTo.value = "";
    addEventNotes.value = "";
    addEventLocation.value = "";
    addEventTaggedUsers.value = "";

    get_calendarEvent(house_id);

    //show added event 
    updateEvents(activeDay);
  }else{
    const response_error = await response.json();
    console.log(response_error.error);
  }
});

async function get_calendarEvent(household_id){
  const url = BASE + "get_shared_calendar/" + household_id;
  const data = new URLSearchParams();

  const startDate = '2000-01-01 00:00:00';
  const endDate = '2050-12-31 00:00:00';

  data.append('starting_time', startDate);
  data.append('ending_time', endDate);

  const response = await fetch(url, {
                          method: 'POST',
                          body: data,
                          headers: {
                            'Content-Type': 'application/x-www-form-urlencoded'
                          }
                        })
  if (response.ok){
    eventsArr.length = 0;
    const response_array = JSON.parse(await response.json());

    for (let i = 0; i < response_array.length; i++) {
      const obj = JSON.parse(response_array[i]);

      const eventID= obj.event_id;

      const dateFrom = new Date(obj.starting_time);
      const yearFrom = dateFrom.getFullYear(); // 2022
      const monthFrom = dateFrom.getMonth() + 1; // 2 (Note: month is 0-indexed, so add 1 to get the actual month)
      const dayFrom = dateFrom.getDate(); // 19
      const hoursFrom = String(dateFrom.getHours()).padStart(2, '0'); // '00'
      const minutesFrom = String(dateFrom.getMinutes()).padStart(2, '0'); // '00'

      const dateTo = new Date(obj.ending_time);
      const yearTo = dateTo.getFullYear(); // 2022
      const monthTo = dateTo.getMonth() + 1; // 2 (Note: month is 0-indexed, so add 1 to get the actual month)
      const dayTo = dateTo.getDate(); // 19
      const hoursTo = String(dateTo.getHours()).padStart(2, '0'); // '00'
      const minutesTo = String(dateTo.getMinutes()).padStart(2, '0'); // '00'

      const timeFrom = convertTime(hoursFrom+":"+minutesFrom);
      const timeTo = convertTime(hoursTo +":"+ minutesTo);

      const newEvent = {
        id: obj.event_id,
        title: obj.title_of_event,
        time: timeFrom + " - " + timeTo,
        location : obj.location_of_event,
        notes : obj.additional_notes,
        tagged : obj.tagged_users, 
        addedBy : obj.added_by,
      };
      console.log(newEvent);

      // if event array empty or current day has no event, create new 
      eventsArr.push({
        day: dayFrom,
        month: monthFrom,
        year: yearFrom,
        events: [newEvent],
      });
      
      console.log(eventsArr);

      //select active day and add event class if not added
    }
    initCalendar();
    updateEvents(activeDay);
  }
}
