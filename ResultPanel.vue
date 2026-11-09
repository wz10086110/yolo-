<template>
  <div v-if="displayData" class="panel">

    <!-- ================= 顶部信息卡 ================= -->
    <div class="card header">
      <h2>🏗 建筑损伤检测结果</h2>

      <div class="pdf-box" v-if="result.pdf_path">
        <a :href="result.pdf_path" target="_blank">
          📄 下载工程报告
        </a>
      </div>
    </div>

    <!-- ================= 指标区 ================= -->
    <div class="card stats">
      <div>裂缝：<b>{{ displayData.crack_count }}</b></div>
      <div>剥落：<b>{{ displayData.spalling_count }}</b></div>
      <div>钢筋：<b>{{ displayData.rebar_count }}</b></div>
      <div>等级：<b>{{ displayData.damage_level }}</b></div>
      <div>评分：<b>{{ displayData.score }}</b></div>
    </div>

    <!-- ================= 图片区 ================= -->
    <div class="card images">

      <div class="tab">
        <button
          :class="{active: tab==='original'}"
          @click="tab='original'"
        >
          原图
        </button>

        <button
          :class="{active: tab==='final'}"
          @click="tab='final'"
        >
          检测结果
        </button>
      </div>

      <div class="img-box">
        <img
          v-if="tab==='original'"
          :src="displayData.images?.original"
        />

        <img
          v-if="tab==='final'"
          :src="displayData.images?.final"
        />
      </div>

    </div>

    <!-- ================= 文件夹切换 ================= -->
    <div class="card file-list" v-if="result.results?.length > 1">

      <h3>📁 图片列表</h3>

      <div class="btn-group">
        <button
          v-for="(item,index) in result.results"
          :key="index"
          @click="currentIndex=index"
          :class="{active: currentIndex===index}"
        >
          {{ item.file }}
        </button>
      </div>

    </div>

  </div>
</template>

<script setup>
import { computed, ref } from "vue"

const props = defineProps({
  result: Object
})

const currentIndex = ref(0)
const tab = ref("original")

const displayData = computed(() => {
  if (!props.result) return null

  if (props.result.results) {
    return props.result.results[currentIndex.value]
  }

  return props.result
})
</script>

<style scoped>
.panel {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

/* 卡片统一风格 */
.card {
  background: #fff;
  padding: 16px;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

/* 顶部 */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* PDF按钮 */
.pdf-box a {
  background: #52c41a;
  color: white;
  padding: 8px 14px;
  border-radius: 6px;
  text-decoration: none;
}

/* 统计区 */
.stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  font-size: 14px;
}

/* tab */
.tab button {
  margin-right: 10px;
  padding: 6px 12px;
  border: none;
  background: #eee;
  cursor: pointer;
}

.tab .active {
  background: #1677ff;
  color: white;
}

/* 图片 */
.img-box {
  margin-top: 10px;
}

img {
  width: 100%;
  max-width: 500px;
  border-radius: 8px;
}

/* 文件列表 */
.btn-group {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.btn-group button {
  padding: 6px 10px;
  border: none;
  background: #1677ff;
  color: white;
  border-radius: 4px;
}

.btn-group .active {
  background: #52c41a;
}
</style>