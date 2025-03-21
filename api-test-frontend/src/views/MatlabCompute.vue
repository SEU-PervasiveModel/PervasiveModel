<!-- filepath: api-test-frontend/src/views/MatlabCompute.vue -->
<template>
  <div class="matlab-compute form-container">
    <h2>MATLAB 计算测试</h2>
    <form @submit.prevent="computeWithMatlab">
      <div class="form-group">
        <label>输入值类型:</label>
        <div>
          <input type="radio" id="single" value="single" v-model="inputType">
          <label for="single">单个值</label>
          
          <input type="radio" id="array" value="array" v-model="inputType">
          <label for="array">数组</label>
        </div>
      </div>
      
      <div class="form-group" v-if="inputType === 'single'">
        <label for="singleValue">数值:</label>
        <input type="number" id="singleValue" v-model="singleValue" step="any">
      </div>
      
      <div class="form-group" v-if="inputType === 'array'">
        <label for="arrayValues">数组值 (逗号分隔):</label>
        <input type="text" id="arrayValues" v-model="arrayValuesString" placeholder="例如: 1,2,3,4">
      </div>
      
      <button type="submit" :disabled="loading">{{ loading ? '计算中...' : '计算' }}</button>
    </form>
    
    <div class="response-container">
      <h3>响应结果:</h3>
      <pre :class="responseClass">{{ responseData }}</pre>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue';
import axios from 'axios';

export default {
  name: 'MatlabCompute',
  setup() {
    const inputType = ref('single');
    const singleValue = ref(5);
    const arrayValuesString = ref('1,2,3,4,5');
    const loading = ref(false);
    const responseData = ref('');
    const responseClass = ref('');
    
    const arrayValues = computed(() => {
      if (!arrayValuesString.value) return [];
      return arrayValuesString.value.split(',').map(v => parseFloat(v.trim())).filter(v => !isNaN(v));
    });

    const computeWithMatlab = async () => {
      loading.value = true;
      responseData.value = '请求中...';
      responseClass.value = '';
      
      const values = inputType.value === 'single' ? singleValue.value : arrayValues.value;
      
      try {
        const response = await axios.post('http://localhost:5000/api/matlab-compute', {
          values: values
        });
        
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
      inputType,
      singleValue,
      arrayValuesString,
      loading,
      responseData,
      responseClass,
      computeWithMatlab
    };
  }
}
</script>