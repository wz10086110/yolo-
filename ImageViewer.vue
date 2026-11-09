<template>

<div class="center">

  <div class="card">

    <h3>原始图片</h3>

    <img
      v-if="currentImage"
      :src="currentImage"
      class="img"
    />

  </div>

  <div class="card">

    <h3>损伤识别结果</h3>

    <img
      v-if="resultImage"
      :src="resultImage"
      class="img"
    />

  </div>

</div>

</template>

<script setup>

defineProps({
  currentImage: String,
  resultImage: String
})

</script>

<style scoped>

.center{
  flex:1;
  display:flex;
  padding:20px;
  gap:20px;
}

.card{
  flex:1;
  background:white;
  border-radius:10px;
  padding:15px;
}

.img{
  width:100%;
  height:600px;
  object-fit:contain;
}

</style>