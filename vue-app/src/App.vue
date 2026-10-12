<script setup>
import { onMounted } from 'vue'
import { installRippleEffect } from './composables/useRipple'

onMounted(() => {
  installRippleEffect()
})
</script>

<template>
  <router-view />
</template>
