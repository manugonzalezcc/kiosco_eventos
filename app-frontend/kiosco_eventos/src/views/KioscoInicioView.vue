<template>
  <div class="admin-top">
    <button v-if="!esAdmin" @click="mostrarAdmin = true">Modo administrador</button>
    <button v-if="esAdmin" @click="salirAdmin">Salir de modo admin</button>
  </div>
  <div class="inicio-kiosco">
    <h2>Iniciar un kiosco</h2>
    <form @submit.prevent="iniciarKiosco">
      <input v-model="nombre" placeholder="Nombre del kiosco" required />
      <input v-model="responsable" placeholder="Responsable" required />
      <button type="submit">Iniciar</button>
    </form>
    <p v-if="msg" class="msg-confirmacion">{{ msg }}</p>

    <div class="botones-inicio">
      <button @click="cerrarSesion">Cerrar sesión</button>
      <button v-if="esAdmin" @click="mostrarKioscos = true">Ver kioscos creados</button>
    </div>

    <div v-if="mostrarAdmin" class="modal">
      <h3>Acceso administrador</h3>
      <form @submit.prevent="loginAdmin">
        <input v-model="adminPassword" type="password" placeholder="Contraseña de admin" required />
        <button type="submit">Ingresar</button>
        <button type="button" @click="mostrarAdmin = false">Cancelar</button>
      </form>
      <p v-if="msgAdmin">{{ msgAdmin }}</p>
    </div>

    <!-- Modal de kioscos -->
    <div v-if="mostrarKioscos" class="modal">
      <div class="modal-kioscos">
        <h3>Kioscos creados</h3>
        <ul class="kioscos-lista">
          <li v-for="k in kioscos" :key="k.id" @click="seleccionarKiosco(k)" class="kiosco-item">
            <strong>{{ k.nombre }}</strong>
            <span style="color:#888;">
              - Responsable: {{ k.responsable }}<br>
              - Fecha: {{ k.fecha_inicio }}
            </span>
          </li>
        </ul>
        <button @click="mostrarKioscos = false" style="margin-top:12px;">Volver</button>
      </div>
    </div>

    <!-- Modal de detalle de kiosco -->
    <div v-if="kioscoSeleccionado" class="modal">
      <div class="modal-detalle">
        <h3>Detalle de "{{ kioscoSeleccionado.nombre }}"</h3>
        <p>
          <strong>Responsable:</strong> {{ kioscoSeleccionado.responsable }}<br>
          <strong>Fecha:</strong> {{ kioscoSeleccionado.fecha_inicio }}
        </p>
        <ul>
          <li v-for="v in ventasKiosco" :key="v.id">
            {{ v.cantidad }} x {{ v.producto }} - ${{ v.precio }} (Total: ${{ v.cantidad * v.precio }})
          </li>
        </ul>
        <p><strong>Total ventas:</strong> ${{ totalVentas }}</p>
        <form @submit.prevent="registrarInversion">
          <input v-model.number="inversion" type="number" min="0" placeholder="Ingresar inversión" required />
          <button type="submit">Registrar inversión</button>
        </form>
        <p v-if="inversionRegistrada !== null" class="ganancia"><strong>Ganancia:</strong> ${{ totalVentas - inversionRegistrada }}</p>
        <button @click="cerrarDetalleKiosco">Cerrar</button>
        <button v-if="esAdmin" @click="eliminarKiosco" style="background:#d32f2f;margin-top:12px;">Eliminar kiosco</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'

const nombre = ref('')
const responsable = ref('')
const msg = ref('')
const mostrarAdmin = ref(false)
const adminPassword = ref('')
const msgAdmin = ref('')
const mostrarKioscos = ref(false)
const kioscos = ref([])
const esAdmin = ref(false)
const kioscoSeleccionado = ref(null)
const ventasKiosco = ref([])
const totalVentas = ref(0)
const inversion = ref(0)
const inversionRegistrada = ref(null)

async function cargarKioscos() {
  const res = await fetch('http://localhost:8000/kioscos/listar')
  kioscos.value = await res.json()
}

watch(mostrarKioscos, (val) => {
  if (val) cargarKioscos()
})

onMounted(() => {
  if (!localStorage.getItem('usuario')) {
    window.location.href = '/login'
  }

  window.onpopstate = function () {
    // Si el usuario vuelve al login desde el inicio, pregunta si quiere cerrar sesión
    if (window.location.pathname === '/login' && localStorage.getItem('usuario')) {
      if (window.confirm('¿Seguro que quieres cerrar sesión y volver al login?')) {
        localStorage.removeItem('usuario')
        window.location.href = '/login'
      } else {
        window.history.forward()
      }
    }
  }

  // Verificar si el usuario es admin
  esAdmin.value = localStorage.getItem('usuario') === 'admin'
})

async function iniciarKiosco() {
  if (!nombre.value || !responsable.value) {
    msg.value = 'Todos los campos son obligatorios'
    return
  }
  const res = await fetch('http://localhost:8000/kioscos/iniciar', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      nombre: nombre.value,
      responsable: responsable.value,
      fecha_inicio: new Date().toISOString()
    }),
  })
  const data = await res.json();
