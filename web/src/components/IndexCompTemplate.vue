<script setup>
import {onMounted, ref} from "vue";

const props = defineProps({
  title: String,
  isOpen: Boolean = false
})

const isOpen = ref(props.isOpen);

const slotRoot = ref(null);
const slotHeigth = ref("0px");

onMounted(() => {
  // 在组件挂载后获取 slot 根元素的高度
  setInterval(()=>{
    let height = 0
    if (slotRoot.value.clientHeight) {
      height = slotRoot.value.clientHeight;
    }

  slotHeigth.value = `${(height + 28)}px`

  },100)
});

</script>

<template>
<div class="shadow shadow-gray-400 overflow-hidden transition-all" :style="isOpen? `height: ${slotHeigth};` : 'height: 1.75rem;'">
  <div @click="isOpen=!isOpen" class="w-full px-5 cursor-pointer bg-white bg-opacity-50 border border-gray-300 h-7
text-sm flex justify-between items-center">
    <div class="uppercase text-xs">{{props.title}}</div>
    <div class="">
      <svg viewBox="0 0 512 512"
           :class="`${!isOpen && '-rotate-90'}`"
           class="w-auto h-5 transition-all"><g><polygon points="128,192 256,320 384,192 	"></polygon></g></svg>
    </div>
  </div>
  <div ref="slotRoot" class="w-auto">
    <slot />
    </div>
</div>
</template>

<style scoped>

</style>