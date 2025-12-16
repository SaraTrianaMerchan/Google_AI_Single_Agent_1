# 🤖 Google AI Single Agent - Frontend

Aplicación web moderna con React que permite interactuar con un agente de IA de Google usando Gemini 2.5 Flash Lite.

## ✨ Características

- 💬 **Interfaz de chat moderna** tipo ChatGPT
- 📱 **Responsive** - funciona en desktop y móvil
- 💾 **Historial persistente** usando LocalStorage
- 🔍 **Google Search integrado** - el agente puede buscar información actual
- ⚡ **Indicador de escritura** en tiempo real
- 🎨 **Diseño atractivo** con gradientes y animaciones

## 🏗️ Arquitectura

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────┐
│  Frontend React │ ──HTTP──> │  API (Vercel)    │ ──────> │   Agent     │
│  (Vite)         │ <──JSON─ │  (Python)        │ <───── │  (Google)   │
└─────────────────┘         └──────────────────┘         └─────────────┘
```

## 📂 Estructura del Proyecto

```
Google_AI_Single_Agent_1/
├── api/                    # Backend API (Vercel Serverless)
│   ├── ask.py             # Endpoint principal
│   └── requirements.txt   # Dependencias Python
├── frontend/              # Frontend React
│   ├── src/
│   │   ├── App.jsx        # Componente principal
│   │   ├── main.jsx       # Entry point
│   │   └── styles/
│   │       └── App.css    # Estilos
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── agent.py               # Agente de IA (usado por API)
├── retry.py               # Configuración de reintentos
├── vercel.json           # Config de Vercel
└── .env                   # Variables de entorno
```

## 🚀 Deployment en Vercel

### Paso 1: Preparar el repositorio

```bash
# Ya está todo listo, solo haz commit y push
git add .
git commit -m "Add frontend for Google AI Agent"
git push origin main
```

### Paso 2: Deploy en Vercel

#### Opción A: Desde la Web (Recomendado)

1. Ve a [vercel.com](https://vercel.com)
2. Click en **"Add New Project"**
3. Importa este repositorio de GitHub
4. Vercel detectará automáticamente la configuración
5. **IMPORTANTE:** Agrega la variable de entorno:
   - Key: `GOOGLE_API_KEY`
   - Value: Tu API key de Google AI
6. Click en **"Deploy"**

#### Opción B: Desde el CLI

```bash
# Instalar Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
vercel

# Agregar variable de entorno
vercel env add GOOGLE_API_KEY
# Pega tu API key cuando te lo pida

# Deploy a producción
vercel --prod
```

### Paso 3: Configurar la API Key

La API key de Google se debe configurar como **variable de entorno secreta en Vercel**:

1. Ve a tu proyecto en Vercel
2. Settings → Environment Variables
3. Agrega: `GOOGLE_API_KEY` = tu_api_key
4. Redeploy el proyecto

## 💻 Desarrollo Local

### Backend (API)

```bash
# Instalar dependencias
pip install -r api/requirements.txt

# Configurar .env
echo "GOOGLE_API_KEY=tu_api_key_aqui" > .env

# Probar el agente
python agent.py
```

### Frontend

```bash
# Ir a la carpeta del frontend
cd frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev

# Abrir en navegador: http://localhost:3000
```

### Desarrollo Full Stack Local

Para probar frontend + backend juntos localmente:

1. Instala [Vercel CLI](https://vercel.com/cli)
2. Ejecuta:

```bash
vercel dev
```

Esto iniciará tanto el frontend como las serverless functions localmente.

## 🔧 Configuración

### Variables de Entorno

```bash
# .env
GOOGLE_API_KEY=tu_api_key_de_google
```

### Personalizar el Agente

Edita `agent.py` para cambiar:

- **Modelo**: `model="gemini-2.5-flash-lite"` (línea 25)
- **Instrucciones**: `instruction="..."` (línea 29)
- **Tools**: `tools=[google_search]` (línea 30)

## 📱 Uso

1. Abre la aplicación en tu navegador
2. Escribe tu pregunta en el input
3. Click en "Enviar"
4. El agente procesará tu pregunta y responderá
5. Tu historial se guarda automáticamente

### Funciones:

- 🗑️ **Limpiar historial**: Botón en la esquina superior derecha
- 📜 **Auto-scroll**: Los mensajes nuevos se muestran automáticamente
- 💾 **Persistencia**: El historial se guarda en tu navegador

## 🎨 Personalización

### Cambiar colores

Edita `frontend/src/styles/App.css`:

```css
/* Gradiente principal */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Puedes cambiar los colores aquí */
```

### Cambiar textos

Edita `frontend/src/App.jsx`:

```jsx
<h2>¡Hola! Soy tu asistente AI</h2>
<p>Pregúntame lo que quieras y te ayudaré</p>
```

## 🐛 Troubleshooting

### Error: "Failed to get response"

- Verifica que la API key esté configurada en Vercel
- Revisa los logs en Vercel Dashboard → Functions

### El frontend no se conecta a la API

- Asegúrate de que ambos estén deployados en el mismo proyecto de Vercel
- Revisa la consola del navegador para errores

### El historial no se guarda

- Verifica que tu navegador permita LocalStorage
- No uses modo incógnito (borra el storage al cerrar)

## 📦 Tecnologías Utilizadas

- **Frontend**: React 18, Vite
- **Backend**: Python, Google ADK
- **IA**: Google Gemini 2.5 Flash Lite
- **Deployment**: Vercel
- **Storage**: LocalStorage (browser)

## 🔮 Mejoras Futuras

- [ ] Streaming de respuestas (ver al agente escribir en tiempo real)
- [ ] Base de datos para historial persistente
- [ ] Autenticación de usuarios
- [ ] Múltiples conversaciones
- [ ] Modo oscuro
- [ ] Exportar conversaciones
- [ ] Soporte para imágenes

## 📝 Notas

- El historial se guarda solo en tu navegador (LocalStorage)
- Cada pregunta es procesada independientemente por el agente
- El agente puede usar Google Search para información actual
- Las responses son procesadas por Gemini 2.5 Flash Lite

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Siéntete libre de abrir issues o pull requests.

## 📄 Licencia

MIT

---

**¿Preguntas?** Abre un issue en GitHub.

**¡Disfruta tu agente de IA!** 🚀
