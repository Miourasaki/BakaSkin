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


const router = useRouter();

const sendCode = () => {
      Loading.value = true;
  const newEmailInput = document.getElementById("new-email")
  axios.post(`/api/user/secure/email/code`, {
    "email": newEmailInput.value
  },{
        headers:{
            Authorization: `Bearer ${Cookies.get("accessToken")}`,
        }
      }).then(() => {
        Loading.value = false;
        alert("send succeed!")
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

function Submit(event) {
      Loading.value = true;
  event.preventDefault();

  const formData = new FormData(event.target);
  axios.post(`/api/user/secure/email`, {
    "code": formData.get("code"),
    "email": formData.get("email")
  },{
        headers:{
            Authorization: `Bearer ${Cookies.get("accessToken")}`,
        }
      }).then(() => {
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
<IndexCompTemplate title="Update you email" :is-open="false">


    <form @submit="Submit" class="w-full  px-5 py-6 bg-white bg-opacity-50">
  <an-input id="new-email" name="email" required type="email">New Email:</an-input>
  <div class="flex items-start">
    <an-input name="code" required type="text" class="flex-grow">Code:</an-input>
    <an-button @click="sendCode" class="ml-4 mt-2 w-10 h-9" type="button">Send</an-button>
  </div>
  <an-button>Submit</an-button>
</form>
  <LoadingComponent v-if="Loading"/>


</IndexCompTemplate>
</template>

<style scoped>

</style>