if (data.msg === 'Kiosco iniciado correctamente' && data.id) {
  localStorage.setItem('kiosco_id', data.id);
  localStorage.setItem('usuario', responsable.value);
  window.location.href = '/kiosco-panel';
}
}

function cerrarSesion() {
  if (window.confirm('¿Seguro que quieres cerrar sesión?')) {
    localStorage.removeItem('usuario')
    window.location.href = '/login'
  }
}

async function loginAdmin() {
  if (adminPassword.value === '12345') {
    esAdmin.value = true
    mostrarAdmin.value = false
    msgAdmin.value = ''
  } else {
    mostrarAdmin.value = false
    msgAdmin.value = 'Contraseña incorrecta'
  }
}

async function seleccionarKiosco(kiosco) {
  kioscoSeleccionado.value = kiosco
  // Obtén las ventas de ese kiosco desde el backend
  const res = await fetch(`http://localhost:8000/ventas/kiosco/${kiosco.id}`)
  ventasKiosco.value = await res.json()
  totalVentas.value = ventasKiosco.value.reduce((acc, v) => acc + v.cantidad * v.precio, 0)
  inversion.value = 0
  inversionRegistrada.value = null
}

function cerrarDetalleKiosco() {
  kioscoSeleccionado.value = null
}

async function registrarInversion() {
  if (!kioscoSeleccionado.value) return
  const res = await fetch('http://localhost:8000/kioscos/registrar-inversion', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      kiosco_id: kioscoSeleccionado.value.id,
      inversion: inversion.value
    }),
  })
  const data = await res.json()
  inversionRegistrada.value = inversion.value
  // Opcional: mostrar mensaje data.msg
}

async function eliminarKiosco() {
  if (!kioscoSeleccionado.value) return
  if (!window.confirm('¿Seguro que quieres eliminar este kiosco?')) return
  const res = await fetch('http://localhost:8000/kioscos/eliminar', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id: kioscoSeleccionado.value.id }),
  })
  const data = await res.json()
  msg.value = data.msg
  kioscoSeleccionado.value = null
  mostrarKioscos.value = true
  await cargarKioscos()
}

function salirAdmin() {
  esAdmin.value = false
}
</script>

<style scoped>
body, .inicio-kiosco {
  background: #f4f6f8;
  font-family: 'Segoe UI', Arial, sans-serif;
  color: #222;
}

.inicio-kiosco {
  max-width: 400px;
  margin: 60px auto;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.08);
  padding: 32px 24px;
  text-align: center;
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
}

input {
  padding: 10px;
  border-radius: 4px;
  border: 1px solid #cfd8dc;
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

p {
  color: #2e3a59;
  font-weight: 500;
  margin-top: 10px;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal h3 {
  color: #fff;
  margin-bottom: 16px;
  font-size: 1.25rem;
  font-weight: 500;
}

.modal form {
  background: #2e3a59;
  padding: 24px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.modal input {
  background: #fff;
  color: #222;
}

.modal button {
  background: #1b2236;
}

.modal ul {
  list-style: none;
  padding: 0;
  margin: 0;
  color: #fff;
  text-align: left;
}

.modal li {
  margin-bottom: 8px;
}

.admin-top {
  position: absolute;
  top: 32px;
  right: 32px;
  z-index: 10;
}

.admin-top button {
  background: #2e3a59;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 10px 20px;
  font-size: 1rem;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(46,58,89,0.10);
  transition: background 0.2s;
}
.admin-top button:hover {
  background: #1b2236;
}

.msg-admin-error {
  color: #d32f2f;
  background: #fdecea;
  border-radius: 6px;
  padding: 10px 0;
  margin-bottom: 16px;
  font-weight: 600;
}

.msg-confirmacion {
  color: #388e3c;
  background: #eafaf1;
  border-radius: 6px;
  padding: 10px 0;
  margin-bottom: 16px;
  font-weight: 600;
  text-align: center;
}

.modal-kioscos, .modal-detalle {
  background: #fff;
  padding: 32px 24px;
  border-radius: 12px;
  min-width: 320px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.18);
  text-align: center;
}

.kiosco-item {
  cursor: pointer;
  padding: 8px 0;
  border-bottom: 1px solid #eee;
  transition: background 0.2s;
}
.kiosco-item:hover {
  background: #e3e7ee;
}

.modal-detalle {
  background: #2e3a59;
  padding: 24px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  color: #fff;
}

.modal-detalle ul {
  list-style: none;
  padding: 0;
  margin: 0;
  color: #fff;
  text-align: left;
}

.modal-detalle li {
  margin-bottom: 8px;
}

.ganancia {
  color: #388e3c;
  background: #fff;
  border-radius: 6px;
  padding: 8px 0;
  margin: 12px 0;
  font-weight: 600;
}

.kioscos-lista {
  max-height: 270px;
  overflow-y: auto;
  padding-right: 6px;
  min-width: 220px;
  margin-bottom: 16px;
}

.kioscos-lista span {
  color: #2e3a59 !important;
  font-size: 0.98rem;
}

.botones-inicio {
  display: flex;
  flex-direction: column;
  gap: 16px;
  align-items: center;
  margin-top: 24px;
}
</style>