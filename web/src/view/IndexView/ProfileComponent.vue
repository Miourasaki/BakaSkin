<script setup>
import Cookies from "js-cookie";

const Loading = ref(false);

import AnInput from "../../components/AnInput.vue";
import AnButton from "../../components/AnButton.vue";
import {ref} from "vue";
import axios from "axios";
import {useRouter} from "vue-router";
import LoadingComponent from "../../components/LoadingComponent.vue";
import IndexCompTemplate from "../../components/IndexCompTemplate.vue";


const props = defineProps({
  name: String,
});

const router = useRouter();

function Submit(event) {
      Loading.value = true;
  event.preventDefault();

  const formData = new FormData(event.target);
  axios.post(`/api/user/profile/${Cookies.get("profileUUID")}/name`,
      {
        accessToken: Cookies.get("accessToken"),
        profileName: formData.get("profileName")
      }).then(() => {
      localStorage.setItem("name",formData.get("profileName"))
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
</script>

<template>
<IndexCompTemplate title="Edit Profile Name" :is-open="true">


    <form @submit="Submit" class="w-full  px-5 py-6 bg-white bg-opacity-50">
   <div class="flex flex-col items-start  mb-2">
        <label class="text-xs text-gray-500 transition-all mb-1">You profile name Now:</label>
        <div class="w-full p-1 text-sm flex items-start justify-start text-blue-900">
            {{props.name}}
        </div>
      </div>
  <an-input name="profileName" required class="flex-grow">set New profile name:</an-input>
  <an-button>Submit</an-button>
</form>
  <LoadingComponent v-if="Loading"/>


</IndexCompTemplate>
</template>

<style scoped>

</style>