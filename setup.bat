@echo off
REM 🚀 Project AI Manager - Script de Instalación Automática
REM Para sistemas Windows

setlocal enabledelayedexpansion

echo ================================
echo   PROJECT AI MANAGER SETUP
echo ================================
echo.

REM Función para verificar prerrequisitos
echo [INFO] Verificando prerrequisitos...

REM Verificar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python 3.8+ es requerido. Por favor instalalo desde https://python.org
    pause
    exit /b 1
) else (
    for /f "tokens=2" %%i in ('python --version') do echo [INFO] Python encontrado: %%i
)

REM Verificar Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js 16+ es requerido. Por favor instalalo desde https://nodejs.org
    pause
    exit /b 1
) else (
    for /f %%i in ('node --version') do echo [INFO] Node.js encontrado: %%i
)

REM Verificar npm
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] npm es requerido. Por favor instalalo con Node.js
    pause
    exit /b 1
) else (
    for /f %%i in ('npm --version') do echo [INFO] npm encontrado: %%i
)

REM Verificar Git
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Git no encontrado. Algunas funciones pueden no estar disponibles.
) else (
    for /f "tokens=1,2,3" %%i in ('git --version') do echo [INFO] Git encontrado: %%i %%j %%k
)

echo [INFO] ✅ Todos los prerrequisitos están satisfechos!
echo.

REM Configurar Backend
echo [INFO] 🔧 Configurando Backend...
cd backend

REM Crear entorno virtual
echo [INFO] Creando entorno virtual...
python -m venv venv

REM Activar entorno virtual
echo [INFO] Activando entorno virtual...
call venv\Scripts\activate.bat

REM Instalar dependencias
echo [INFO] Instalando dependencias de Python...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Crear archivo .env si no existe
if not exist .env (
    echo [INFO] Creando archivo .env...
    copy .env.example .env
    echo [WARNING] ⚠️  Por favor edita el archivo backend\.env con tus configuraciones
)

REM Crear directorio de datos
if not exist data mkdir data

echo [INFO] ✅ Backend configurado correctamente!
cd ..
echo.

REM Configurar Frontend
echo [INFO] ⚛️  Configurando Frontend...
cd frontend

REM Instalar dependencias
echo [INFO] Instalando dependencias de Node.js...
npm install

echo [INFO] ✅ Frontend configurado correctamente!
cd ..
echo.

REM Crear scripts de inicio
echo [INFO] 📝 Creando scripts de inicio...

REM Script para iniciar backend
echo @echo off > start-backend.bat
echo cd backend >> start-backend.bat
echo call venv\Scripts\activate.bat >> start-backend.bat
echo uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload >> start-backend.bat

REM Script para iniciar frontend
echo @echo off > start-frontend.bat
echo cd frontend >> start-frontend.bat
echo npm run dev >> start-frontend.bat

REM Script para iniciar ambos
echo @echo off > start-all.bat
echo echo 🚀 Iniciando Project AI Manager... >> start-all.bat
echo echo Backend: http://localhost:8000 >> start-all.bat
echo echo Frontend: http://localhost:5173 >> start-all.bat
echo echo API Docs: http://localhost:8000/docs >> start-all.bat
echo echo. >> start-all.bat
echo echo Iniciando backend... >> start-all.bat
echo start /b cmd /c start-backend.bat >> start-all.bat
echo timeout /t 3 /nobreak ^>nul >> start-all.bat
echo echo Iniciando frontend... >> start-all.bat
echo start /b cmd /c start-frontend.bat >> start-all.bat
echo echo ✅ Aplicación iniciada! >> start-all.bat
echo echo Presiona cualquier tecla para cerrar... >> start-all.bat
echo pause >> start-all.bat

echo [INFO] ✅ Scripts de inicio creados!
echo.

echo [INFO] 🎉 ¡Instalación completada exitosamente!
echo.
echo Para iniciar la aplicación:
echo   start-all.bat     - Iniciar backend y frontend
echo   start-backend.bat - Solo backend
echo   start-frontend.bat - Solo frontend
echo.
echo URLs de la aplicación:
echo   Frontend: http://localhost:5173
echo   Backend:  http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo.
echo Nota: Recuerda configurar las variables de entorno en backend\.env
echo.
pause