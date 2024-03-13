<script setup>
import {Input} from "postcss";

const Loading = ref(false);

import AnButton from "../../components/AnButton.vue";
import {ref} from "vue";
import axios from "axios";
import {useRouter} from "vue-router";
import LoadingComponent from "../../components/LoadingComponent.vue";
import Cookies from "js-cookie";
import IndexCompTemplate from "../../components/IndexCompTemplate.vue";

const isSlim = ref(false);

const props = defineProps({
  skin: String,
  stype: String,
});

const router = useRouter();
function Submit(event) {
        Loading.value = true;
  event.preventDefault();

  const formData = new FormData(event.target);


  axios.put(`/api/user/profile/${Cookies.get("profileUUID")}/SKIN?backTextures=true`, {
    file: formData.get("file"),
    model:  isSlim? 'slim':'classic'
  },{
    headers: {
      Authorization: `Bearer ${Cookies.get("accessToken")}`,
      "Content-Type": 'multipart/form-data'
    }
  }).then(r => {
    const ApiData = r.data
      localStorage.setItem("textures",ApiData["properties"][0]["value"])
    location.reload()
  }).catch(
      error => {
        try {
          alert(error.response.data["cause"])

        } catch (e) {
          alert("Unknown error!")
        }

        Loading.value = false;
      }
  )

}

const fileInputRef = ref(null);
const imageSrc = ref(null);

const openFilePicker = () => {
  const fileInput = fileInputRef.value;
  fileInput.click();
};

const handleFileChange = (event) => {
  const file = event.target.files[0];
  const reader = new FileReader();

  reader.onload = (e) => {
    imageSrc.value = e.target.result;
  };

  if (file) {
    reader.readAsDataURL(file);
  }
};

const handleDrop = (event) => {
  event.preventDefault();
  const file = event.dataTransfer.files[0];
  updateFileInput(event.dataTransfer.files);
  readAndDisplayImage(file);
};
const readAndDisplayImage = (file) => {
  const reader = new FileReader();
  reader.onload = (e) => {
    imageSrc.value = e.target.result;
  };

  if (file) {
    reader.readAsDataURL(file);
  }
};

const updateFileInput = (file) => {
  const fileInput = fileInputRef.value;
  fileInput.files = file;
};
</script>

<template>
<IndexCompTemplate title="Edit Profile Skin" :is-open="true">
  <form @submit="Submit" class="w-full shadow px-5 py-6 shadow-gray-400 bg-white bg-opacity-50">


   <div class="flex flex-col items-start  mb-4 text-blue-700 ">
        <label class="text-xs text-gray-500 transition-all mb-2">Update skin Now:</label>
        <div @dragover.prevent
    @drop="handleDrop" @click="openFilePicker" class="w-full border uppercase font-bold text-xl h-auto flex relative justify-center items-center focus:outline-0 p-1 bg-white shadow-sm  cursor-pointer">
          <div v-if="!imageSrc" class="h-20 flex justify-center items-center">
            <svg  viewBox="0 0 24 24" class="w-10 h-10"><path d="M9 16h6v-6h4l-7-7l-7 7h4v6zm-4 2h14v2H5v-2z" fill="currentColor"></path></svg>
            Upload Skin</div>
          <div v-if="imageSrc" class="w-full group"><img :src="imageSrc" class="w-full h-auto">
          <div class="hidden absolute bg-white w-full h-full text-2xl top-0 left-0 bg-opacity-50 group-hover:flex justify-center items-center">
            <svg  viewBox="0 0 1024 1024" class="w-10 h-10"><path d="M909.1 209.3l-56.4 44.1C775.8 155.1 656.2 92 521.9 92C290 92 102.3 279.5 102 511.5C101.7 743.7 289.8 932 521.9 932c181.3 0 335.8-115 394.6-276.1c1.5-4.2-.7-8.9-4.9-10.3l-56.7-19.5a8 8 0 0 0-10.1 4.8c-1.8 5-3.8 10-5.9 14.9c-17.3 41-42.1 77.8-73.7 109.4A344.77 344.77 0 0 1 655.9 829c-42.3 17.9-87.4 27-133.8 27c-46.5 0-91.5-9.1-133.8-27A341.5 341.5 0 0 1 279 755.2a342.16 342.16 0 0 1-73.7-109.4c-17.9-42.4-27-87.4-27-133.9s9.1-91.5 27-133.9c17.3-41 42.1-77.8 73.7-109.4c31.6-31.6 68.4-56.4 109.3-73.8c42.3-17.9 87.4-27 133.8-27c46.5 0 91.5 9.1 133.8 27a341.5 341.5 0 0 1 109.3 73.8c9.9 9.9 19.2 20.4 27.8 31.4l-60.2 47a8 8 0 0 0 3 14.1l175.6 43c5 1.2 9.9-2.6 9.9-7.7l.8-180.9c-.1-6.6-7.8-10.3-13-6.2z" fill="currentColor"></path></svg>
            reupload
          </div></div>
        </div>
        <input ref="fileInputRef" @change="handleFileChange" accept="image/png" class="w-full border hidden focus:outline-0 p-1 bg-white shadow-sm text-sm mt-6"
               required
               type="file"
               name="file">


         <div class="flex w-full mt-3 text-blue-500 font-bold text-sm py-0.5 bg-white relative border shadow-sm">
            <button @click="isSlim=false" class="w-1/2  z-10" :class="`${!isSlim && 'text-white'}`" type="button">classic</button>
            <button @click="isSlim=true" class="w-1/2  z-10" :class="`${isSlim && 'text-white'}`" type="button">slim</button>
           <span class="w-1/2 top-0 left-0 transition-all absolute bg-blue-500 h-full"
           :class="`${isSlim? 'translate-x-full':''}`"></span>
         </div>
      </div>

  <an-button>Submit</an-button>

     <div class="flex flex-col items-start  mt-8 h-auto">
        <label class="text-xs text-gray-500 transition-all mb-1">You skin Now: ({{props.stype}})</label>
        <div class="w-full p-1 text-sm flex items-start justify-start">
          <img :src="props.skin" class="w-full h-full shadow-xl bg-white">
        </div>
      </div>

</form>
  <LoadingComponent v-if="Loading"/>
</IndexCompTemplate>
</template>

<style scoped>

</style>