<template>
    <div class="schedule-container">
      <div class="header">
        <div class="buttons-row">
          <div class="left-buttons">
            <div class="schedule-selector">
              <select v-model="selectedSchedule" @change="selectSchedule">
                <option v-for="schedule in schedules" :key="schedule.id" :value="schedule">{{ schedule.name }}</option>
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
          <!-- Events will be added here -->
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        schedules: [
          {
            id: 1,
            name: 'Schedule 1',
            events: []
          }
        ],
        selectedSchedule: null,
        days: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        times: [
          '00:00', '01:00', '02:00', '03:00', '04:00', '05:00',
          '06:00', '07:00', '08:00', '09:00', '10:00', '11:00',
          '12:00', '13:00', '14:00', '15:00', '16:00', '17:00',
          '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'
        ]
      };
    },
    methods: {
      addSchedule() {
        const newSchedule = {
          id: this.schedules.length + 1,
          name: `Schedule ${this.schedules.length + 1}`,
          events: []
        };
        this.schedules.push(newSchedule);
        this.selectedSchedule = newSchedule;
      },
      deleteSchedule() {
        if (this.selectedSchedule) {
          const index = this.schedules.findIndex(schedule => schedule.id === this.selectedSchedule.id);
          if (index !== -1) {
            this.schedules.splice(index, 1);
            this.selectedSchedule = this.schedules.length > 0 ? this.schedules[0] : null;
          }
        }
      },

      fetchSchedules() {
      // You would fetch from an API, here is a hardcoded example
      this.schedules = [
        { id: 1, title: 'Class Schedule' },
        { id: 2, title: 'Test Schedule' },
        { id: 3, title: 'Test3' }
      ];
    },
      selectSchedule() {
        console.log('Selected schedule:', this.selectedSchedule);
      },
      addEvent() {
        // Logic to handle adding an event to the selected schedule
        console.log('Add an event to the selected schedule');
      }
    },
    created() {
      // Set the initial selected schedule
      this.selectedSchedule = this.schedules.length > 0 ? this.schedules[0] : null;
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
    grid-template-rows: repeat(24, 60px);
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
    height: 60px;
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
  </style>