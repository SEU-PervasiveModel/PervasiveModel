<!-- filepath: api-test-frontend/src/views/Register.vue -->
<template>
  <div class="register form-container">
    <h2>用户注册</h2>
    <form @submit.prevent="register">
      <div class="form-group">
        <label for="username">用户名:</label>
        <input type="text" id="username" v-model="username" required>
      </div>
      
      <div class="form-group">
        <label for="password">密码:</label>
        <input type="password" id="password" v-model="password" required>
      </div>
      
      <div class="form-group">
        <label for="email">邮箱 (可选):</label>
        <input type="email" id="email" v-model="email">
      </div>
      
      <button type="submit" :disabled="loading">{{ loading ? '注册中...' : '注册' }}</button>
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
  name: 'Register',
  setup() {
    const username = ref('');
    const password = ref('');
    const email = ref('');
    const loading = ref(false);
    const responseData = ref('');
    const responseClass = ref('');

    const register = async () => {
      loading.value = true;
      responseData.value = '请求中...';
      responseClass.value = '';
      
      try {
        const response = await axios.post('http://localhost:5000/api/register', {
          username: username.value,
          password: password.value,
          email: email.value || ''
        });
        
        responseData.value = JSON.stringify(response.data, null, 2);
        responseClass.value = 'success';
        
        // 清空表单
        username.value = '';
        password.value = '';
        email.value = '';
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
      username,
      password,
      email,
      loading,
      responseData,
      responseClass,
      register
    };
  }
}
</script>