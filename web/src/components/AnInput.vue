<script setup>


import {Input} from "postcss";
import {ref} from "vue";

const props = defineProps({
  type: Input.types,
  name: String,
  required: Boolean,
  id: String
});

</script>

<template>
      <div class="flex flex-col items-start  mb-8">
        <label class="text-xs text-gray-500 transition-all mb-0.5 w-full flex justify-between items-center"><slot /></label>
        <input class="w-full border-b border-blue-800 focus:outline-0 p-1 text-sm h-7 text-blue-700
bg-white bg-opacity-0" :id="id"
               :required="props.required"
               :type="props.type"
               :name="props.name">
      </div>
</template>

<style scoped>

</style>