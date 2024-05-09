<template>
    <!-- Toast container -->
    <div :class="{ 'toast-container': true, 'fade-in': showToast, 'fade-out': !showToast }" :style="{ backgroundColor: toastColor }">
        <div class="toast-content" :style="{ height: showToast ? 'auto' : '40px' }">
            <p>{{ toastMessage }}</p>
        </div>
        <div class="progress-bar" v-if="showToast">
            <div class="progress" :style="{ width: `${progress}%` }"></div>
        </div>
    </div>
</template>

<script>
    export default {
        props: {
            showToast: Boolean,
            toastMessage: String,
            toastColor:{
                type: String,
                default: '#da4d4d' //"#51da6e" alternate code for green color
            }
        },

        data() {
            return {
                progress: 100,
            };
        },

        watch: {
            showToast(newVal) {
                if (newVal) {
                    this.startProgressBar();
                }
            },
        },

        methods: {
            startProgressBar() {
                this.progress = 100;
                    const interval = setInterval(() => {
                    this.progress -= 1;
                        if (this.progress <= 0) {
                            clearInterval(interval);
                            this.dismissToast();
                        }
                    }, 50);
            },
                
            dismissToast() {
                this.progress = 0;
            },
        },
    };
    </script>

<style scoped>
    .toast-container {
        align-content: center;
        position: fixed;
        top: 10%;
        left: 50%;
        transform: translateX(-50%);
        background-color: var(--toast-color, #da4d4d);
        color: #ffffff;
        border-radius: 5px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        z-index: 999;
        opacity: 0;
        transition: opacity 0.3s ease-in-out;
        height: auto;
        overflow: hidden;
    }

    .fade-in {
        opacity: 1;
    }

    .fade-out {
        opacity: 0;
    }

    .toast-content {
        padding: 5px 20px;
        display: flex;
        justify-content: center;
        align-items: center;
        height: auto;
        font-family: Poppins;
    }

    .progress-bar {
        height: 5px;
        background-color: rgba(255, 255, 255, 0.5);
        border-radius: 3px;
        overflow: hidden;
        margin-top: 5px;
    }

    .progress {
        height: 100%;
        width: 100%;
        background-color: #ffffff;
        transition: width 0.05s linear;
    }
</style>