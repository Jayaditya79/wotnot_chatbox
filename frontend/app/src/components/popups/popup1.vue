<template>
  <div class="fixed inset-0 bg-black bg-opacity-40 flex justify-center items-center z-[10000]">
    <div class="bg-[#f5f6fa] p-5 rounded-lg w-28% shadow-lg relative">
      <span class="absolute top-2.5 right-8 text-4xl cursor-pointer text-black" @click="$emit('close')">&times;</span>
      <slot/>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PopUp1'
}
</script>
























<!-- <template>
    <div class="popup1">
      <div class="popup1-inner">
        <span class="close" @click="$emit('close')">&times;</span>
        <slot/>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'PopUp1'
  }
  </script>
  
  <style scoped>
  .popup1 {
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    background-color: rgba(0, 0, 0, 0.4); /* Darkened overlay */
    display: flex;
    justify-content: center;
    align-items: center; /* Center the popup vertically */
    z-index: 10000;
  }
  
  .popup1-inner {
    background-color: #f5f6fa;
    padding: 20px;
    border-radius: 8px;
    width: 28%; /* Reduced width */
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
    position: relative; /* Ensures close button is relative to this container */
  }
  
  .close {
    position: absolute;
    top: 10px; /* Positioned closer to the top-right corner */
    right: 10px;
    font-size: 20px;
    cursor: pointer;
    color: black;
  }
  </style>
   -->