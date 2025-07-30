<template>
  <div class="volver-inicio">
    <button @click="irInicio">Volver al inicio</button>
  </div>
  <div class="panel-kiosco">
    <div class="panel-titulo">
      <h1 class="titulo-panel">Panel Kiosco</h1>
    </div>
    <div class="acciones">
      <button @click="mostrarProducto = true">Añadir producto</button>
      <button @click="mostrarVenta = true">Registrar venta</button>
      <button @click="mostrarStock = true">Actualizar stock</button>
      <button @click="mostrarResponsable = true">Cambiar responsable</button>
    </div>

    <!-- Modal Añadir Producto -->
    <div v-if="mostrarProducto" class="modal">
      <h3>Añadir producto</h3>
      <form @submit.prevent="agregarProducto">
        <input v-model="nombreProducto" placeholder="Nombre" required />
        <input v-model.number="cantidadProducto" type="number" min="1" placeholder="Cantidad" required />
        <input v-model.number="precioProducto" type="number" min="0" step="0.01" placeholder="Precio" required />
        <button type="submit">Agregar</button>
        <button type="button" @click="mostrarProducto = false">Cancelar</button>
      </form>
      <p v-if="msgProducto">{{ msgProducto }}</p>
    </div>

    <!-- Modal Registrar Venta -->
    <div v-if="mostrarVenta" class="modal">
      <h3>Registrar venta</h3>
      <form @submit.prevent="registrarVenta">
        <select v-model="nombreVenta" required>
          <option disabled value="">Selecciona producto</option>
          <option v-for="p in productos" :key="p.id" :value="p.nombre">
            {{ p.nombre }} (Stock: {{ p.cantidad }})
          </option>
        </select>
        <input v-model.number="cantidadVenta" type="number" min="1" placeholder="Cantidad" required />
        <button type="submit">Registrar venta</button>
        <button type="button" @click="mostrarVenta = false">Cancelar</button>
      </form>
      <p v-if="msgVenta">{{ msgVenta }}</p>
    </div>

    <!-- Modal Actualizar Stock -->
    <div v-if="mostrarStock" class="modal">
      <h3>Actualizar stock</h3>
      <form @submit.prevent="actualizarStock">
        <select v-model="nombreStock" required>
          <option disabled value="">Selecciona producto</option>
          <option v-for="p in productos" :key="p.id" :value="p.nombre">
            {{ p.nombre }} (Stock: {{ p.cantidad }})
          </option>
        </select>
        <input v-model.number="cantidadStock" type="number" min="1" placeholder="Cantidad a añadir" required />
        <button type="submit">Actualizar</button>
        <button type="button" @click="eliminarProducto">Eliminar stock</button>
        <button type="button" @click="eliminarProductoCompleto">Eliminar producto</button>
        <button type="button" @click="mostrarStock = false">Cancelar</button>
      </form>
      <p v-if="msgStock">{{ msgStock }}</p>
    </div>

    <!-- Modal Cambiar Responsable -->
    <div v-if="mostrarResponsable" class="modal">
      <h3>Cambiar responsable</h3>
      <form @submit.prevent="cambiarResponsable">
        <input v-model="nuevoResponsable" placeholder="Nuevo responsable" required />
        <button type="submit">Registrar cambio</button>
        <button type="button" @click="mostrarResponsable = false">Cancelar</button>
      </form>
      <p v-if="msgResponsable">{{ msgResponsable }}</p>
    </div>

    <div class="panel-grid">
      <div>
        <h3>Productos</h3>
        <ul class="productos-lista">
          <li v-for="p in productos" :key="p.id">
            {{ p.nombre }} (Stock: {{ p.cantidad }}) - ${{ p.precio }}
          </li>
        </ul>
      </div>
      <div>
        <h3>Ventas</h3>
        <ul class="ventas-lista">
          <li v-for="v in ventas" :key="v.id" class="venta-item">
            {{ v.cantidad }} x {{ v.producto }} - ${{ v.precio }}
            <span class="eliminar-venta" @click="confirmarEliminarVenta(v.id)">✖</span>
          </li>
        </ul>
        <p v-if="msgVentaEliminar">{{ msgVentaEliminar }}</p>
      </div>
      <div>
        <h3>Responsable actual</h3>
        <p class="responsable-actual">{{ responsableActual }}</p>
        <h3>Responsables</h3>
        <ul class="responsables-lista">
          <li v-for="r in responsables" :key="r.id">
            {{ r.nombre }} <span style="color:#888;">({{ r.hora }})</span>
          </li>
        </ul>
      </div>
    </div>

    <div class="panel-grid panel-ventas">
      <div>
        <h3>Ventas del responsable actual</h3>
        <ul class="ventas-lista">
          <li v-for="v in ventas.filter(v => v.responsable === responsableActual)" :key="v.id">
            {{ v.cantidad }} x {{ v.producto }} - ${{ v.precio }}
          </li>
        </ul>
      </div>
      <div>
        <h3>Ventas por responsable</h3>
        <select v-model="responsableSeleccionado">
          <option disabled value="">Selecciona responsable</option>
          <option v-for="r in responsables" :key="r.id" :value="r.nombre">
            {{ r.nombre }} ({{ r.hora }})
          </option>
        </select>
        <ul class="ventas-lista">
          <li v-for="v in ventas.filter(v => v.responsable === responsableSeleccionado)" :key="v.id">
            {{ v.cantidad }} x {{ v.producto }} - ${{ v.precio }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

// Modales
const mostrarProducto = ref(false)
const mostrarVenta = ref(false)
const mostrarStock = ref(false)
const mostrarResponsable = ref(false)

// Añadir producto
const nombreProducto = ref('')
const cantidadProducto = ref(1)
const precioProducto = ref(0)
const msgProducto = ref('')

async function agregarProducto() {
  const res = await fetch('http://localhost:8000/productos/agregar', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      nombre: nombreProducto.value,
      cantidad: cantidadProducto.value,
      precio: precioProducto.value
    }),
  })
  msgProducto.value = (await res.json()).msg
  mostrarProducto.value = false

  await recargarTodo()
}

