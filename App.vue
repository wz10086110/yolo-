<template>
  <div class="app">

    <UploadPanel @analysisFinished="setResult" />

    <ResultPanel :result="result" />

  </div>
</template>

<script setup>
import { ref } from "vue"

import UploadPanel from "./components/UploadPanel.vue"
import ResultPanel from "./components/ResultPanel.vue"

const result = ref(null)

function setResult(data) {
  console.log("最终数据：", data)
  result.value = data
}
</script>