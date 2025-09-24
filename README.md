# Project AI Manager

Un sistema inteligente de gestión de proyectos que utiliza IA para proporcionar insights, análisis de riesgos y predicciones de progreso.

## 🚀 Características

### Backend (FastAPI)
- **API RESTful** con FastAPI
- **Autenticación JWT** segura
- **Base de datos SQLAlchemy** con SQLite
- **Integración con OpenAI** para análisis inteligente
- **Análisis de IA**:
  - Evaluación de riesgos del proyecto
  - Predicciones de progreso
  - Análisis de rendimiento del equipo
  - Pronósticos de presupuesto

### Frontend (React + TypeScript)
- **React 18** con TypeScript
- **Tailwind CSS** para estilos modernos
- **React Router** para navegación
- **Tanstack Query** para gestión de estado del servidor
- **Zustand** para gestión de estado local
- **React Hook Form** con validación Zod
- **Recharts** para visualización de datos

## 📋 Funcionalidades

### Gestión de Proyectos
- ✅ Crear, editar y eliminar proyectos
- ✅ Seguimiento de estado y progreso
- ✅ Gestión de presupuesto y fechas
- ✅ Filtrado y búsqueda avanzada

### Gestión de Tareas
- ✅ Crear y asignar tareas
- ✅ Establecer prioridades y fechas límite
- ✅ Seguimiento de progreso
- ✅ Estados personalizables

### Dashboard Inteligente
- ✅ Estadísticas en tiempo real
- ✅ Gráficos de progreso
- ✅ Resumen de proyectos recientes
- ✅ Alertas de tareas vencidas

### Insights de IA
- 🤖 Análisis de riesgos automático
- 📈 Predicciones de progreso
- 👥 Análisis de rendimiento del equipo
- 💰 Pronósticos de presupuesto

## 🛠️ Tecnologías

### Backend
- **FastAPI** - Framework web moderno y rápido
- **SQLAlchemy** - ORM para Python
- **Pydantic** - Validación de datos
- **OpenAI API** - Integración de IA
- **JWT** - Autenticación segura
- **Uvicorn** - Servidor ASGI

### Frontend
- **React 18** - Biblioteca de UI
- **TypeScript** - Tipado estático
- **Vite** - Herramienta de construcción
- **Tailwind CSS** - Framework de CSS
- **React Router** - Enrutamiento
- **Tanstack Query** - Gestión de estado del servidor
- **Zustand** - Gestión de estado
- **React Hook Form** - Gestión de formularios
- **Zod** - Validación de esquemas
- **Recharts** - Gráficos y visualizaciones
- **Lucide React** - Iconos

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.8+
- Node.js 16+
- npm o yarn

### Backend

1. **Navegar al directorio del backend**
   ```bash
   cd backend
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\\Scripts\\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   ```bash
   cp .env.example .env
   ```
   
   Editar `.env` con tus configuraciones:
   ```env
   DATABASE_URL=sqlite:///./project_manager.db
   SECRET_KEY=tu-clave-secreta-aqui
   OPENAI_API_KEY=tu-api-key-de-openai  # Opcional
   ```

5. **Ejecutar el servidor**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
   ```

   El backend estará disponible en: http://localhost:8001
   Documentación API: http://localhost:8001/docs

### Frontend

1. **Navegar al directorio del frontend**
   ```bash
   cd frontend
   ```

2. **Instalar dependencias**
   ```bash
   npm install
   ```

3. **Ejecutar el servidor de desarrollo**
   ```bash
   npm run dev
   ```

   El frontend estará disponible en: http://localhost:3001

## 📁 Estructura del Proyecto

```
project-ai-manager/
├── backend/
│   ├── app/
│   │   ├── models/          # Modelos de base de datos
│   │   ├── routes/          # Endpoints de la API
│   │   ├── services/        # Lógica de negocio
│   │   ├── database.py      # Configuración de BD
│   │   └── main.py          # Aplicación principal
│   ├── requirements.txt     # Dependencias Python
│   └── .env.example         # Variables de entorno
├── frontend/
│   ├── src/
│   │   ├── components/      # Componentes React
│   │   ├── pages/           # Páginas de la aplicación
│   │   ├── services/        # Servicios y API
│   │   ├── App.tsx          # Componente principal
│   │   └── main.tsx         # Punto de entrada
│   ├── package.json         # Dependencias Node.js
│   └── vite.config.ts       # Configuración Vite
└── README.md
```

## 🔧 Configuración de Desarrollo

### Variables de Entorno del Backend

```env
# Base de datos
DATABASE_URL=sqlite:///./project_manager.db

# Seguridad
SECRET_KEY=tu-clave-secreta-muy-segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# IA (Opcional)
OPENAI_API_KEY=tu-api-key-de-openai
OPENAI_MODEL=gpt-3.5-turbo

# Email (Opcional)
MAIL_USERNAME=tu-email@ejemplo.com
MAIL_PASSWORD=tu-contraseña-de-email
MAIL_FROM=tu-email@ejemplo.com
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com

# Entorno
ENVIRONMENT=development
```

## 📊 API Endpoints

### Autenticación
- `POST /api/v1/auth/register` - Registro de usuario
- `POST /api/v1/auth/login` - Inicio de sesión

### Proyectos
- `GET /api/v1/projects/` - Listar proyectos
- `POST /api/v1/projects/` - Crear proyecto
- `GET /api/v1/projects/{id}` - Obtener proyecto
- `PUT /api/v1/projects/{id}` - Actualizar proyecto
- `DELETE /api/v1/projects/{id}` - Eliminar proyecto

### Tareas
- `GET /api/v1/tasks/` - Listar tareas
- `POST /api/v1/tasks/` - Crear tarea
- `GET /api/v1/tasks/{id}` - Obtener tarea
- `PUT /api/v1/tasks/{id}` - Actualizar tarea
- `DELETE /api/v1/tasks/{id}` - Eliminar tarea

### IA Insights
- `POST /api/v1/ai-insights/analyze-project/{id}` - Análisis completo
- `GET /api/v1/ai-insights/project/{id}/risk-assessment` - Evaluación de riesgos
- `GET /api/v1/ai-insights/project/{id}/progress-prediction` - Predicción de progreso

## 🎯 Uso

1. **Registro/Login**: Crea una cuenta o inicia sesión
2. **Dashboard**: Visualiza el resumen de tus proyectos
3. **Proyectos**: Crea y gestiona tus proyectos
4. **Tareas**: Organiza las tareas de cada proyecto
5. **IA Insights**: Obtén análisis inteligentes de tus proyectos

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🔮 Roadmap

- [ ] Notificaciones en tiempo real
- [ ] Integración con calendarios
- [ ] Reportes avanzados
- [ ] Colaboración en equipo
- [ ] Aplicación móvil
- [ ] Integración con herramientas de terceros

## 📞 Soporte

Si tienes alguna pregunta o problema, por favor abre un issue en el repositorio.

---

**Desarrollado con ❤️ usando FastAPI y React**