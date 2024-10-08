<template>
    <div class="fixed inset-0 bg-black bg-opacity-20 flex justify-center items-center p-5 z-[10000] text-left shadow-lg">
      <div class="bg-[#ffffff] p-6 rounded-md w-[750px] overflow-y-auto relative max-h-[750px]">
        <span class="close" @click="$emit('close')" hover>&times;</span>   
        <slot/>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'PopUp'
  }
  </script>
  
  <style scoped>
.close{

  padding-left: 645px;
  font-size: 25px;
  cursor: pointer;
}
</style>