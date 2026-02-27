<template>
  <div class="auth-container">
    <div class="auth-card">
      <h1 class="logo">TRINDER</h1>
      
      <!-- Сообщение об ошибке -->
      <div v-if="error" class="error-message">{{ error }}</div>
      
      <form @submit.prevent="handleLogin" class="auth-form">
        <div class="input-group">
          <input 
            type="email" 
            v-model="email" 
            placeholder="Электронная почта"
            required
            :disabled="loading"
          />
        </div>
        
        <div class="input-group">
          <input 
            type="password" 
            v-model="password" 
            placeholder="Пароль"
            required
            :disabled="loading"
          />
        </div>
        
        <button type="submit" class="login-btn" :disabled="loading">
          {{ loading ? 'Вход...' : 'Войти' }}
        </button>
      </form>
      
      <div class="separator">
        <span>или</span>
      </div>
      
      <button class="google-btn" @click="loginWithGoogle" :disabled="loading">
        <svg width="20" height="20" viewBox="0 0 24 24">
          <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
          <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
          <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
          <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
        </svg>
        Войти через Google
      </button>
      
      <div class="register-link">
        <router-link to="/register">Зарегистрироваться</router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: '',
      password: '',
      loading: false,
      error: ''
    }
  },
  methods: {
    async handleLogin() {
      this.loading = true
      this.error = ''
      
      try {
        const response = await fetch('http://localhost:8000/api/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            email: this.email,
            password: this.password,
            oauth: false
          }),
          credentials: 'include' // для отправки cookies
        })
        
        const data = await response.json()
        
        if (!response.ok) {
          throw new Error(data.detail || 'Ошибка при входе')
        }
        
        // Сохраняем токен если есть
        if (data.access_token) {
          localStorage.setItem('token', data.access_token)
        }
        
        // Перенаправляем на главную
        window.location.href = '/dashboard'
        
      } catch (err) {
        this.error = err.message
      } finally {
        this.loading = false
      }
    },
    
    loginWithGoogle() {
      window.location.href = 'http://localhost:8000/api/oauth/google/url'
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

.input-group input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
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

.login-btn:hover:not(:disabled) {
  background: #ff80b5;
  transform: scale(1.02);
}

.login-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
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

.google-btn:hover:not(:disabled) {
  background: #f5f5f5;
  transform: scale(1.02);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.15);
}

.google-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.google-btn svg {
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

.error-message {
  background: rgba(255, 87, 87, 0.2);
  color: #ff5757;
  padding: 12px;
  border-radius: 30px;
  margin-bottom: 20px;
  font-size: 0.9rem;
  border: 1px solid rgba(255, 87, 87, 0.3);
}
</style>