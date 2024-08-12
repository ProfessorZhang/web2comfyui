<template>
  <d2-container>
    <div class="container">
      <div class="sidebar">
        <div class="style-select"></div>
        <div class="style-section">
          <h3>图片上传</h3>
          <el-upload
            class="upload-demo"
            action="#"
            :show-file-list="false"
            :on-change="handleImageUpload"
            :before-upload="beforeUpload"
            :on-remove="handleRemove">
            <el-button type="primary" class="custom-button">点击上传</el-button>
          </el-upload>
          <img v-if="selectedStyleImage" :src="selectedStyleImage" class="preview-image">
        </div>
        <div class="num-section">
          <h3>图片数量</h3>
          <div class="num-options">
            <button
              class="option-button"
              :class="{ selected: selectedNum === 1 }"
              @click="selectNum(1)">1</button>
            <button
              class="option-button"
              :class="{ selected: selectedNum === 2 }"
              @click="selectNum(2)">2</button>
            <button
              class="option-button"
              :class="{ selected: selectedNum === 3 }"
              @click="selectNum(3)">3</button>
            <button
              class="option-button"
              :class="{ selected: selectedNum === 4 }"
              @click="selectNum(4)">4</button>
          </div>
        </div>
        <div class="size-section">
          <h3>图片大小</h3>
          <div class="size-inputs">
            <el-input v-model="width" placeholder="宽度 (px)" style="width: 100px; margin-right: 10px;"></el-input>
            <el-input v-model="height" placeholder="高度 (px)" style="width: 100px;"></el-input>
          </div>
        </div>
      </div>
      <el-form label-width="100px">
        <div class="main-content">
          <el-form-item label="图片提示词">
            <el-input v-model="prompt_body" type="textarea" placeholder="如:英国短毛猫" style="width: 400px;" :rows= "3"></el-input>
          </el-form-item>
          <el-form-item label="风格提示词">
            <el-input v-model="prompt_style" type="textarea" placeholder="如:动漫风格" style="width: 400px;" :rows= "3"></el-input>
          </el-form-item>
          <el-form-item label="反向提示词">
            <el-switch v-model="showNegativePrompt" active-text="开启" inactive-text="关闭"></el-switch>
          </el-form-item>
          <el-form-item v-if="showNegativePrompt" label="反向提示词">
            <el-input v-model="negativePrompt" type="textarea" placeholder="如:畸形,多人" :rows= "3"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button
              type="primary"
              class="custom-button"
              @click="generateImage"
              :loading="loading"
              :disabled="isButtonDisabled"
            >开始绘制</el-button>
          </el-form-item>
        </div>
        <div class="image-section" v-if="!loading &&generatedImages.length">
        <h3>生成的图片</h3>
        <div class="image-list">
          <img
            v-for="(img, index) in generatedImages"
            :src="img"
            :key="index"
            class="generated-image"
            @click="openPreview(img)"
          >
        </div>
        <div v-if="previewImage" class="preview-overlay" @click="closePreview">
          <img :src="previewImage" class="preview-image">
        </div>
      </div>
      </el-form>
    </div>
    <div v-if="loading" class="loading-overlay">
      <div class="spinner"></div>
      <p>正在努力生成图像...</p>
    </div>
  </d2-container>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      showNegativePrompt: false,
      prompt_body: '',
      prompt_style: '',
      negativePrompt: '',
      loading: false,
      selectedStyleImage: '',
      selectedNum: null,
      width: '',
      height: '',
      generatedImages: []
    }
  },
  computed: {
    isButtonDisabled () {
      // The button is disabled if prompt is empty or selectedNum is null
      return !this.prompt || this.selectedNum === null
    }
  },
  methods: {
    // selectStyle (style) {
    //   this.selectedStyle = style
    // },
    selectNum (num) {
      this.selectedNum = num
    },
    beforeUpload (file) {
      const isImage = file.type.startsWith('image/')
      if (!isImage) {
        this.$message.error('只能上传图片文件！')
      }
      return isImage
    },
    handleImageUpload (file) {
      const reader = new FileReader()
      reader.onload = (e) => {
        this.selectedStyleImage = e.target.result
      }
      reader.readAsDataURL(file.raw)
    },
    handleRemove () {
      this.selectedStyleImage = ''
    },
    async generateImage () {
      this.loading = true
      const formData = new FormData()
      formData.append('img_file', this.selectedStyleImage) // 添加上传的文件
      formData.append('positive_body', this.prompt_body)
      formData.append('positive_style', this.prompt_style)
      formData.append('negative_prompt', this.negativePrompt)
      formData.append('batch_size', this.selectedNum)
      formData.append('width', this.width)
      formData.append('height', this.height)

      try {
        const response = await axios.post('http://localhost:5001/img2img', formData, {
          headers: {
            'Content-Type': 'multipart/form-data' // 设置请求头
          }
        })
        console.log('API Response:', response.data) // 检查数据结构
        if (Array.isArray(response.data)) {
          this.generatedImages = response.data
        } else {
          console.error('Invalid data format from API:', response.data)
        }
      } catch (error) {
        console.error('Error generating image:', error)
      } finally {
        this.loading = false
      }
    },
    openPreview (image) {
      this.previewImage = image
    },
    closePreview () {
      this.previewImage = null
    }
  }
}
</script>

<style scoped>
.container {
  display: flex;
}

.sidebar {
  width: 200px;
  padding: 10px;
  border-right: 1px solid #43ccd1;
}

.size-section {
  margin-bottom: 30px;
}

.style-options, .num-options, .size-options {
  display: flex;
  flex-wrap: wrap;
}

.custom-button {
  background-color: #43ccd1 !important;
  border-color: #43ccd1 !important;
}

::v-deep .el-switch__label--left.is-active {
  color: rgb(0, 0, 0);
}

.option-button {
  margin-right: 10px;
  margin-top: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 5px;
  box-sizing: border-box;
  cursor: pointer;
  transition: all 0.3s ease;
  width: 60px;
  height: 40px;
  border: 1px solid transparent;
}

.option-button.selected {
  background-color: #43ccd1;
  color: #fff;
  border-color: #43ccd1;
}

.size-inputs {
  display: flex;
  align-items: center;
}

.main-content {
  flex: 1;
  padding: 10px;
}

.image-section {
  padding: 10px;
}

.image-list {
  display: flex;
  flex-wrap: wrap;
}

.generated-image {
  width: 500px;
  height: auto;
  margin: 10px;
  cursor: pointer;
  border: 1px solid #ddd;
  border-radius: 4px;
  transition: transform 0.3s ease;
}

.generated-image:hover {
  transform: scale(1.5);
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7); /* Slightly darker background */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: white;
  z-index: 1000; /* Ensure it is on top of other content */
}

.spinner {
  border: 8px solid rgba(0, 0, 0, 0.1);
  border-left-color: white;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
}

.preview-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1001; /* Ensure it is on top of other content */
}

.preview-image {
  max-width: 90%;
  max-height: 90%;
  border: 1px solid #fff;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

</style>
