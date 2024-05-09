<template>
    <div class="schedule-container">
      <div class="header">
        <div class="buttons-row">
          <div class="left-buttons">
            <div class="schedule-selector">
              <select v-model="selectedSchedule" @change="selectSchedule">
                <option v-for="schedule in schedules" :key="schedule.id" :value="schedule">{{ schedule.title }}</option>
              </select>
              <button class="add-schedule-button" @click="addSchedule">+</button>
              <button class="delete-schedule-button" @click="deleteSchedule">🗑️</button>
            </div>
          </div>
          <div class="right-buttons">
            <button class="add-event-button" @click="addEvent">ADD AN EVENT</button>
          </div>
        </div>
        <div class="days-row">
          <div class="days">
            <div class="day" v-for="day in days" :key="day">{{ day }}</div>
          </div>
        </div>
      </div>
      <div class="schedule">
        <div class="times">
          <div class="time" v-for="time in times" :key="time">{{ time }}</div>
        </div>
        <div class="events">
          <div class="event-lines">
            <div class="event-line" v-for="time in times" :key="time"></div>
          </div>
          <div v-if="selectedSchedule && selectedSchedule.events">
            <div v-for="event in selectedSchedule.events" :key="event.eventID">
            <div v-for="day in event.daysOfWeek" :key="day" class="event-block"
            :style="getEventBlockStyle(event, day)" @click="openDeleteEventPopup(event)">
            <div class="event-description">{{ event.description }}</div>
            <div class="event-time">{{ formatTime(event.startTime) }} - {{ formatTime(event.endTime) }}</div>
            </div>
            </div>
            </div>
        </div>
      </div>
    </div>
  
    <!-- Pop-up window -->
    <div class="popup" v-if="showPopup">
      <div class="popup-content">
        <h3>Create New Schedule</h3>
        <input type="text" v-model="newScheduleName" placeholder="Enter schedule name">
        <div class="popup-buttons">
          <button @click="createSchedule">Create</button>
          <button @click="showPopup = false">Cancel</button>
        </div>
      </div>
    </div>

        <!-- Schedule Deletion Confirmation Pop-up -->
        <div class="popup" v-if="showDeleteSchedulePopup">
        <div class="popup-content">
            <h3>Confirm Schedule Deletion</h3>
            <p>Are you sure you want to delete this schedule?</p>
            <div class="popup-buttons">
            <button @click="confirmDeleteSchedule">Delete</button>
            <button @click="closeDeleteSchedulePopup">Cancel</button>
            </div>
        </div>
        </div>
  

    <!-- Event Deletion Confirmation Pop-up -->
    <div class="popup" v-if="showDeleteEventPopup">
    <div class="popup-content">
        <h3>Confirm Event Deletion</h3>
        <p>Are you sure you want to delete this event?</p>
        <div class="popup-buttons">
        <button @click="deleteEvent">Delete</button>
        <button @click="closeDeleteEventPopup">Cancel</button>
        </div>
    </div>
    </div>

    <!-- Event Creation Pop-up -->
    <div class="popup" v-if="showEventPopup">
      <div class="popup-content">
        <h3>Create New Event</h3>
        <input type="text" v-model="newEvent.title" placeholder="Enter event title">
        <input type="text" v-model="newEvent.description" placeholder="Enter event description">
        <input type="time" v-model="newEvent.startTime" placeholder="Start Time">
        <input type="time" v-model="newEvent.endTime" placeholder="End Time">
        <input type="color" v-model="newEvent.color">
        <div>
          <label v-for="day in days" :key="day">
            <input type="checkbox" :value="day" v-model="newEvent.daysOfWeek"> {{ day }}
          </label>
        </div>
        <div class="popup-buttons">
          <button @click="createEvent">Create</button>
          <button @click="showEventPopup = false">Cancel</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
  return {
    schedules: [],
    selectedSchedule: null,
    days: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
    times: [
      '00:00', '01:00', '02:00', '03:00', '04:00', '05:00',
      '06:00', '07:00', '08:00', '09:00', '10:00', '11:00',
      '12:00', '13:00', '14:00', '15:00', '16:00', '17:00',
      '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'
    ],
    showPopup: false,
    newScheduleName: '',
    showEventPopup: false,
    newEvent: {
      description: '',
      startTime: '',
      endTime: '',
      color: '#000000',
      daysOfWeek: []
    },
    showDeleteEventPopup: false,
    eventToDelete: null,
    showDeleteSchedulePopup: false,
    scheduleToDelete: null
  };
},
    methods: {
      addSchedule() {
        this.showPopup = true;
      },
      async createSchedule() {
        const newSchedule = {
          title: this.newScheduleName
        };
  
        // Make an HTTP POST request to the backend
        axios.post('http://localhost:5000/createSchedule', newSchedule)
          .then(response => {
            // Handle the response from the backend
            console.log('Schedule created:', response.data);
  
            // Add the new schedule to the schedules array with the returned ID
            newSchedule.id = response.data.scheduleID;
            this.schedules.push(newSchedule);
            this.selectedSchedule = newSchedule;
  
            // Clear the new schedule name and hide the pop-up
            this.newScheduleName = '';
            this.showPopup = false;
          })
          .catch(error => {
            // Handle any errors that occurred during the request
            console.error('Error creating schedule:', error);
          });
      },

        deleteSchedule() {
        if (!this.selectedSchedule) {
            alert('Please select a schedule to delete.');
            return;
        }
            this.scheduleToDelete = this.selectedSchedule;
            this.showDeleteSchedulePopup = true;
        },

        confirmDeleteSchedule() {
        axios.delete(`http://localhost:5000/deleteSchedule/${this.scheduleToDelete.id}`)
            .then(response => {
            console.log('Schedule deleted:', response);
            // Remove the schedule from the local list after successful deletion
            this.schedules = this.schedules.filter(schedule => schedule.id !== this.scheduleToDelete.id);
            this.selectedSchedule = this.schedules.length > 0 ? this.schedules[0] : null;
            this.closeDeleteSchedulePopup();
            //alert('Schedule deleted successfully.');
            })
            .catch(error => {
            console.error('Error deleting schedule:', error.response);
            if (error.response && error.response.data && error.response.data.error) {
                alert('Failed to delete schedule: ' + error.response.data.error);
            } else {
                alert('Failed to delete schedule. Please try again.');
            }
            });
        },
        
        fetchSchedules() {
            axios.get('http://localhost:5000/getSchedules')
            .then(response => {
                this.schedules = response.data;
            if (this.schedules.length > 0) {
                this.selectedSchedule = this.schedules[0];
                }
            })
            .catch(error => {
                console.error('Error fetching schedules:', error);
            });
        },
        
        selectSchedule() {
            console.log('Selected schedule:', this.selectedSchedule);
            if (this.selectedSchedule) {
                axios.get(`http://localhost:5000/getEvents/${this.selectedSchedule.id}`)
                    .then(response => {
                        this.selectedSchedule.events = response.data;
                    })
                    .catch(error => {
                        console.error('Error fetching events:', error);
                    });
            }
        },

        addEvent() {
            if (!this.selectedSchedule) {
            alert('Please select a schedule first!');
            return;
            }
            this.showEventPopup = true;
        },
        
        createEvent() {
        const newEvent = {
            scheduleID: this.selectedSchedule.id,
            title: this.newEvent.title,
            description: this.newEvent.description,
            color: this.newEvent.color,
            startTime: this.newEvent.startTime,
            endTime: this.newEvent.endTime,
            daysOfWeek: this.newEvent.daysOfWeek
        };

        axios.post('http://localhost:5000/addEvent', newEvent)
            .then(response => {
            console.log('Event added:', response.data);
            this.selectedSchedule.events.push({ ...newEvent, eventID: response.data.eventID });
            this.resetNewEvent();
            this.showEventPopup = false;
            })
            .catch(error => {
            console.error('Error adding event:', error);
            });
        },


        getEventBlockStyle(event, day) {
        const startTime = new Date(`2000-01-01T${event.startTime}`);
        const endTime = new Date(`2000-01-01T${event.endTime}`);
        const dayIndex = this.days.indexOf(day);
        const rowHeight = 80;
        const top = (startTime.getHours() * 60 + startTime.getMinutes()) * (rowHeight / 60);
        const height = ((endTime - startTime) / 60000) * (rowHeight / 60);
        const left = dayIndex * (100 / 7);
        const width = 100 / 7;

        return {
            top: `${top}px`,
            height: `${height}px`,
            left: `${left}%`,
            width: `${width}%`,
            backgroundColor: event.color,
        };
        },

        formatTime(time) {
        return new Date(`2000-01-01T${time}`).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        },

        resetNewEvent() {
            this.newEvent = {
            description: '',
            startTime: '',
            endTime: '',
            color: '#000000'
            };
        },

        openDeleteEventPopup(event) {
            this.eventToDelete = event;
            this.showDeleteEventPopup = true;
        },
        closeDeleteEventPopup() {
            this.eventToDelete = null;
            this.showDeleteEventPopup = false;
        },
        deleteEvent() {
            const eventID = this.eventToDelete.eventID;
            axios.delete(`http://localhost:5000/deleteEvent/${eventID}`)
            .then(response => {
                console.log('Event deleted:', response.data);
                // Remove the event from the local array
                this.selectedSchedule.events = this.selectedSchedule.events.filter(event => event.eventID !== eventID);
                this.closeDeleteEventPopup();
            })
            .catch(error => {
                console.error('Error deleting event:', error);
            });
        },

        closeDeleteSchedulePopup() {
            this.scheduleToDelete = null;
            this.showDeleteSchedulePopup = false;
        },


    },
    created() {
        this.fetchSchedules();
    }
  };
  </script>
  
  <style scoped>
  .schedule-container {
    display: flex;
    flex-direction: column;
    height: 800px; /* Increased height */
  }
  
  .header {
    display: flex;
    flex-direction: column;
    background-color: #f0f0f0;
    position: sticky;
    top: 0;
    z-index: 1;
  }
  
  .buttons-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px;
  }
  
  .left-buttons {
    display: flex;
    align-items: center;
  }
  
  .right-buttons {
    display: flex;
    justify-content: flex-end;
  }
  
  .days-row {
    padding: 10px;
  }
  
  .days {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 1px;
    width: 100%;
  }
  
  .day {
    display: flex;
    justify-content: center;
    align-items: center;
    font-weight: bold;
    font-size: 18px;
    padding: 10px;
    border-right: 1px solid #ccc;
  }
  
  .add-event-button {
    padding: 8px 16px;
    font-size: 16px;
    font-weight: bold;
    background-color: #03030e;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin-left: 20px;
  }
  
  .schedule {
    display: grid;
    grid-template-columns: 80px 1fr;
    gap: 1px;
    overflow-y: auto;
  }
  
  .times {
    display: grid;
    grid-template-rows: repeat(24, 80px);
    background-color: #f0f0f0;
  }
  
  .time {
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 20px;
    border-bottom: 1px solid #ccc;
  }
  
  .events {
    background-color: white;
    position: relative;
  }
  
  .event-lines {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    pointer-events: none;
  }
  
  .event-line {
    border-bottom: 1px solid #eee;
    height: 80px;
  }
  
  .schedule-selector {
    display: flex;
    align-items: center;
    margin-right: 20px;
  }
  
  .add-schedule-button,
  .delete-schedule-button {
    padding: 4px 8px;
    font-size: 16px;
    background-color: #03030e;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin-left: 10px;
  }
  
  .popup {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999; /* Add a higher z-index value */
}
  
  .popup-content {
    background-color: white;
    padding: 20px;
    border-radius: 4px;
  }
  
  .popup-buttons {
    margin-top: 10px;
    text-align: right;
  }
  
  .popup-buttons button {
    margin-left: 10px;
  }

  .event-block {
    position: absolute;
    background-color: #f0f0f0;
    border-radius: 4px;
    padding: 4px;
    font-size: 12px;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    z-index: 1;
  }

  .event-description {
    font-weight: bold;
  }

  .event-time {
    font-size: 10px;
  }

  </style>