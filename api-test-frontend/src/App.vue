<template>
  <div class="app-container">
    <header>
      <h1>后端 API 测试界面</h1>
      <nav>
        <router-link to="/">首页</router-link> |
        <router-link to="/register">注册</router-link> |
        <router-link to="/login">登录</router-link> |
        <router-link to="/matlab">MATLAB计算</router-link> |
        <router-link to="/track">轨迹管理</router-link> |
        <router-link to="/antenna">天线配置</router-link>
      </nav>
    </header>
    <main>
      <router-view></router-view>
    </main>

    <footer>
      <p>API 状态: <span :class="apiStatus.class">{{ apiStatus.text }}</span></p>
    </footer>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';

export default {
  name: 'App',
  setup() {
    const apiStatus = ref({ text: '检查中...', class: 'status-checking' });

    onMounted(async () => {
  try {
    // 首先尝试一个简单的HEAD请求
    await axios.head('http://localhost:5000/api');
    apiStatus.value = { text: '已连接', class: 'status-connected' };
  } catch (error) {
    console.error('详细错误信息:', error);
    apiStatus.value = { text: '未连接', class: 'status-disconnected' };
  }
});

    return {
      apiStatus
    };
  }
}
</script>

<style>
.app-container {
  font-family: Arial, sans-serif;
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

header {
  margin-bottom: 30px;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

nav {
  margin-top: 15px;
}

nav a {
  margin: 0 10px;
  text-decoration: none;
  color: #2c3e50;
  font-weight: bold;
}

nav a.router-link-exact-active {
  color: #42b983;
}

footer {
  margin-top: 40px;
  padding-top: 10px;
  border-top: 1px solid #eee;
  text-align: center;
  font-size: 0.9em;
  color: #666;
}

.status-connected {
  color: green;
}

.status-disconnected {
  color: red;
}

.status-checking {
  color: orange;
}

.form-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.response-container {
  margin-top: 20px;
  padding: 10px;
  border: 1px solid #eee;
  border-radius: 5px;
  background-color: #f9f9f9;
  min-height: 100px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input, select {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
  border: 1px solid #ddd;
  border-radius: 4px;
}

button {
  background-color: #42b983;
  color: white;
  border: none;
  padding: 10px 15px;
  cursor: pointer;
  border-radius: 4px;
  font-size: 16px;
}

button:hover {
  background-color: #3aa876;
}

.success {
  color: green;
}

.error {
  color: red;
}

pre {
  white-space: pre-wrap;
  word-break: break-word;
}
</style>
