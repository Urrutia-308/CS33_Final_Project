import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './main.css' //Global CSS for Font
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import '@mdi/font/css/materialdesignicons.css'
import { VCalendar } from 'vuetify/labs/VCalendar'
import { VNumberInput } from 'vuetify/labs/VNumberInput'
const vuetify = createVuetify({
    components:{
      VCalendar,
      VNumberInput,
      ...components,
    },
    
    directives,
    icons: {
        defaultSet: 'mdi',
        aliases,
        sets: {
          mdi,
        },
    },
})
  
  createApp(App).use(router).use(vuetify).mount('#app')