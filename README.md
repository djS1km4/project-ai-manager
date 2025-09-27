# 🚀 Project AI Manager

<div align="center">

![Project AI Manager](https://img.shields.io/badge/Project-AI%20Manager-blue?style=for-the-badge&logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

**Un sistema inteligente de gestión de proyectos potenciado por IA**

[Demo en Vivo](#) • [Documentación](#) • [Reportar Bug](mailto:djs1km4@gmail.com) • [Solicitar Feature](mailto:djs1km4@gmail.com)

</div>

---

## 📋 Tabla de Contenidos

- [🎯 Descripción](#-descripción)
- [✨ Características](#-características)
- [🛠️ Tecnologías](#️-tecnologías)
- [🚀 Instalación Rápida](#-instalación-rápida)
- [📖 Instalación Detallada](#-instalación-detallada)
- [🐳 Despliegue con Docker](#-despliegue-con-docker)
- [📁 Estructura del Proyecto](#-estructura-del-proyecto)
- [🔧 Configuración](#-configuración)
- [📊 API Documentation](#-api-documentation)
- [🎮 Uso](#-uso)
- [📸 Capturas de Pantalla](#-capturas-de-pantalla)
- [🤝 Contribución](#-contribución)
- [📝 Licencia](#-licencia)

---

## 🎯 Descripción

**Project AI Manager** es una aplicación web moderna de gestión de proyectos que integra inteligencia artificial para proporcionar insights avanzados, análisis de riesgos y predicciones de progreso. Diseñada para equipos que buscan optimizar su productividad y tomar decisiones basadas en datos.

### 🌟 ¿Por qué Project AI Manager?

- **🤖 IA Integrada**: Análisis automático de riesgos y predicciones de progreso
- **📊 Dashboard Inteligente**: Visualizaciones en tiempo real de métricas clave
- **🎨 UI/UX Moderna**: Interfaz elegante y responsive con Tailwind CSS
- **⚡ Alto Rendimiento**: Backend optimizado con FastAPI y frontend con React 18
- **🔒 Seguro**: Autenticación JWT y validación robusta de datos

---

## ✨ Características

### 🎯 Gestión de Proyectos
- ✅ **CRUD Completo**: Crear, leer, actualizar y eliminar proyectos
- ✅ **Seguimiento de Estado**: Monitoreo en tiempo real del progreso
- ✅ **Gestión de Presupuesto**: Control financiero integrado
- ✅ **Filtrado Avanzado**: Búsqueda y filtros inteligentes
- ✅ **Fechas y Plazos**: Gestión completa de cronogramas

### 📋 Gestión de Tareas
- ✅ **Asignación de Tareas**: Sistema completo de asignación
- ✅ **Prioridades**: Clasificación por importancia y urgencia
- ✅ **Estados Personalizables**: Workflow adaptable a tu equipo
- ✅ **Fechas Límite**: Control de vencimientos y alertas
- ✅ **Progreso Visual**: Indicadores de avance en tiempo real

### 🤖 Insights de IA
- 🧠 **Análisis de Riesgos**: Evaluación automática de factores de riesgo
- 📈 **Predicciones de Progreso**: Estimaciones basadas en datos históricos
- 👥 **Análisis de Rendimiento**: Métricas de productividad del equipo
- 💰 **Pronósticos de Presupuesto**: Predicciones financieras inteligentes
- 📊 **Reportes Automáticos**: Generación de insights periódicos

### 📊 Dashboard y Analytics
- 📈 **Métricas en Tiempo Real**: KPIs actualizados constantemente
- 🎯 **Gráficos Interactivos**: Visualizaciones con Recharts
- 🚨 **Alertas Inteligentes**: Notificaciones de tareas críticas
- 📅 **Vista de Calendario**: Planificación visual de proyectos

---

## 🛠️ Tecnologías

<div align="center">

### Backend
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat-square&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=flat-square&logo=sqlalchemy&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat-square&logo=postgresql&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=flat-square&logo=openai&logoColor=white)

### Frontend
![React](https://img.shields.io/badge/React-20232A?style=flat-square&logo=react&logoColor=61DAFB)
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=flat-square&logo=typescript&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=flat-square&logo=vite&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=flat-square&logo=tailwind-css&logoColor=white)
![React Query](https://img.shields.io/badge/React_Query-FF4154?style=flat-square&logo=react-query&logoColor=white)

### DevOps & Tools
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat-square&logo=github&logoColor=white)

</div>

---

## 🚀 Instalación Rápida

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/project-ai-manager.git
cd project-ai-manager

# Ejecutar script de instalación automática
chmod +x setup.sh
./setup.sh

# O en Windows
setup.bat
```

La aplicación estará disponible en:
- **Frontend**: http://localhost:5173
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 📖 Instalación Detallada

### 📋 Prerrequisitos

- **Python 3.8+** ([Descargar](https://python.org))
- **Node.js 16+** ([Descargar](https://nodejs.org))
- **Git** ([Descargar](https://git-scm.com))

### 🔧 Backend Setup

```bash
# 1. Navegar al directorio backend
cd backend

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones

# 6. Ejecutar migraciones (si aplica)
alembic upgrade head

# 7. Iniciar servidor
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### ⚛️ Frontend Setup

```bash
# 1. Navegar al directorio frontend
cd frontend

# 2. Instalar dependencias
npm install

# 3. Iniciar servidor de desarrollo
npm run dev
```

---

## 🐳 Despliegue con Docker

### 🚀 Despliegue Rápido

```bash
# Construir y ejecutar con Docker Compose
docker-compose up --build -d

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down
```

### 🔧 Configuración Docker

El proyecto incluye:
- `Dockerfile` para backend
- `Dockerfile` para frontend  
- `docker-compose.yml` para orquestación
- `docker-compose.prod.yml` para producción

---

## 📁 Estructura del Proyecto

```
project-ai-manager/
├── 📁 backend/
│   ├── 📁 app/
│   │   ├── 📁 models/          # Modelos SQLAlchemy
│   │   ├── 📁 routes/          # Endpoints FastAPI
│   │   ├── 📁 services/        # Lógica de negocio
│   │   ├── 📁 utils/           # Utilidades
│   │   ├── 📄 database.py      # Configuración BD
│   │   └── 📄 main.py          # App principal
│   ├── 📁 alembic/             # Migraciones
│   ├── 📄 requirements.txt     # Dependencias Python
│   ├── 📄 Dockerfile           # Docker backend
│   └── 📄 .env.example         # Variables de entorno
├── 📁 frontend/
│   ├── 📁 src/
│   │   ├── 📁 components/      # Componentes React
│   │   ├── 📁 pages/           # Páginas
│   │   ├── 📁 services/        # API services
│   │   ├── 📁 hooks/           # Custom hooks
│   │   ├── 📁 utils/           # Utilidades
│   │   └── 📁 types/           # Tipos TypeScript
│   ├── 📄 package.json         # Dependencias Node
│   ├── 📄 Dockerfile           # Docker frontend
│   └── 📄 vite.config.ts       # Configuración Vite
├── 📄 docker-compose.yml       # Orquestación Docker
├── 📄 setup.sh                 # Script instalación Linux/Mac
├── 📄 setup.bat                # Script instalación Windows
└── 📄 README.md                # Este archivo
```

---

## 🔧 Configuración

### 🔐 Variables de Entorno Backend

```env
# Base de datos
DATABASE_URL=sqlite:///./project_manager.db
# Para PostgreSQL: postgresql://user:password@localhost/dbname

# Seguridad
SECRET_KEY=tu-clave-secreta-super-segura-aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI (Opcional - para funciones de IA)
OPENAI_API_KEY=sk-tu-api-key-de-openai
OPENAI_MODEL=gpt-3.5-turbo

# Email (Opcional - para notificaciones)
MAIL_USERNAME=tu-email@ejemplo.com
MAIL_PASSWORD=tu-app-password
MAIL_FROM=tu-email@ejemplo.com
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com

# Entorno
ENVIRONMENT=development
DEBUG=true
```

### ⚙️ Configuración Frontend

El frontend se configura automáticamente para conectarse al backend en `http://localhost:8000`. Para cambiar esto, modifica `src/services/apiClient.ts`.

---

## 📊 API Documentation

### 🔗 Endpoints Principales

#### 🔐 Autenticación
```http
POST /api/v1/auth/register    # Registro de usuario
POST /api/v1/auth/login       # Inicio de sesión
POST /api/v1/auth/refresh     # Renovar token
```

#### 📁 Proyectos
```http
GET    /api/v1/projects/           # Listar proyectos
POST   /api/v1/projects/           # Crear proyecto
GET    /api/v1/projects/{id}       # Obtener proyecto
PUT    /api/v1/projects/{id}       # Actualizar proyecto
DELETE /api/v1/projects/{id}       # Eliminar proyecto
```

#### ✅ Tareas
```http
GET    /api/v1/tasks/              # Listar tareas
POST   /api/v1/tasks/              # Crear tarea
GET    /api/v1/tasks/{id}          # Obtener tarea
PUT    /api/v1/tasks/{id}          # Actualizar tarea
DELETE /api/v1/tasks/{id}          # Eliminar tarea
```

#### 🤖 IA Insights
```http
POST /api/v1/ai-insights/analyze-project/{id}           # Análisis completo
GET  /api/v1/ai-insights/project/{id}/risk-assessment   # Evaluación riesgos
GET  /api/v1/ai-insights/project/{id}/progress-prediction # Predicción progreso
```

### 📖 Documentación Interactiva

Una vez que el backend esté ejecutándose, visita:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🎮 Uso

### 1️⃣ **Registro e Inicio de Sesión**
- Crea una cuenta nueva o inicia sesión
- El sistema incluye autenticación JWT segura

### 2️⃣ **Dashboard**
- Visualiza métricas clave de tus proyectos
- Revisa alertas y tareas pendientes
- Analiza gráficos de progreso

### 3️⃣ **Gestión de Proyectos**
- Crea nuevos proyectos con información detallada
- Establece presupuestos y fechas límite
- Monitorea el progreso en tiempo real

### 4️⃣ **Gestión de Tareas**
- Organiza tareas por proyecto
- Asigna prioridades y fechas límite
- Actualiza estados de progreso

### 5️⃣ **Insights de IA**
- Obtén análisis automáticos de riesgos
- Revisa predicciones de progreso
- Consulta recomendaciones inteligentes

---

## 📸 Capturas de Pantalla

<div align="center">

### 🔐 Pantalla de Login
![Login](./docs/images/login.png)
*Interfaz de autenticación segura con validación de credenciales*

### 🏠 Dashboard Principal
![Dashboard](./docs/images/dashboard.png)
*Vista general del dashboard con métricas en tiempo real y resumen de proyectos*

### 📁 Gestión de Proyectos
![Projects](./docs/images/projects.png)
*Interfaz completa para gestionar proyectos con filtros y búsqueda avanzada*

### ✅ Gestión de Tareas
![Tasks](./docs/images/tasks.png)
*Sistema de tareas con estados, prioridades y seguimiento de progreso*

### 🤖 Asistente de IA
![AI Assistant](./docs/images/ai.png)
*Asistente de IA integrado para análisis de proyectos y sugerencias inteligentes*

### ⚙️ Panel de Administración
![Admin Panel](./docs/images/admin.png)
*Panel de administración para gestión de usuarios y configuración del sistema*

</div>

---

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Sigue estos pasos:

### 🔄 Proceso de Contribución

1. **Fork** el proyecto
2. **Crea** una rama para tu feature
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit** tus cambios
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push** a la rama
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Abre** un Pull Request

### 📋 Guidelines

- Sigue las convenciones de código existentes
- Añade tests para nuevas funcionalidades
- Actualiza la documentación si es necesario
- Asegúrate de que todos los tests pasen

### 🐛 Reportar Bugs

Envía un email a [djs1km4@gmail.com](mailto:djs1km4@gmail.com) para reportar bugs. Incluye:
- Descripción detallada del problema
- Pasos para reproducir
- Comportamiento esperado vs actual
- Screenshots si aplica

---

## 📝 Licencia

Este proyecto está bajo la **Licencia MIT**. Ver [LICENSE](LICENSE) para más detalles.

```
MIT License

Copyright (c) 2024 Project AI Manager

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 🙏 Agradecimientos

- [FastAPI](https://fastapi.tiangolo.com/) - Framework web moderno para Python
- [React](https://reactjs.org/) - Biblioteca para interfaces de usuario
- [Tailwind CSS](https://tailwindcss.com/) - Framework de CSS utilitario
- [OpenAI](https://openai.com/) - API de inteligencia artificial
- [Lucide](https://lucide.dev/) - Iconos hermosos y consistentes

---

## 📞 Soporte y Contacto

- 📧 **Email**: [djs1km4@gmail.com](mailto:djs1km4@gmail.com)
- 🐛 **Issues**: [djs1km4@gmail.com](mailto:djs1km4@gmail.com)
- 💬 **Discusiones**: [GitHub Discussions](../../discussions)
- 📖 **Wiki**: [Documentación Completa](../../wiki)

---

<div align="center">

**⭐ Si te gusta este proyecto, ¡dale una estrella! ⭐**

**Desarrollado con ❤️ usando FastAPI, React y mucho café ☕**

![Visitors](https://visitor-badge.laobi.icu/badge?page_id=tu-usuario.project-ai-manager)
![GitHub stars](https://img.shields.io/github/stars/tu-usuario/project-ai-manager?style=social)
![GitHub forks](https://img.shields.io/github/forks/tu-usuario/project-ai-manager?style=social)

</div>