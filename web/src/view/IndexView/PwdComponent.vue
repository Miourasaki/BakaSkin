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

function Submit(event) {
      Loading.value = true;
  event.preventDefault();

  const formData = new FormData(event.target);
  axios.post(`/api/user/secure/password`, {
    "pwd1": formData.get("pwd1"),
    "pwd2": formData.get("pwd2")
  },{
        headers:{
            Authorization: `Bearer ${Cookies.get("accessToken")}`,
        }
      }).then(() => {
        Cookies.remove("accessToken")
    location.href = "login"
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
<IndexCompTemplate title="Update you password" :is-open="false">


    <form @submit="Submit" class="w-full  px-5 py-6 bg-white bg-opacity-50">
  <an-input name="pwd1" required type="password">Input you new Password:</an-input>
  <an-input name="pwd2" required type="password">Repeat you new Password:</an-input>
  <an-button>Submit</an-button>
</form>
  <LoadingComponent v-if="Loading"/>


</IndexCompTemplate>
</template>

<style scoped>

</style>