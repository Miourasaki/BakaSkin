<template>
  <div class="w-screen h-screen bg-[url(./assets/20200419124410_wfzok.jpg)]
  bg-no-repeat bg-cover bg-center text-white">
    <div class="bg-white bg-opacity-30 w-full h-full absolute top-0">
      <div class="w-full h-full flex justify-center items-center text-black">
        <div class="w-full h-full sm:w-[40rem] sm:h-96  px-8 bg-white bg-opacity-50 backdrop-blur-md shadow-xl flex items-center justify-between relative">
    <div class="w-[20rem] min-w-[20rem] h-full hidden  pr-16  sm:block py-8">
      <img draggable="false" @click="alert('咱可是最强的！')" src="./assets/baka.png" class="w-auto h-full active:scale-90 transition-all cursor-pointer" alt="">
    </div>
            <router-view />
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
</script>