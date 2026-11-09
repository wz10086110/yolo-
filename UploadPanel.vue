<template>

<div class="left">

  <h2>图片上传</h2>

  <input
    type="file"
    accept="image/*"
    @change="selectImage"
  />

  <br><br>

  <h2>文件夹上传</h2>

  <input
    type="file"
    webkitdirectory
    multiple
    @change="selectFolder"
  />

  <p v-if="fileName">
    {{ fileName }}
  </p>

  <button
    class="btn"
    @click="startAnalyze"
    :disabled="loading"
  >
    {{ loading ? "分析中..." : "开始分析" }}
  </button>

</div>

</template>

<script setup>

import { ref } from "vue"
import request from "../api/request"

const emit = defineEmits(["analysisFinished"])

const imageFile = ref(null)
const folderFiles = ref([])
const fileName = ref("")
const loading = ref(false)

function selectImage(e){

  const file = e.target.files[0]
  if(!file) return

  imageFile.value = file
  folderFiles.value = []
  fileName.value = file.name
}

function selectFolder(e){

  const files = Array.from(e.target.files)
    .filter(f => f.type.startsWith("image/"))

  folderFiles.value = files
  imageFile.value = null

  fileName.value = `已选择 ${files.length} 张图片`
}

async function startAnalyze() {

  if (loading.value) return
  loading.value = true

  try {

    let res

    // ======================
    // 单图
    // ======================
    if (imageFile.value) {

      const formData = new FormData()
      formData.append("file", imageFile.value)

      res = await request.post("/analyze", formData)

      console.log("单图返回：", res.data)

      emit("analysisFinished", normalize(res.data))
      return
    }

    // ======================
    // 文件夹
    // ======================
    if (folderFiles.value.length > 0) {

      const formData = new FormData()

      folderFiles.value.forEach(file => {
        formData.append("files", file)
      })

      const uploadRes = await request.post("/upload-folder", formData)

      const folderId = uploadRes.data.folder_id

      const analyzeForm = new FormData()
      analyzeForm.append("folder_id", folderId)

      // ⭐⭐⭐ 关键增强：防卡死 + 超时保护
      const timeout = new Promise((_, reject) =>
        setTimeout(() => reject(new Error("分析超时（120s）")), 120000)
      )

      const requestPromise = request.post(
        "/start-analysis",
        analyzeForm
      )

      res = await Promise.race([
        requestPromise,
        timeout
      ])

      console.log("文件夹返回：", res.data)

      emit("analysisFinished", normalizeFolder(res.data))
      return
    }

    alert("请先选择图片或文件夹")

  } catch (err) {

    console.log("分析失败:", err)
    alert("分析失败或超时，请检查后端")

  } finally {
    loading.value = false
  }
}

/**
 * 单图统一结构
 */
function normalize(data) {
  return {
    ...data,
    images: data.images || {
      original: null,
      final: null
    }
  }
}

/**
 * 文件夹统一结构
 */
function normalizeFolder(data) {
  return {
    ...data,
    results: (data.results || []).map(item => ({
      ...item,
      images: item.images || {
        original: null,
        final: null
      }
    }))
  }
}

</script>

<style scoped>

.left{
  width:260px;
  background:white;
  padding:20px;
  border-right:1px solid #ddd;
}

.btn{
  width:100%;
  height:45px;
  margin-top:20px;
  background:#1677ff;
  color:white;
  border:none;
  cursor:pointer;
  border-radius:6px;
}

.btn:disabled{
  background:#999;
  cursor:not-allowed;
}

</style>