// Registrar venta
const nombreVenta = ref('')
const cantidadVenta = ref(1)
const msgVenta = ref('')
const msgVentaEliminar = ref('')

async function registrarVenta() {
  const producto = productos.value.find(p => p.nombre === nombreVenta.value)
  if (!producto) {
    msgVenta.value = "Producto no encontrado"
    return
  }
  if (cantidadVenta.value > producto.cantidad) {
    msgVenta.value = "No puedes vender más de lo que hay en stock"
    return
  }
  const res = await fetch('http://localhost:8000/ventas/registrar', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      nombre: nombreVenta.value,
      cantidad: cantidadVenta.value,
      responsable: responsableActual.value,
      kiosco_id: kioscoId.value // <-- así sí está definido
    }),
  })
  msgVenta.value = (await res.json()).msg
  mostrarVenta.value = false

  await cargarVentas()
  const resProductos = await fetch('http://localhost:8000/productos/listar')
  productos.value = await resProductos.json()
}

// Actualizar stock
const nombreStock = ref('')
const cantidadStock = ref(1)
const msgStock = ref('')

async function actualizarStock() {
  const res = await fetch('http://localhost:8000/productos/actualizar-stock', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      nombre: nombreStock.value,
      cantidad: cantidadStock.value
    }),
  })
  msgStock.value = (await res.json()).msg
  mostrarStock.value = false

  const resProductos = await fetch('http://localhost:8000/productos/listar')
  productos.value = await resProductos.json()
}

// Cambiar responsable
const nuevoResponsable = ref('')
const msgResponsable = ref('')
const responsableActual = ref('')
const responsableSeleccionado = ref('')

