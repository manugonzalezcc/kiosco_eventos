# kiosco_eventos

Sistema web para la gestión de kioscos en eventos, desarrollado con Vue.js (frontend) y Python/Litestar + SQLAlchemy (backend).

---

## Características principales

- **Gestión de kioscos:** crear, listar, eliminar y administrar kioscos.
- **Registro de ventas:** por producto, responsable y kiosco.
- **Gestión de productos:** añadir, actualizar stock, eliminar productos.
- **Control de responsables:** asignación de responsables y historial de turnos.
- **Registro de inversiones:** inversión inicial por kiosco.
- **Panel administrativo:** estadísticas en tiempo real de ventas y productos.
- **Autenticación de usuarios:** inicio de sesión y control de acceso.

---

## Tecnologías utilizadas

| Categoría     | Tecnologías                                  |
|---------------|----------------------------------------------|
| Frontend      | Vue.js 3, Vite, Composition API, CSS         |
| Backend       | Python 3, Litestar, SQLAlchemy, Pydantic     |
| Base de datos | PostgreSQL (puede adaptarse a SQLite)        |
| Otros         | Git, VS Code                                 |

---

## Instalación y ejecución

### 1. Clona el repositorio

```sh
git clone https://github.com/manugonzalezcc/kiosco_eventos.git
cd kiosco_eventos
```

### 2. Backend

**Requisitos:**
- Python 3.11+
- PostgreSQL (o SQLite para pruebas)

**Pasos:**
```sh
cd app-backend
pip install -r requirements.txt
python init_db.py  # Inicializa la base de datos
uvicorn app.main:app --reload  # Ejecuta el servidor
```
Configura la conexión a la base de datos en `config.py`.

### 3. Frontend

**Requisitos:**
- Node.js 18+
- npm

**Pasos:**
```sh
cd app-frontend/kiosco_eventos
npm install
npm run dev
```
Accede en [http://localhost:5173](http://localhost:5173)

---

## Estructura del proyecto

```
kiosco_eventos/
├── app-backend/
│   ├── app/
│   │   ├── main.py
│   │   └── services/
│   │       ├── kiosco/
│   │       ├── producto/
│   │       ├── turno/
│   │       ├── usuario/
│   │       └── venta/
│   ├── models/
│   ├── config.py
│   ├── database.py
│   └── init_db.py
└── app-frontend/
    └── kiosco_eventos/
        ├── src/
        │   ├── views/
        │   ├── components/
        │   ├── router/
        │   └── main.ts
        ├── public/
        ├── package.json
        └── README.md
```

---

## Uso básico

- Inicia backend y frontend.
- Accede a [http://localhost:5173](http://localhost:5173).
- Inicia sesión como administrador o responsable.
- Crea kioscos, añade productos, registra ventas.
- Visualiza estadísticas y gestiona el kiosco desde el panel.

---

## Personalización

- Modifica modelos: `app-backend/models/`
- Estilos: `app-frontend/kiosco_eventos/src/style.css`
- Configuración base de datos: `app-backend/config.py`

---

## Contribuciones

¡Se aceptan sugerencias y mejoras!  
Haz un fork, crea tu rama (`git checkout -b mejora-nombre`) y envía un pull request.

---

## Autor

Manuel González  
[GitHub](https://github.com/manugonzalezcc)

---
