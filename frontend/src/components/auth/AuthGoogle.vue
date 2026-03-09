<template>
  <div class="auth-redirect">
    <div class="loader">Авторизация через Google...</div>
  </div>
</template>

<script>
export default {
  name: 'AuthGoogle',
  mounted() {
    const queryParams = new URLSearchParams(window.location.search);
    const code = queryParams.get('code');
    const state = queryParams.get('state');

    if (code && state) {
      // Отправляем данные на бэкенд
      fetch('http://localhost:8000/api/oauth/google/callback', {
        body: JSON.stringify({ code, state }),
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include' // Важно для получения/установки cookie
      })
        .then(res => {
          if (!res.ok) {
            throw new Error('Ошибка авторизации');
          }
          // Бэкенд сам установит cookie, мы просто редиректим
          window.location.href = '/';
        })
        .catch(err => {
          console.error('Ошибка:', err);
          window.location.href = '/login?error=auth_failed';
        });
    } else {
      // Нет code или state - ошибка
      window.location.href = '/login?error=missing_params';
    }
  }
};
</script>

<style scoped>
.auth-redirect {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.loader {
  background: white;
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.1);
  text-align: center;
  font-size: 18px;
  color: #333;
  animation: fade 1.5s infinite;
}

@keyframes fade {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}
</style>