async function cambiarResponsable() {
  const kioscoId = 1 // Reemplaza por el ID real del kiosco
  const res = await fetch('http://localhost:8000/turnos/cambiar', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      kiosco_id: kioscoId,
      responsable: nuevoResponsable.value,
      hora_inicio: new Date().toISOString()
    }),
  })
  msgResponsable.value = (await res.json()).msg
  mostrarResponsable.value = false

  responsableActual.value = nuevoResponsable.value

  await cargarResponsables()
}

// Tipos de datos
interface Producto {
  id: number
  nombre: string
  cantidad: number
  precio: number
}

interface Venta {
  id: number
  cantidad: number
  producto: string
  precio: number
  responsable: string
}

interface Responsable {
  id: number
  nombre: string
  hora: string
}

// Listar productos
const productos = ref<Producto[]>([])
const ventas = ref<Venta[]>([])
const responsables = ref<Responsable[]>([])
const kioscoId = ref<number | null>(null);

onMounted(async () => {
  const resProductos = await fetch('http://localhost:8000/productos/listar')
  productos.value = await resProductos.json()
  await cargarVentas()
  await cargarResponsables()
  if (!localStorage.getItem('usuario')) {
    window.location.href = '/login'
  }
  // Inicializa responsableActual con el usuario logueado
  responsableActual.value = localStorage.getItem('usuario') || ''
  // Supón que guardas el id del kiosco en localStorage al iniciar
  kioscoId.value = Number(localStorage.getItem('kiosco_id'));
  // Si no lo tienes, deberías guardarlo al iniciar el kiosco
})

async function cargarVentas() {
  const res = await fetch('http://localhost:8000/ventas/listar')
  ventas.value = await res.json()
}

async function cargarResponsables() {
  const res = await fetch('http://localhost:8000/turnos/listar')
  responsables.value = await res.json()
}

async function recargarTodo() {
  await cargarVentas()
  await cargarResponsables()
  const resProductos = await fetch('http://localhost:8000/productos/listar')
  productos.value = await resProductos.json()
}

async function eliminarProducto() {
  const producto = productos.value.find(p => p.nombre === nombreStock.value)
  if (!producto) {
    msgStock.value = "Producto no encontrado"
    return
  }
  if (cantidadStock.value > producto.cantidad) {
    msgStock.value = "No puedes eliminar más stock del disponible"
    return
  }
  if (!window.confirm(`¿Seguro que quieres eliminar ${cantidadStock.value} unidades de "${producto.nombre}"?`)) return;

  const res = await fetch('http://localhost:8000/productos/eliminar-stock', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ nombre: nombreStock.value, cantidad: cantidadStock.value }),
  })
  msgStock.value = (await res.json()).msg
  mostrarStock.value = false
  await recargarTodo()
}

async function eliminarProductoCompleto() {
  const producto = productos.value.find(p => p.nombre === nombreStock.value)
  if (!producto) {
    msgStock.value = "Producto no encontrado"
    return
  }
  if (!window.confirm(`¿Seguro que quieres eliminar el producto "${producto.nombre}" por completo?`)) return;

  const res = await fetch('http://localhost:8000/productos/eliminar', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ nombre: nombreStock.value }),
  })
  msgStock.value = (await res.json()).msg
  mostrarStock.value = false
  await recargarTodo()
}

async function confirmarEliminarVenta(id: number) {
  if (window.confirm('¿Seguro que quieres eliminar esta venta?')) {
    const res = await fetch('http://localhost:8000/ventas/eliminar', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id }),
    })
    const data = await res.json()
    msgVentaEliminar.value = data.msg
    await cargarVentas()
    // Opcional: limpiar el mensaje después de unos segundos
    setTimeout(() => { msgVentaEliminar.value = '' }, 2500)
  }
}

