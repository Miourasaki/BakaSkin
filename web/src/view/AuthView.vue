<script setup>

import axios from "axios";
import {useRouter} from "vue-router";
import Cookies from "js-cookie";

const router = useRouter();

const accessToken = Cookies.get("accessToken");
  if (accessToken) {
    axios.post("/api/yggdrasil/authserver/validate", {
      accessToken: accessToken
    }).then(()=>{
    router.replace("/")
    })
  }
</script>

<template>

    <router-view />
</template>
