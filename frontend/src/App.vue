<!-- App.vue
 -->
<template>
  <div id="app">
    <ScheduleComponent/>
    <Toast/>
  </div>
</template>

<script>
import ScheduleComponent from './components/ScheduleComponent.vue';
import Toast from '@/components/ToastNotification.vue'


export default {
  name: 'App',
  components: {
    ScheduleComponent,
    Toast
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
