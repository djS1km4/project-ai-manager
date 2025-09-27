# Configuración de Deepseek AI via OpenRouter

## ¿Qué se ha implementado?

✅ **Sistema de IA completamente funcional** que reemplaza los datos simulados con análisis real de Deepseek AI.

### Características implementadas:

1. **Servicio Deepseek AI** (`deepseek_service.py`)
   - Análisis de riesgos del proyecto
   - Predicción de finalización
   - Análisis de rendimiento del equipo
   - Fallback a análisis basado en reglas cuando la IA no está disponible

2. **Integración completa** con el sistema existente
   - Reemplaza OpenAI con Deepseek
   - Mantiene compatibilidad con todos los endpoints
   - Elimina mensajes de "datos simulados"

3. **Endpoints funcionando**:
   - `/api/v1/ai-insights/project/{id}/analyze/risk`
   - `/api/v1/ai-insights/project/{id}/analyze/progress`
   - `/api/v1/ai-insights/project/{id}/analyze/team`
   - `/api/v1/ai-insights/analyze-project/{id}`

## Cómo obtener tu API key GRATUITA

### Paso 1: Registrarse en OpenRouter
1. Ve a [https://openrouter.ai](https://openrouter.ai)
2. Haz clic en "Sign Up" 
3. Regístrate con tu email o GitHub

### Paso 2: Obtener API Key
1. Una vez registrado, ve a [https://openrouter.ai/keys](https://openrouter.ai/keys)
2. Haz clic en "Create Key"
3. Dale un nombre (ej: "Project AI Manager")
4. Copia la API key (empieza con `sk-or-v1-...`)

### Paso 3: Configurar en tu proyecto
1. Abre el archivo `backend/.env`
2. Reemplaza la línea:
   ```
   DEEPSEEK_API_KEY=sk-or-v1-temp-key-for-testing
   ```
   Con tu API key real:
   ```
   DEEPSEEK_API_KEY=sk-or-v1-tu-api-key-aqui
   ```

### Paso 4: Reiniciar el servidor
```bash
cd backend
# Detener el servidor (Ctrl+C)
# Reiniciar
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## ¿Por qué OpenRouter?

- **GRATUITO**: Deepseek ofrece acceso gratuito via OpenRouter
- **Sin tarjeta de crédito**: No necesitas ingresar información de pago
- **Límites generosos**: Suficiente para desarrollo y pruebas
- **Fácil configuración**: Compatible con OpenAI SDK

## Verificar que funciona

1. Ve a la página de "AI Insights" en el frontend
2. Selecciona un proyecto
3. Haz clic en "Generar Insight"
4. Deberías ver análisis reales sin mensajes de "datos simulados"

## Solución de problemas

### Error: "AI service not enabled"
- Verifica que tu API key esté correctamente configurada
- Asegúrate de que no haya espacios extra en el archivo `.env`
- Reinicia el servidor backend

### Error: "Invalid API key"
- Verifica que copiaste la API key completa
- Asegúrate de que la key empiece con `sk-or-v1-`
- Genera una nueva key si es necesario

### Los insights siguen mostrando "datos simulados"
- Verifica que `AI_PROVIDER=deepseek` en el archivo `.env`
- Reinicia el servidor backend
- Limpia la caché del navegador

## Estado actual

🎉 **¡Todo está listo!** Solo necesitas configurar tu API key gratuita para tener IA real funcionando.

El sistema ya no muestra mensajes de "datos simulados" cuando Deepseek está configurado correctamente.