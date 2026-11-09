<template>

  <HeaderBar />

  <div class="container">

    <UploadPanel
      @filesUploaded="setFiles"
      @folderUploaded="setFolder"
      @analysisFinished="setResult"
      @startBatchAnalyze="startBatchAnalyze"
    />

    <ImageViewer
      :currentImage="currentImage"
      :resultImage="resultImage"
    />

    <ResultPanel
      :result="result"
    />

  </div>

</template>

<script setup>

import { ref } from "vue"
import request from "../api/request"

import HeaderBar from "../components/HeaderBar.vue"
import UploadPanel from "../components/UploadPanel.vue"
import ImageViewer from "../components/ImageViewer.vue"
import ResultPanel from "../components/ResultPanel.vue"

const currentImage = ref("")
const resultImage = ref("")
const result = ref({})
const imageList = ref([])
const imageFile = ref(null)

function setFiles(data){
  imageFile.value = data
  currentImage.value = data
}

function setFolder(files){

  imageList.value = files
  imageFile.value = null

  if(files.length > 0){
    currentImage.value =
      URL.createObjectURL(files[0])
  }

  result.value = {}
  resultImage.value = ""
}

async function setResult(data){

  result.value = data

  if(data.result_image){
    resultImage.value =
      "http://127.0.0.1:8000" + data.result_image
  }
}

async function startBatchAnalyze(){

  if(imageList.value.length === 0){
    return
  }

  for(let i = 0; i < imageList.value.length; i++){

    const file = imageList.value[i]

    const formData = new FormData()
    formData.append("file", file)

    try{

      const res = await request.post(
        "/analyze",
        formData
      )

      if(i === 0){
        setResult(res.data)
      }

    }catch(err){
      console.log("batch error:", err)
    }
  }
}

</script>

<style scoped>

.container{
  height:calc(100vh - 70px);
  display:flex;
  background:#eef2f7;
}

</style>