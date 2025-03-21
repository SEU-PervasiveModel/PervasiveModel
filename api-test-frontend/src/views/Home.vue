<!-- filepath: api-test-frontend/src/views/Home.vue -->
<template>
  <div class="home">
    <h2>API 测试工具</h2>
    <p>这是一个用于测试后端 API 的前端界面。请使用导航菜单选择要测试的功能。</p>
    
    <div v-if="authToken" class="user-info">
      <p>已登录</p>
      <button @click="logout">登出</button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';

export default {
  name: 'Home',
  setup() {
    const authToken = ref(localStorage.getItem('auth_token'));

    const logout = () => {
      localStorage.removeItem('auth_token');
      authToken.value = null;
    };

    return {
      authToken,
      logout
    };
  }
}
</script>