// Cerrar sesión al cerrar la pestaña
window.onpopstate = function () {
  if (window.confirm('¿Seguro que quieres cerrar sesión y volver al login?')) {
    localStorage.removeItem('usuario')
    window.location.href = '/login'
  } else {
    window.history.forward()
  }
}

function irInicio() {
  if (window.confirm('¿Seguro que quieres volver al inicio?')) {
    window.location.href = "/";
  }
}
</script>

<style scoped>
body, .panel-kiosco {
  background: #f4f6f8;
  font-family: 'Segoe UI', Arial, sans-serif;
  color: #222;
}

.panel-kiosco {
  max-width: 1100px;
  margin: 40px auto;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 24px rgba(46,58,89,0.08);
  padding: 32px 24px;
}

.panel-titulo {
  width: 100%;
  background: linear-gradient(90deg, #2e3a59 60%, #4f5b7a 100%);
  padding: 40px 0 30px 0;
  border-radius: 32px; /* Todas las esquinas redondeadas */
  text-align: center;
  margin-bottom: 32px;
  box-shadow: 0 4px 24px rgba(46,58,89,0.10);
}

.titulo-panel {
  font-size: 3.5rem;
  font-weight: 900;
  color: #fff;
  margin: 0;
  letter-spacing: 2px;
  text-transform: uppercase;
}

.acciones {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 32px;
}

.acciones button {
  background: #2e3a59;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 12px 24px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;
}
.acciones button:hover {
  background: #1b2236;
}

.panel-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;
  margin-bottom: 32px;
}

.panel-ventas {
  grid-template-columns: 1fr 1fr;
  gap: 32px;
}

.listas {
  margin-top: 32px;
  display: flex;
  gap: 40px;
  justify-content: center;
  flex-wrap: wrap;
}

.listas > div, .listas ul {
  min-width: 220px;
}

.listas h3 {
  color: #2e3a59;
  margin-bottom: 8px;
  font-size: 1.1rem;
  font-weight: 600;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  background: #f4f6f8;
  margin-bottom: 6px;
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 0.98rem;
}

select, input {
  margin-bottom: 10px;
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #cfd8dc;
  width: 100%;
  font-size: 1rem;
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

.modal h3 {
  color: #2e3a59;
  margin-bottom: 18px;
  text-align: center;
}

.modal button {
  background: #2e3a59;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 10px 18px;
  font-size: 1rem;
  margin-right: 8px;
  margin-top: 8px;
  cursor: pointer;
  transition: background 0.2s;
}
.modal button:hover {
  background: #1b2236;
}

.modal input, .modal select {
  margin-bottom: 12px;
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #cfd8dc;
  width: 100%;
  font-size: 1rem;
}

p {
  text-align: center;
  color: #2e3a59;
  font-weight: 500;
  margin-top: 10px;
}

.ventas-lista {
  max-height: 270px; /* Aproximadamente 6 elementos de 45px */
  overflow-y: auto;
  padding-right: 6px;
  min-width: 220px;
}

.productos-lista {
  max-height: 270px; /* Aproximadamente 6 elementos */
  overflow-y: auto;
  padding-right: 6px;
  min-width: 220px;
}

.responsables-lista {
  max-height: 270px;
  overflow-y: auto;
  padding-right: 6px;
  min-width: 220px;
  list-style: none;
}

.venta-item {
  position: relative;
}

.eliminar-venta {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #d32f2f;
  font-weight: bold;
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.2s;
}

.venta-item:hover .eliminar-venta {
  opacity: 1;
}

.responsable-actual {
  background: #e3e7ee;
  color: #2e3a59;
  font-weight: 700;
  border-radius: 6px;
  padding: 8px 12px;
  margin-bottom: 12px;
  text-align: center;
  word-break: break-word;
}

.volver-inicio {
  position: absolute;
  top: 32px;
  left: 32px;
  z-index: 10;
}

.volver-inicio button {
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
.volver-inicio button:hover {
  background: #1b2236;
}
</style>