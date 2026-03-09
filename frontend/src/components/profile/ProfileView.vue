<template>
  <div class="profile-view-page">
    <!-- Кнопка назад -->
    <button class="back-btn" @click="goBack">
      <i class="fas fa-arrow-left"></i> Назад
    </button>

    <!-- Загрузка -->
    <div v-if="loading" class="loader">Загрузка профиля...</div>

    <!-- Ошибка -->
    <div v-else-if="error" class="error-message">
      {{ error }}
      <button @click="fetchProfile" class="btn-primary">Повторить</button>
    </div>

    <!-- Профиль не найден -->
    <div v-else-if="!profile" class="not-found">
      <p>Профиль не найден</p>
      <button class="btn-primary" @click="goBack">Вернуться</button>
    </div>

    <!-- Профиль найден -->
    <div v-else class="profile-card">
      <div class="profile-header">
        <div class="avatar">
          <img 
            :src="profile.photo || '/default-avatar.png'" 
            alt="avatar"
            @error="handleImageError"
          />
        </div>
      </div>

      <div class="profile-info">
        <h2>{{ profile.name }}, {{ profile.age }}</h2>
        <p><i class="fas fa-map-marker-alt"></i> {{ profile.city }}</p>
        <p><i class="fas fa-venus-mars"></i> {{ genderLabel(profile.gender) }}</p>
        
        <!-- Кнопка действия (например, написать сообщение) -->
        <div class="action-buttons">
          <button class="btn-primary" @click="sendMessage">
            <i class="fas fa-comment"></i> Написать сообщение
          </button>
          <button class="btn-secondary" @click="likeProfile">
            <i class="fas fa-heart"></i> Поставить лайк
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const profile = ref(null)
const loading = ref(true)
const error = ref(null)

const API_BASE_URL = 'http://localhost:8000'

// Получаем ID из URL параметров
const userId = route.params.id

const fetchProfile = async () => {
  loading.value = true
  error.value = null
  
  try {
    const response = await fetch(`${API_BASE_URL}/api/profile/${userId}`, {
      credentials: 'include'
    })

    if (response.status === 401) {
      // Не авторизован - перенаправляем на логин
      router.push('/login')
      return
    }

    if (response.status === 404) {
      profile.value = null
      return
    }

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    profile.value = data
  } catch (err) {
    console.error('Ошибка загрузки профиля:', err)
    error.value = 'Не удалось загрузить профиль. Попробуйте позже.'
  } finally {
    loading.value = false
  }
}

const goBack = () => {
  router.back()
}

const handleImageError = (e) => {
  e.target.src = '/default-avatar.png'
}

const genderLabel = (gender) => {
  const map = {
    male: 'Мужской',
    female: 'Женский',
    other: 'Другой'
  }
  return map[gender] || gender
}

const sendMessage = () => {
  alert(`Написать сообщение пользователю ${profile.value.name}`)
  // Здесь будет переход к чату
}

const likeProfile = () => {
  alert(`Лайк для ${profile.value.name}`)
  // Здесь будет API для лайка
}

onMounted(() => {
  if (userId) {
    fetchProfile()
  } else {
    error.value = 'ID пользователя не указан'
    loading.value = false
  }
})
</script>

<style scoped>
.profile-view-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  position: relative;
}

.back-btn {
  position: absolute;
  top: 20px;
  left: 20px;
  background: white;
  border: none;
  padding: 10px 20px;
  border-radius: 50px;
  font-size: 16px;
  cursor: pointer;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
  display: flex;
  align-items: center;
  gap: 8px;
  transition: transform 0.2s;
}

.back-btn:hover {
  transform: translateX(-5px);
}

.loader, .error-message, .not-found {
  background: white;
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.1);
  text-align: center;
  max-width: 500px;
  margin: 50px auto;
}

.profile-card {
  background: white;
  border-radius: 30px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.2);
  overflow: hidden;
  max-width: 500px;
  margin: 50px auto;
}

.profile-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 30px 20px;
  text-align: center;
}

.avatar {
  width: 120px;
  height: 120px;
  margin: 0 auto;
  border-radius: 50%;
  overflow: hidden;
  border: 4px solid white;
  box-shadow: 0 4px 10px rgba(0,0,0,0.2);
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.profile-info {
  padding: 30px;
  text-align: center;
}

.profile-info h2 {
  margin: 0 0 10px;
  font-size: 28px;
  color: #333;
}

.profile-info p {
  margin: 10px 0;
  color: #666;
  font-size: 18px;
}

.profile-info i {
  margin-right: 10px;
  color: #764ba2;
}

.action-buttons {
  display: flex;
  gap: 15px;
  justify-content: center;
  margin-top: 30px;
}

.btn-primary, .btn-secondary {
  padding: 12px 30px;
  border: none;
  border-radius: 50px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.2);
}

.btn-secondary {
  background: #f0f0f0;
  color: #666;
}

.btn-secondary:hover {
  background: #e0e0e0;
  transform: translateY(-2px);
}
</style>