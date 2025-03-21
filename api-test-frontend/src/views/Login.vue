<!-- filepath: api-test-frontend/src/views/Login.vue -->
<template>
  <div class="login form-container">
    <h2>用户登录</h2>
    <form @submit.prevent="login">
      <div class="form-group">
        <label for="username">用户名:</label>
        <input type="text" id="username" v-model="username" required>
      </div>
      
      <div class="form-group">
        <label for="password">密码:</label>
        <input type="password" id="password" v-model="password" required>
      </div>
      
      <button type="submit" :disabled="loading">{{ loading ? '登录中...' : '登录' }}</button>
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
  name: 'Login',
  setup() {
    const username = ref('');
    const password = ref('');
    const loading = ref(false);
    const responseData = ref('');
    const responseClass = ref('');

    const login = async () => {
      loading.value = true;
      responseData.value = '请求中...';
      responseClass.value = '';
      
      try {
        const response = await axios.post('http://localhost:5000/api/login', {
          username: username.value,
          password: password.value
        });
        
        responseData.value = JSON.stringify(response.data, null, 2);
        responseClass.value = 'success';
        
        // 存储用户ID或token
        if (response.data.user_id) {
          localStorage.setItem('auth_token', response.data.user_id);
        }
        
        // 清空表单
        username.value = '';
        password.value = '';
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
      loading,
      responseData,
      responseClass,
      login
    };
  }
}
</script>