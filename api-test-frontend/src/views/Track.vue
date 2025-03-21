<!-- filepath: api-test-frontend/src/views/Track.vue -->
<template>
  <div class="track form-container">
    <h2>轨迹参数配置</h2>
    <form @submit.prevent="submitTrackConfig">
      <div class="form-group">
        <label for="name">名称:</label>
        <input type="text" id="name" v-model="formData.name" required>
      </div>
      
      <div class="form-group">
        <label for="moveSpeed">移动速度:</label>
        <input type="number" id="moveSpeed" v-model="formData.move_speed" step="any" required>
      </div>
      
      <div class="form-group">
        <label for="moveAccel">加速度:</label>
        <input type="number" id="moveAccel" v-model="formData.move_accel" step="any" required>
      </div>
      
      <div class="form-group">
        <label for="iniPos">初始位置 [x,y,z]:</label>
        <input type="text" id="iniPos" v-model="iniPosString" placeholder="例如: 0,0,0" required>
      </div>
      
      <div class="form-group">
        <label for="moveDir">移动方向 [x,y,z]:</label>
        <input type="text" id="moveDir" v-model="moveDirString" placeholder="例如: 1,0,0" required>
      </div>
      
      <div class="form-group">
        <label for="trackType">轨迹类型:</label>
        <select id="trackType" v-model="formData.track_type" required>
          <option value="static">静止</option>
          <option value="linear">直线</option>
          <option value="circle">圆形</option>
          <option value="random">随机</option>
          <option value="random_circle">随机圆</option>
        </select>
      </div>
      
      <button type="submit" :disabled="loading">{{ loading ? '提交中...' : '提交' }}</button>
    </form>
    
    <div class="response-container">
      <h3>响应结果:</h3>
      <pre :class="responseClass">{{ responseData }}</pre>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch } from 'vue';
import axios from 'axios';

export default {
  name: 'Track',
  setup() {
    const formData = ref({
      name: '测试设备',
      move_speed: 1.5,
      move_accel: 0.5,
      ini_pos: [0, 0, 0],
      move_dir: [1, 0, 0],
      track_type: 'linear'
    });
    
    const iniPosString = ref('0,0,0');
    const moveDirString = ref('1,0,0');
    const loading = ref(false);
    const responseData = ref('');
    const responseClass = ref('');
    
    // 将字符串转换为数组
    watch(iniPosString, (newVal) => {
      formData.value.ini_pos = newVal.split(',').map(v => parseFloat(v.trim()));
    });
    
    watch(moveDirString, (newVal) => {
      formData.value.move_dir = newVal.split(',').map(v => parseFloat(v.trim()));
    });
    
    // 初始化字符串表示
    watch(formData, (newVal) => {
      if (Array.isArray(newVal.ini_pos)) {
        iniPosString.value = newVal.ini_pos.join(',');
      }
      
      if (Array.isArray(newVal.move_dir)) {
        moveDirString.value = newVal.move_dir.join(',');
      }
    }, { immediate: true });

    const submitTrackConfig = async () => {
      loading.value = true;
      responseData.value = '请求中...';
      responseClass.value = '';
      
      try {
        const response = await axios.post('http://localhost:5000/api/track', formData.value);
        responseData.value = JSON.stringify(response.data, null, 2);
        responseClass.value = 'success';
      } catch (error) {
        responseClass.value = 'error';
        if (error.response) {
          responseData.value = JSON.stringify(error.response.data, null, 2);
        } else {
          responseData.value = error.message;
        }
      } finally {
        loading.value = false;
      }
    };

    return {
      formData,
      iniPosString,
      moveDirString,
      loading,
      responseData,
      responseClass,
      submitTrackConfig
    };
  }
}
</script>