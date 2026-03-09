<template>
  <div class="profile-page">
    <!-- Загрузка -->
    <div v-if="loading" class="loader">Загрузка...</div>

    <!-- Ошибка -->
    <div v-else-if="error" class="error-message">
      {{ error }}
      <button @click="fetchProfile">Повторить</button>
    </div>

    <!-- Нет профиля -->
    <div v-else-if="!profile" class="no-profile">
      <p>У вас ещё нет профиля.</p>
      <button class="btn-primary" @click="openCreateModal">Создать профиль</button>
    </div>

    <!-- Профиль есть -->
    <div v-else class="profile-card">
      <div class="profile-header">
        <div class="avatar">
          <img :src="profile.photo || '/default-avatar.png'" alt="avatar" />
        </div>
        <div class="profile-actions">
          <button class="edit-btn" @click="openEditModal" title="Редактировать профиль">
            <i class="fas fa-pencil-alt"></i>
          </button>
        </div>
      </div>

      <div class="profile-info">
        <h2>{{ profile.name }}, {{ profile.age }}</h2>
        <p><i class="fas fa-map-marker-alt"></i> {{ profile.city }}</p>
        <p><i class="fas fa-venus-mars"></i> {{ genderLabel(profile.gender) }}</p>
      </div>
    </div>

    <!-- Модальное окно создания/редактирования -->
    <ProfileFormModal
      :show="showModal"
      :initial-data="editingProfile"
      @close="closeModal"
      @saved="handleProfileSaved"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import ProfileFormModal from './ProfileFormModal.vue'

// Состояние
const profile = ref(null)
const loading = ref(true)
const error = ref(null)
const showModal = ref(false)
const editingProfile = ref(null)

// Базовый URL API
const API_BASE_URL = 'http://localhost:8000'

// Функция загрузки профиля
const fetchProfile = async () => {
  loading.value = true
  error.value = null
  
  try {
    const response = await fetch(`${API_BASE_URL}/api/profile`, {
      method: 'GET',
      credentials: 'include', // КРИТИЧЕСКИ ВАЖНО: отправляем cookie
      headers: {
        'Content-Type': 'application/json',
        // НЕ добавляем Authorization - токен в cookie
      }
    })

    if (response.status === 401) {
      // Не авторизован - перенаправляем на логин
      window.location.href = '/login'
      return
    }

    if (response.status === 404) {
      // Профиль не найден
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

// Открыть создание профиля
const openCreateModal = () => {
  editingProfile.value = null
  showModal.value = true
}

// Открыть редактирование профиля
const openEditModal = () => {
  editingProfile.value = profile.value
  showModal.value = true
}

// Закрыть модалку
const closeModal = () => {
  showModal.value = false
  editingProfile.value = null
}

// Обработчик успешного сохранения профиля
const handleProfileSaved = (updatedProfile) => {
  profile.value = updatedProfile
  closeModal()
}

// Вспомогательная функция для отображения пола
const genderLabel = (gender) => {
  const map = {
    male: 'Мужской',
    female: 'Женский',
    other: 'Другой'
  }
  return map[gender] || gender
}

// Загружаем профиль при монтировании
onMounted(() => {
  fetchProfile()
})
</script>

<!-- Стили остаются теми же -->
<style scoped>
.profile-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.loader, .error-message, .no-profile {
  background: white;
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.1);
  text-align: center;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 12px 30px;
  border-radius: 50px;
  font-size: 16px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  margin-top: 20px;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.2);
}

.profile-card {
  background: white;
  border-radius: 30px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.2);
  overflow: hidden;
  max-width: 500px;
  width: 100%;
}

.profile-header {
  position: relative;
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

.profile-actions {
  position: absolute;
  top: 20px;
  right: 20px;
}

.edit-btn {
  background: white;
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #764ba2;
  font-size: 18px;
  cursor: pointer;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
  transition: transform 0.2s;
}

.edit-btn:hover {
  transform: scale(1.1);
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
</style>