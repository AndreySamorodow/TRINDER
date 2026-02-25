<template>
  <div class="auth-container">
    <div class="auth-card">
      <h1 class="logo">TRINDER</h1>
      <form @submit.prevent="handleLogin" class="auth-form">
        <div class="input-group">
          <input 
            type="email" 
            v-model="email" 
            placeholder="Электронная почта"
            required
          />
        </div>
        
        <div class="input-group">
          <input 
            type="password" 
            v-model="password" 
            placeholder="Пароль"
            required
          />
        </div>
        
        <button type="submit" class="login-btn">Войти</button>
      </form>
      
      <div class="separator">
        <span>или</span>
      </div>
      
      <button class="google-btn" @click="loginWithGoogle">
        <img src="../assets/google.webp" width="20" height="20" alt="Google" />
        Войти через Google
      </button>
      
      <div class="register-link">
        <a href="#">Зарегистрироваться</a>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: '',
      password: ''
    }
  },
  methods: {
    handleLogin() {
      console.log('Login attempt with:', this.email, this.password);
    },
    loginWithGoogle() {
      window.location.href = 'http://localhost:8000/api/oauth/google/url';
    }
  }
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
  overflow: hidden;
}

.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100vw;
  background: #1a1a1a;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.auth-card {
  background: #2d2d2d;
  padding: 50px 40px;
  width: 100%;
  max-width: 420px;
  text-align: center;
  border-radius: 30px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
}

.logo {
  color: #ff99cc;
  font-size: 3rem;
  margin-bottom: 5px;
  font-weight: 700;
  letter-spacing: 2px;
}

.auth-form {
  margin-bottom: 20px;
}

.input-group {
  margin-bottom: 15px;
}

.input-group input {
  width: 100%;
  padding: 16px 20px;
  background: #3d3d3d;
  border: none;
  border-radius: 30px;
  font-size: 1rem;
  box-sizing: border-box;
  color: white;
  transition: all 0.2s;
}

.input-group input:focus {
  outline: none;
  background: #454545;
  box-shadow: 0 0 0 2px rgba(255, 153, 204, 0.3);
}

.input-group input::placeholder {
  color: #777;
}

.login-btn {
  width: 100%;
  padding: 16px 20px;
  background: #ff99cc;
  color: #1a1a1a;
  border: none;
  border-radius: 30px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  margin-top: 10px;
}

.login-btn:hover {
  background: #ff80b5;
  transform: scale(1.02);
}

.separator {
  display: flex;
  align-items: center;
  text-align: center;
  color: #777;
  margin: 20px 0;
}

.separator::before,
.separator::after {
  content: '';
  flex: 1;
  border-bottom: 1px solid #444;
}

.separator span {
  padding: 0 15px;
  font-size: 0.9rem;
}

.google-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  width: 100%;
  padding: 16px 20px;
  background: white;
  color: #333;
  border: none;
  border-radius: 30px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  margin-bottom: 25px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.google-btn:hover {
  background: #f5f5f5;
  transform: scale(1.02);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.15);
}

.google-btn img {
  width: 22px;
  height: 22px;
}

.register-link a {
  color: #ff99cc;
  text-decoration: none;
  font-size: 1rem;
  font-weight: 500;
  transition: all 0.2s;
}

.register-link a:hover {
  color: #ff80b5;
  text-decoration: underline;
}
</style>