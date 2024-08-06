<template>
  <d2-container>
    <div class="container">
      <div class="sidebar">
        <div class="style-select"></div>
        <div class="style-section">
          <h3>图片风格</h3>
          <div class="style-options">
            <button 
              class="option-button" 
              :class="{ selected: selectedStyle === 'cartoon' }" 
              @click="selectStyle('cartoon')">卡通</button>
            <button 
              class="option-button" 
              :class="{ selected: selectedStyle === 'anime' }" 
              @click="selectStyle('anime')">动漫</button>
            <button 
              class="option-button" 
              :class="{ selected: selectedStyle === 'realistic' }" 
              @click="selectStyle('realistic')">写实</button>
            <button 
              class="option-button" 
              :class="{ selected: selectedStyle === 'architecture' }" 
              @click="selectStyle('architecture')">建筑</button>
            <button 
              class="option-button" 
              :class="{ selected: selectedStyle === 'twozone' }" 
              @click="selectStyle('twozone')">二次元</button>
          </div>
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
          <el-form-item label="提示词">
            <el-input v-model="prompt" placeholder="如:一个漂亮的女孩" style="width: 400px;"></el-input>
          </el-form-item>
          <el-form-item label="反向提示词">
            <el-switch v-model="showNegativePrompt" active-text="开启" inactive-text="关闭"></el-switch>
          </el-form-item>
          <el-form-item v-if="showNegativePrompt" label="反向提示词">
            <el-input v-model="negativePrompt" placeholder="如:畸形,多人"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button 
              type="primary" 
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
import axios from 'axios';

export default {
  data() {
    return {
      showNegativePrompt: false,
      prompt: '',
      negativePrompt: '',
      loading: false,
      selectedStyle: '',
      selectedNum: null,
      width: '',
      height: '',
      generatedImages: [],
      styleImages: {
        cartoon: '../../../image/style/cartoon_image.jpeg',
        anime: 'path_to_anime_image',
        realistic: 'path_to_realistic_image',
        architecture: 'path_to_architecture_image',
        twozone: 'path_to_2d_image',
      }
    };
  },
  computed: {
    isButtonDisabled() {
      // The button is disabled if prompt is empty or selectedNum is null
      return !this.prompt || this.selectedNum === null;
    },
    selectedStyleImage() {
      return this.styleImages[this.selectedStyle];
    }
  },
  methods: {
    selectStyle(style) {
      this.selectedStyle = style;
    },
    selectNum(num) {
      this.selectedNum = num;
    },
    async generateImage() {
      this.loading = true;
      const params = {
        positive_prompt: this.prompt,
        negative_prompt: this.negativePrompt,
        // style: this.selectedStyle,
        batch_size: this.selectedNum,
        width: this.width,
        height: this.height
      };

    try {
    const response = await axios.post('http://localhost:5001/txt2img', params);
    console.log('API Response:', response.data); // 检查数据结构
    if (Array.isArray(response.data)) {
      this.generatedImages = response.data;
    } else {
      console.error('Invalid data format from API:', response.data);
    }
  } catch (error) {
    console.error('Error generating image:', error);
  } finally {
    this.loading = false;
  }
    },
    openPreview(image) {
      this.previewImage = image;
    },
    closePreview() {
      this.previewImage = null;
    }
  }
};
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
