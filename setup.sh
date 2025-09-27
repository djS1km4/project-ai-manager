#!/bin/bash

# 🚀 Project AI Manager - Script de Instalación Automática
# Para sistemas Linux y macOS

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes con colores
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}  PROJECT AI MANAGER SETUP${NC}"
    echo -e "${BLUE}================================${NC}"
    echo ""
}

# Función para verificar si un comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Función para verificar prerrequisitos
check_prerequisites() {
    print_message "Verificando prerrequisitos..."
    
    # Verificar Python
    if command_exists python3; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        print_message "Python encontrado: $PYTHON_VERSION"
    else
        print_error "Python 3.8+ es requerido. Por favor instálalo desde https://python.org"
        exit 1
    fi
    
    # Verificar Node.js
    if command_exists node; then
        NODE_VERSION=$(node --version)
        print_message "Node.js encontrado: $NODE_VERSION"
    else
        print_error "Node.js 16+ es requerido. Por favor instálalo desde https://nodejs.org"
        exit 1
    fi
    
    # Verificar npm
    if command_exists npm; then
        NPM_VERSION=$(npm --version)
        print_message "npm encontrado: $NPM_VERSION"
    else
        print_error "npm es requerido. Por favor instálalo con Node.js"
        exit 1
    fi
    
    # Verificar Git
    if command_exists git; then
        GIT_VERSION=$(git --version)
        print_message "Git encontrado: $GIT_VERSION"
    else
        print_warning "Git no encontrado. Algunas funciones pueden no estar disponibles."
    fi
    
    print_message "✅ Todos los prerrequisitos están satisfechos!"
    echo ""
}

# Función para configurar el backend
setup_backend() {
    print_message "🔧 Configurando Backend..."
    
    cd backend
    
    # Crear entorno virtual
    print_message "Creando entorno virtual..."
    python3 -m venv venv
    
    # Activar entorno virtual
    print_message "Activando entorno virtual..."
    source venv/bin/activate
    
    # Instalar dependencias
    print_message "Instalando dependencias de Python..."
    pip install --upgrade pip
    pip install -r requirements.txt
    
    # Crear archivo .env si no existe
    if [ ! -f .env ]; then
        print_message "Creando archivo .env..."
        cp .env.example .env
        print_warning "⚠️  Por favor edita el archivo backend/.env con tus configuraciones"
    fi
    
    # Crear directorio de datos
    mkdir -p data
    
    print_message "✅ Backend configurado correctamente!"
    cd ..
    echo ""
}

# Función para configurar el frontend
setup_frontend() {
    print_message "⚛️  Configurando Frontend..."
    
    cd frontend
    
    # Instalar dependencias
    print_message "Instalando dependencias de Node.js..."
    npm install
    
    print_message "✅ Frontend configurado correctamente!"
    cd ..
    echo ""
}

# Función para crear scripts de inicio
create_start_scripts() {
    print_message "📝 Creando scripts de inicio..."
    
    # Script para iniciar backend
    cat > start-backend.sh << 'EOF'
#!/bin/bash
cd backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
EOF
    chmod +x start-backend.sh
    
    # Script para iniciar frontend
    cat > start-frontend.sh << 'EOF'
#!/bin/bash
cd frontend
npm run dev
EOF
    chmod +x start-frontend.sh
    
    # Script para iniciar ambos
    cat > start-all.sh << 'EOF'
#!/bin/bash
echo "🚀 Iniciando Project AI Manager..."
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo "API Docs: http://localhost:8000/docs"
echo ""

# Iniciar backend en segundo plano
./start-backend.sh &
BACKEND_PID=$!

# Esperar un poco para que el backend inicie
sleep 3

# Iniciar frontend
./start-frontend.sh &
FRONTEND_PID=$!

echo "✅ Aplicación iniciada!"
echo "Presiona Ctrl+C para detener ambos servicios"

# Función para limpiar procesos al salir
cleanup() {
    echo ""
    echo "🛑 Deteniendo servicios..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup INT

# Esperar indefinidamente
wait
EOF
    chmod +x start-all.sh
    
    print_message "✅ Scripts de inicio creados!"
    echo ""
}

# Función principal
main() {
    print_header
    
    check_prerequisites
    setup_backend
    setup_frontend
    create_start_scripts
    
    print_message "🎉 ¡Instalación completada exitosamente!"
    echo ""
    echo -e "${GREEN}Para iniciar la aplicación:${NC}"
    echo -e "  ${BLUE}./start-all.sh${NC}     - Iniciar backend y frontend"
    echo -e "  ${BLUE}./start-backend.sh${NC}  - Solo backend"
    echo -e "  ${BLUE}./start-frontend.sh${NC} - Solo frontend"
    echo ""
    echo -e "${GREEN}URLs de la aplicación:${NC}"
    echo -e "  Frontend: ${BLUE}http://localhost:5173${NC}"
    echo -e "  Backend:  ${BLUE}http://localhost:8000${NC}"
    echo -e "  API Docs: ${BLUE}http://localhost:8000/docs${NC}"
    echo ""
    echo -e "${YELLOW}Nota:${NC} Recuerda configurar las variables de entorno en backend/.env"
}

# Ejecutar función principal
main "$@"