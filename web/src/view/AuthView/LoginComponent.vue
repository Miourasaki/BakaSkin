<script setup>
import {ref} from "vue";
const Loading = ref(false);

import Cookies from "js-cookie"

import AnButton from "../../components/AnButton.vue";
import LoadingComponent from "../../components/LoadingComponent.vue";
import AnInput from "../../components/AnInput.vue";
import CryptoJS from "crypto-js"
import axios from "axios";
import {useRouter} from "vue-router";

const router = useRouter();

const LoginSubmit = (event) => {
  Loading.value = true;
  event.preventDefault();

  const formData = new FormData(event.target)
  const username = formData.get("user")
  const password = (CryptoJS.SHA1(formData.get("pwd"))).toString()


  axios.post("/api/yggdrasil/authserver/authenticate?useSHA1=false",
      {
        "username": username,
        "password": password,
        "requestUser": true,
        "agent": {
          "name": "Minecraft",
          "version": 1
        }
      }).then(r => {
    const ApiData = r.data
      const LocalUrl = new URL(location.host)


      Cookies.set("accessToken", ApiData["accessToken"],{ path: `.${LocalUrl.hostname}` })
      Cookies.set("profileUUID", ApiData["user"]["id"],{ path: `.${LocalUrl.hostname}` })
      router.push("/")
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

const ResetPassword = () => {
      Loading.value = true;
  const newEmailInput = document.getElementById("login-email")
  axios.post(`/api/user/secure/password/reset`, {
    "email": newEmailInput.value
  },{
      }).then(() => {
        Loading.value = false;
        alert("new password already send to you email!")
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
  <form @submit="LoginSubmit" class="flex-grow mb-1">
    <div class="mb-10 text-2xl font-mono text-blue-950">BakaRealm OpenID</div>

    <div class="p-1">
      <AnInput id="login-email" name="user" required>Email / Username</AnInput>

      <AnInput type="password" name="pwd" required>
        <div>Password</div>
        <div class="hover:text-blue-800 uppercase cursor-pointer" @click="ResetPassword" type="button">Reset Password!</div>
      </AnInput>
    </div>

    <AnButton>Submit</AnButton>

  </form>

  <LoadingComponent v-if="Loading"/>
</template>