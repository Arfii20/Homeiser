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
  addEventSubmit = document.querySelector(".add-event-btn ");
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
        events += `<div class="event">
            <div class="title">
              <i class="fas fa-circle"></i>
              <h3 class="event-title">${event.title}</h3>
            </div>
            <div class="event-time">
              <span class="event-time">${event.time}</span>
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
  saveEvents();
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


//function to add event to eventsArr
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
  const newEvent = {
    title: eventTitle,
    time: timeFrom + " - " + timeTo,
    location : eventLocation,
    notes : eventNotes,
    tagged : eventTaggedUsers, 
    addedBy : null,
  };
  console.log(newEvent);
  console.log(activeDay);
  let eventAdded = false;

  //check of eventArr not empty
  if (eventsArr.length > 0) {
    //check if curretn day has already any event, then add to that 
    eventsArr.forEach((item) => {
      if (
        item.day === activeDay &&
        item.month === month + 1 &&
        item.year === year
      ) {
        item.events.push(newEvent);
        eventAdded = true;
      }
    });
  }

  // if event array empty or current day has no eveet, create new 
  if (!eventAdded) {
    eventsArr.push({
      day: activeDay,
      month: month + 1,
      year: year,
      events: [newEvent],
    });
  }

  console.log(eventsArr);

  //select active day and add event class if not added

  //also add event class to newly added day if not already 
  const activeDayEl = document.querySelector(".day.active");
  if (!activeDayEl.classList.contains("event")) {
    activeDayEl.classList.add("event");
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

    //show added event 
    updateEvents(activeDay);
  }else{
    const response_error = await response.json();
    console.log(response_error.error);
  }
});

//function to delete event when clicked on event
eventsContainer.addEventListener("click", (e) => {
  if (e.target.classList.contains("event")) {
    if (confirm("Are you sure you want to delete this event?")) {
      //get event title of event, then search in array and delete 
      const eventTitle = e.target.children[0].children[1].innerHTML;
      eventsArr.forEach((event) => {
        if (
          event.day === activeDay &&
          event.month === month + 1 &&
          event.year === year
        ) {
          event.events.forEach((item, index) => {
            if (item.title === eventTitle) {
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
      //after removing from array , update event
      updateEvents(activeDay);
    }
  }
});

//function to save events in local   - AREFIN TP CHANGE TO DATABASE 
function saveEvents() {
  console.log(eventsArr);
  localStorage.setItem("events", JSON.stringify(eventsArr));
}

//function to get events from local storage
// function getEvents() {
//   console.log(eventsArr);
//   //check if events are already saved in local storage then return event else nothing
//   if (localStorage.getItem("events") === null) {
//     return;
//   }

//   eventsArr.push(...JSON.parse(localStorage.getItem("events")));
// }

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

async function get_calendarEvent(household_id){
  const url = BASE + "get_shared_calendar/" + household_id;
  const data = new URLSearchParams();

  const startDate = '2022-02-19 00:00:00';
  const endDate = '2024-02-19 00:00:00';

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
    const response_array = JSON.parse(await response.json());

    for (let i = 0; i < response_array.length; i++) {
      const obj = JSON.parse(response_array[i]);

      const eventID= obj.event_id;

      // const dateString = '2022-02-19 00:00:00';
      const dateFrom = new Date(obj.starting_time);
      const dateTo = new Date(obj.ending_time);

      const year = date.getFullYear(); // 2022
      const month = date.getMonth() + 1; // 2 (Note: month is 0-indexed, so add 1 to get the actual month)
      const day = date.getDate(); // 19
      const hours = date.getHours(); // 0
      const minutes = date.getMinutes(); // 0
      const seconds = date.getSeconds(); // 0

      const timeFrom = convertTime(hoursFrom +":"+ minutesFrom);
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
        day: dateFrom.getDate(),
        month: dateFrom.getMonth() + 1,
        year: dateFrom.getFullYear(),
        events: [newEvent],
      });

      console.log(eventsArr);

      //select active day and add event class if not added

      //also add event class to newly added day if not already 
      const activeDayEl = document.querySelector(".day.active");
      if (!activeDayEl.classList.contains("event")) {
        activeDayEl.classList.add("event");
      }
    }
  }
}
























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
