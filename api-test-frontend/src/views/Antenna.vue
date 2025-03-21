<!-- filepath: api-test-frontend/src/views/Antenna.vue -->
<template>
  <div class="antenna form-container">
    <h2>天线配置</h2>
    <form @submit.prevent="submitAntennaConfig">
      <div class="form-group">
        <label for="antennaType">天线类型:</label>
        <select id="antennaType" v-model="formData.antenna_type" required>
          <option value="uniform_linear">均匀线性阵列</option>
          <option value="uniform_plane">均匀平面阵列</option>
          <option value="cylindrical">圆柱形阵列</option>
        </select>
      </div>
      
      <div class="form-group">
        <label for="antennaName">天线名称:</label>
        <input type="text" id="antennaName" v-model="formData.name" required>
      </div>
      
      <div class="form-group">
        <label for="numPerRow">每行单元数:</label>
        <input type="number" id="numPerRow" v-model="formData.num_per_row" min="1" required>
      </div>
      
      <div class="form-group">
        <label for="numPerCol">每列单元数:</label>
        <input type="number" id="numPerCol" v-model="formData.num_per_col" min="1" required>
      </div>
      
      <div class="form-group">
        <label for="spacingRow">行间距 (波长):</label>
        <input type="number" id="spacingRow" v-model="formData.spacing_row" step="0.1" min="0" required>
      </div>
      
      <div class="form-group">
        <label for="spacingCol">列间距 (波长):</label>
        <input type="number" id="spacingCol" v-model="formData.spacing_col" step="0.1" min="0" required>
      </div>
      
      <div class="form-group">
        <label for="rotateZ">Z轴旋转角度 (度):</label>
        <input type="number" id="rotateZ" v-model="formData.rotate_z" required>
      </div>
      
      <div class="form-group">
        <label for="rotateY">Y轴旋转角度 (度):</label>
        <input type="number" id="rotateY" v-model="formData.rotate_y" required>
      </div>
      
      <div class="form-group">
        <label for="rotateX">X轴旋转角度 (度):</label>
        <input type="number" id="rotateX" v-model="formData.rotate_x" required>
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
import { ref } from 'vue';
import axios from 'axios';

export default {
  name: 'Antenna',
  setup() {
    const formData = ref({
      antenna_type: 'uniform_plane',
      name: '测试天线',
      num_per_row: 8,
      num_per_col: 8,
      spacing_row: 0.5,
      spacing_col: 0.5,
      rotate_z: 0,
      rotate_y: 0,
      rotate_x: 0
    });
    
    const loading = ref(false);
    const responseData = ref('');
    const responseClass = ref('');

    const submitAntennaConfig = async () => {
      loading.value = true;
      responseData.value = '请求中...';
      responseClass.value = '';
      
      try {
        const response = await axios.post('http://localhost:5000/api/antenna', formData.value);
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
      loading,
      responseData,
      responseClass,
      submitAntennaConfig
    };
  }
}
</script>