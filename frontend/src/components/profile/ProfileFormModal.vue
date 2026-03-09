<template>
  <div v-if="show" class="modal-overlay" @click.self="close">
    <div class="modal-container">
      <div class="modal-header">
        <h3>{{ isEditing ? 'Редактировать профиль' : 'Создать профиль' }}</h3>
        <button class="close-btn" @click="close">&times;</button>
      </div>

      <form @submit.prevent="submitForm">
        <!-- Поле имени -->
        <div class="form-group">
          <label>Имя</label>
          <input
            v-model="form.name"
            type="text"
            required
            minlength="2"
            maxlength="15"
            placeholder="Введите имя"
          />
        </div>

        <!-- Город -->
        <div class="form-group">
          <label>Город</label>
          <input
            v-model="form.city"
            type="text"
            required
            minlength="2"
            maxlength="100"
            placeholder="Введите город"
          />
        </div>

        <!-- Возраст -->
        <div class="form-group">
          <label>Возраст</label>
          <input
            v-model.number="form.age"
            type="number"
            required
            min="13"
            placeholder="Ваш возраст"
          />
        </div>

        <!-- Пол -->
        <div class="form-group">
          <label>Пол</label>
          <select v-model="form.gender" required>
            <option value="" disabled>Выберите пол</option>
            <option value="male">Мужской</option>
            <option value="female">Женский</option>
          </select>
        </div>

        <!-- Фото -->
        <div class="form-group">
          <label>Фото профиля</label>
          <div class="file-input">
            <input
              type="file"
              accept="image/*"
              @change="handleFileChange"
              ref="fileInput"
            />
            <button type="button" class="file-btn" @click="triggerFileInput">
              <i class="fas fa-upload"></i> Выберите файл
            </button>
            <span v-if="photoFile" class="file-name">{{ photoFile.name }}</span>
          </div>
          <div v-if="photoPreview" class="photo-preview">
            <img :src="photoPreview" alt="preview" />
          </div>
        </div>

        <!-- Ошибки -->
        <div v-if="error" class="error-message">{{ error }}</div>

        <!-- Кнопки -->
        <div class="modal-actions">
          <button type="button" class="btn-secondary" @click="close" :disabled="saving">
            Отмена
          </button>
          <button type="submit" class="btn-primary" :disabled="saving">
            <span v-if="saving">Сохранение...</span>
            <span v-else>{{ isEditing ? 'Сохранить' : 'Создать' }}</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'

const props = defineProps({
  show: Boolean,
  initialData: Object
})

const emit = defineEmits(['close', 'saved'])

// Базовый URL API
const API_BASE_URL = 'http://localhost:8000'

// Состояние формы
const form = ref({
  name: '',
  city: '',
  age: null,
  gender: ''
})

const photoFile = ref(null)
const photoPreview = ref(null)
const saving = ref(false)
const error = ref(null)
const fileInput = ref(null)

// Определяем, редактирование ли это
const isEditing = computed(() => props.initialData !== null)

// При изменении initialData или show обновляем форму
watch(
  () => [props.show, props.initialData],
  ([newShow, newData]) => {
    if (newShow) {
      if (newData) {
        // Редактирование: заполняем форму данными профиля
        form.value = {
          name: newData.name || '',
          city: newData.city || '',
          age: newData.age || null,
          gender: newData.gender || ''
        }
        // Если есть фото, показываем предпросмотр
        if (newData.photo_url) {
          photoPreview.value = newData.photo_url
        } else {
          photoPreview.value = null
        }
      } else {
        // Создание: очищаем форму
        form.value = { name: '', city: '', age: null, gender: '' }
        photoPreview.value = null
      }
      photoFile.value = null
      error.value = null
    }
  },
  { immediate: true }
)

// Выбор файла
const handleFileChange = (e) => {
  const file = e.target.files[0]
  if (file) {
    photoFile.value = file
    // Создаём preview
    const reader = new FileReader()
    reader.onload = (e) => {
      photoPreview.value = e.target.result
    }
    reader.readAsDataURL(file)
  } else {
    photoFile.value = null
    photoPreview.value = null
  }
}

const triggerFileInput = () => {
  fileInput.value.click()
}

// Закрытие модалки
const close = () => {
  emit('close')
}

// Отправка формы
const submitForm = async () => {
  // Простейшая валидация
  if (!form.value.name || !form.value.city || !form.value.age || !form.value.gender) {
    error.value = 'Заполните все поля'
    return
  }
  if (form.value.age < 13) {
    error.value = 'Возраст должен быть больше 12 лет'
    return
  }

  saving.value = true
  error.value = null

  try {
    // Формируем FormData
    const formData = new FormData()
    
    // Добавляем JSON с данными профиля в поле user_data
    formData.append('user_data', JSON.stringify(form.value))
    
    // Добавляем фото, если выбрано новое
    if (photoFile.value) {
      formData.append('photo', photoFile.value)
    }

    const response = await fetch(`${API_BASE_URL}/api/profile/create`, {
      method: 'POST',
      credentials: 'include', // КРИТИЧЕСКИ ВАЖНО: отправляем cookie
      // НЕ указываем Content-Type - браузер сам установит правильный boundary для FormData
      body: formData
    })

    if (response.status === 401) {
      // Не авторизован - перенаправляем на логин
      window.location.href = '/login'
      return
    }

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    emit('saved', data)
  } catch (err) {
    console.error('Ошибка сохранения профиля:', err)
    error.value = err.message || 'Ошибка сохранения профиля'
  } finally {
    saving.value = false
  }
}
</script>

<!-- Стили остаются теми же -->
<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
}

.modal-container {
  background: white;
  border-radius: 30px;
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(50px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 30px;
  border-bottom: 1px solid #f0f0f0;
}

.modal-header h3 {
  margin: 0;
  font-size: 24px;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 28px;
  cursor: pointer;
  color: #999;
  transition: color 0.2s;
}

.close-btn:hover {
  color: #333;
}

form {
  padding: 30px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #555;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 12px 15px;
  border: 2px solid #e0e0e0;
  border-radius: 50px;
  font-size: 16px;
  transition: border-color 0.3s;
  box-sizing: border-box;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #764ba2;
}

.file-input {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.file-input input[type="file"] {
  display: none;
}

.file-btn {
  background: #f0f0f0;
  border: 2px solid #e0e0e0;
  padding: 10px 20px;
  border-radius: 50px;
  cursor: pointer;
  font-size: 16px;
  color: #555;
  transition: all 0.2s;
}

.file-btn:hover {
  background: #e0e0e0;
}

.file-name {
  color: #666;
  font-size: 14px;
  word-break: break-all;
}

.photo-preview {
  margin-top: 15px;
  text-align: center;
}

.photo-preview img {
  max-width: 200px;
  max-height: 200px;
  border-radius: 20px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}

.error-message {
  background: #ffebee;
  color: #c62828;
  padding: 10px 20px;
  border-radius: 50px;
  margin-bottom: 20px;
  text-align: center;
}

.modal-actions {
  display: flex;
  gap: 15px;
  justify-content: flex-end;
}

.btn-primary, .btn-secondary {
  padding: 12px 30px;
  border: none;
  border-radius: 50px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.2);
}

.btn-secondary {
  background: #f0f0f0;
  color: #666;
}

.btn-secondary:hover:not(:disabled) {
  background: #e0e0e0;
}

.btn-primary:disabled, .btn-secondary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>