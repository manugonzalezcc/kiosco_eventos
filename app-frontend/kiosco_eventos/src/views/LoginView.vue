<template>
  <div class="login-page">
    <div class="kiosco-banner">
      <h1 class="titulo-kiosco">KIOSCO</h1>
    </div>
    <div class="login-container">
      <h2>Iniciar sesión</h2>
      <form @submit.prevent="login">
        <input v-model="username" placeholder="Usuario" required />
        <input v-model="password" type="password" placeholder="Contraseña" required />
        <button type="submit">Entrar</button>
      </form>
      <p v-if="loginError" class="error">{{ loginError }}</p>
      <button @click="mostrarRegistro = true" style="margin-bottom: 12px;">
        ¿No tienes cuenta? Regístrate
      </button>
      <!-- Modal Registro -->
      <div v-if="mostrarRegistro" class="modal">
        <h2>Registrarse</h2>
        <form @submit.prevent="register">
          <input v-model="regUsername" placeholder="Usuario" required />
          <input v-model="regPassword" type="password" placeholder="Contraseña" required />
          <button type="submit">Registrar</button>
          <button type="button" @click="mostrarRegistro = false">Cancelar</button>
        </form>
        <p v-if="registerError" class="error">{{ registerError }}</p>
        <p v-if="registerSuccess" class="success">{{ registerSuccess }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const username = ref('')
const password = ref('')
const regUsername = ref('')
const regPassword = ref('')
const loginError = ref('')
const registerError = ref('')
const registerSuccess = ref('')
const mostrarRegistro = ref(false)

async function login() {
  loginError.value = ''
  if (!username.value || !password.value) {
    loginError.value = 'Usuario y contraseña son obligatorios'
    return
  }
  try {
    const res = await fetch('http://localhost:8000/usuarios/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: username.value, password: password.value }),
    })
    const data = await res.json()
    if (data.msg === 'Inicio de sesión exitoso') {
      localStorage.setItem('usuario', username.value)
      window.location.href = '/kiosco-inicio'
    } else {
      loginError.value = data.msg || 'Usuario o contraseña incorrectos'
    }
  } catch (err) {
    loginError.value = 'Error de conexión con el servidor'
  }
}

async function register() {
  registerError.value = ''
  registerSuccess.value = ''
  if (!regUsername.value || !regPassword.value) {
    registerError.value = 'Usuario y contraseña son obligatorios'
    return
  }
  try {
    const res = await fetch('http://localhost:8000/usuarios/registro', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: regUsername.value, password: regPassword.value }),
    })
    const data = await res.json()
    if (data.msg === 'Usuario registrado') {
      registerSuccess.value = '¡Usuario registrado correctamente!'
      registerError.value = ''
      mostrarRegistro.value = false // <-- Cierra el modal automáticamente
    } else {
      registerError.value = data.msg || 'No se pudo registrar el usuario'
    }
  } catch (err) {
    registerError.value = 'Error de conexión con el servidor'
  }
}

function toggleRegistro() {
  mostrarRegistro.value = !mostrarRegistro.value
}

onMounted(() => {
  if (localStorage.getItem('usuario')) {
    window.location.href = '/kiosco-inicio'
  }

  window.onpopstate = function () {
    if (localStorage.getItem('usuario')) {
      if (window.confirm('¿Seguro que quieres cerrar sesión y volver al login?')) {
        localStorage.removeItem('usuario')
        window.location.href = '/login'
      } else {
        window.history.forward()
      }
    }
  }
})
</script>

<style scoped>
body {
  min-height: 100vh;
  background: repeating-linear-gradient(
    180deg,           /* Rayas horizontales */
    #e3e7ee 0px,      /* Raya clara */
    #e3e7ee 120px,    /* Ancho de la raya clara */
    #2e3a59 120px,    /* Raya azul oscuro */
    #2e3a59 240px     /* Ancho de la raya azul */
  );
  font-family: 'Segoe UI', Arial, sans-serif;
  color: #222;
}

.login-page {
  position: relative;
  max-width: 520px;
  margin: 60px auto;
}

.kiosco-banner {
  background: linear-gradient(90deg, #2e3a59 60%, #4f5b7a 100%);
  border-radius: 36px;
  padding: 40px 0 140px 0; /* Menos espacio arriba */
  box-shadow: 0 8px 32px rgba(46,58,89,0.18);
  text-align: center;
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 700px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start; /* Alinea arriba */
}

.titulo-kiosco {
  font-size: 5rem; /* Mucho más grande */
  font-weight: 900;
  color: #fff;
  margin: 0;
  letter-spacing: 2px;
  text-transform: uppercase;
  line-height: 1.1;
}

.login-container {
  background: #fff;
  border-radius: 0 0 24px 24px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.12);
  padding: 32px 24px;
  text-align: center;
  position: absolute;
  top: 140px; /* Ajusta para que el blanco quede adelante del azul */
  left: 50%;
  transform: translateX(-50%);
  width: 80%; /* Más angosto que el banner azul */
  z-index: 2;
}

h2 {
  color: #2e3a59;
  margin-bottom: 24px;
  font-size: 1.5rem;
  font-weight: 600;
}

form {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 18px;
}

input {
  padding: 10px;
  border-radius: 4px;
  border: 1px solid #104962;
  font-size: 1rem;
}

button {
  background: #2e3a59;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 12px 24px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;
}
button:hover {
  background: #1b2236;
}

.error {
  color: #d32f2f;
  font-weight: 500;
  margin-top: 8px;
}
.success {
  color: #388e3c;
  font-weight: 500;
  margin-top: 8px;
}

.modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: #fff;
  border: 2px solid #2e3a59;
  border-radius: 12px;
  padding: 32px 24px;
  z-index: 1000;
  box-shadow: 0 8px 32px rgba(0,0,0,0.18);
  min-width: 320px;
}

.modal h2 {
  margin-bottom: 16px;
}

.modal form {
  background: #fff;
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.2);
}
</style>