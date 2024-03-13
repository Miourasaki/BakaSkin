<script setup>

import {onMounted, ref} from "vue";
import {useRouter} from "vue-router";
import AnButton from "../components/AnButton.vue";
import axios from "axios";
import LoadingComponent from "../components/LoadingComponent.vue";
import ProfileComponent from "./IndexView/ProfileComponent.vue";
import SkinComponent from "./IndexView/SkinComponent.vue";
import LinkComponent from "./IndexView/LinkComponent.vue";
import Cookies from "js-cookie";
import PwdComponent from "./IndexView/PwdComponent.vue";
import EmailComponent from "./IndexView/EmailComponent.vue";

const router = useRouter();

const UserId = ref(null);
const UserName = ref(null);
const UserEmail = ref(null);
const UserAvatar = ref("../assets/6ea6a47358157ac85c050760d26f9cbae058b370811ef1927bc55009d5b81f4f.png");
const UserSkin = ref(null);
const UserSkinType = ref(null);
const UserVerified = ref(true);
const Loading = ref(true);

  const accessToken = Cookies.get("accessToken");
  if (accessToken) {
    axios.post("/api/yggdrasil/authserver/validate", {
      accessToken: accessToken
    }).then(()=>{
     UserId.value = Cookies.get("profileUUID");

      axios.get(`/api/user/profile/${UserId.value}`,{
        headers:{
            Authorization: `Bearer ${accessToken}`,
        }
      }).then(r => {
        const ApiData = r.data;
     UserAvatar.value = `/api/parse/${UserId.value}/skin`;
     UserEmail.value = ApiData["email"];
     UserName.value = ApiData["username"];
     UserVerified.value = ApiData["verified"]

     UserSkin.value = ApiData["textures"]["SKIN"]["url"]
     try{
       UserSkinType.value = ApiData["textures"]["SKIN"]["metadata"]["model"]
     }catch{
        UserSkinType.value = "classic";
     }


    })

      Loading.value = false;
    }).catch(()=>{
    router.replace("/auth")
    })
  }else {
    router.replace("/auth")
  }

function Logout() {
  Loading.value = true;
  Cookies.remove("accessToken");
  setTimeout(()=>{router.replace("/auth")},500)
}


  function sendCode() {
  Loading.value = true;
    axios.get("/api/join/getCode",{
      headers:{
            Authorization: `Bearer ${accessToken}`,
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
</script>

<template>
  <div class="w-full h-full flex flex-col p-1 overflow-y-auto ">
    <div class="mt-8"></div>

    <div id="verify" v-if="!UserVerified" class="w-full shadow px-5 py-2 flex shadow-gray-400 bg-white mb-3 bg-opacity-50 border-l-8 border-red-400">
      <div class="flex-grow flex flex-col justify-center items-start">
        <div class="text-sm">此邮箱未经过验证</div>
        <div class="text-xs text-gray-400">未经验证的账户将在一天后或重启服务器时删除</div>
        <div class="text-xs text-red-400">没有收到验证邮件？<button @click="sendCode" class="hover:text-blue-900 transition-all text-blue-500">重新发送</button></div>
      </div>
    </div>

    <div id="main" class="w-full shadow px-5 py-6 shadow-gray-400 bg-white mb-3 bg-opacity-50">
      <div class="flex w-full overflow-auto">
        <img class="w-12 h-12 mr-4" :src='UserAvatar'/>
        <div class="flex flex-col flex-grow justify-center">
          <div class="font-bold text-lg text-blue-700">{{UserName}}</div>
          <div class="font-thin text-xs text-gray-600">{{UserEmail}}</div>
        </div>
      </div>

      <div class="mt-3 text-xs text-gray-400 overflow-x-auto">{{UserId}}</div>

    </div>

    <LinkComponent id="auth-link" />

    <div class="w-full flex flex-col gap-3 mb-8">
      <ProfileComponent id="edit-profileName" :name="UserName" />

      <SkinComponent id="edit-profileSkin" :skin="UserSkin" :stype="UserSkinType" />
    </div>

     <div class="w-full flex flex-col gap-3">
      <PwdComponent id="edit-userPassword" />

      <EmailComponent id="edit-userEmail" />
    </div>

    <an-button @click="Logout" class="mt-8 w-full mb-8">Logout</an-button>

  </div>
  <LoadingComponent v-if="Loading"/>
</template>

<style scoped>

</style>