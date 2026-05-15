# Portal Náutico SILVIACILENE ⛵

Un portal web náutico completo con gestión de enlaces, datos de emergencia, información de fondeo, y tracker personal de salud y práctica de vela.

## 📋 Descripción

Este proyecto consiste en una aplicación web Flask diseñada para uso náutico, que incluye:

- **Portal de Enlaces**: Gestión de enlaces útiles para navegación (clima, navegación, sistema)
- **Datos de Emergencia**: Información de contacto de emergencia
- **Gestión de Fondeo**: Waypoints y rutas de navegación
- **Tracker Personal**: Seguimiento de glucosa, práctica de vela, lectura, sueño, nutrición e hidratación
- **Modo Oscuro**: Interfaz adaptable con soporte para modo oscuro
- **Iconos Personalizables**: Sistema de iconos para los enlaces

## 🚀 Aplicaciones Incluidas

### 1. `app.py` - Portal Náutico Principal
Versión final del portal con bot integrado. Incluye autenticación HTTP Basic y gestión completa de datos náuticos.

### 2. `app2.py` - Portal con Iconos + Modo Oscuro
Versión alternativa con soporte mejorado para iconos personalizados y modo oscuro.

### 3. `tracker_web.py` - Tracker Personal Nito
Aplicación independiente para seguimiento personal de:
- Glucosa
- Práctica de vela
- Lectura
- Sueño
- Nutrición
- Hidratación (agua)

## 📁 Estructura del Proyecto

```
/workspace
├── app.py                 # Portal principal
├── app2.py                # Portal con modo oscuro
├── tracker_web.py         # Tracker personal
├── config.json            # Configuración (no subir al repo)
├── data/
│   ├── enlaces.json       # Enlaces personalizados
│   ├── emergencia.json    # Contactos de emergencia
│   ├── fondeo.json        # Datos de fondeo
│   └── vela_tracker/      # Datos del tracker personal
│       ├── glucosa.csv
│       ├── practica_vela.csv
│       ├── lectura.csv
│       ├── sueno.csv
│       ├── nutricion.csv
│       └── agua.csv
├── templates/
│   ├── base.html          # Plantilla base
│   ├── index.html         # Página principal
│   ├── admin.html         # Panel de administración
│   ├── back-admin.htm     # Admin alternativo
│   └── tracker.html       # Interfaz del tracker
├── static/
│   ├── css/               # Hojas de estilo
│   ├── js/                # Scripts JavaScript
│   └── iconos/            # Iconos personalizados
└── README.md              # Este archivo
```

## 🔧 Requisitos

- Python 3.x
- Flask
- Flask-HTTPAuth
- gpxpy
- Werkzeug

### Instalar dependencias

```bash
pip install flask flask-httpauth gpxpy werkzeug
```

## 🏃‍♂️ Ejecución

### Portal Principal
```bash
python app.py
# o
python app2.py
```

### Tracker Personal
```bash
python tracker_web.py
```

Por defecto, las aplicaciones se ejecutan en:
- Portal: `http://localhost:5000`
- Tracker: `http://localhost:5001`

## 🔐 Autenticación

**Usuario:** `nito`  
**Contraseña:** `nito2002`

⚠️ **Importante:** Cambiar estas credenciales en producción modificando las variables `USUARIO` y `CONTRASENA_HASH` en el código.

## ⚙️ Configuración

El archivo `config.json` contiene la configuración del bot y no debe subirse al repositorio (está en `.gitignore`).

Los archivos de datos se generan automáticamente en la carpeta `data/`:
- `enlaces.json` - Lista de enlaces personalizados
- `emergencia.json` - Información de contacto de emergencia
- `fondeo.json` - Waypoints y rutas de fondeo

## 🎨 Características

- ✅ Interfaz responsive (móvil y escritorio)
- ✅ Modo oscuro disponible
- ✅ Iconos personalizables (emojis e imágenes)
- ✅ Autenticación básica HTTP
- ✅ Persistencia de datos en JSON y CSV
- ✅ Cálculo de rumbos y distancias náuticas
- ✅ Soporte para archivos GPX
- ✅ Gradientes marinos en la interfaz

## 📝 Notas

- Los archivos sensibles (`config.json`, `*.json` en data, logs) están excluidos del control de versiones
- El proyecto está diseñado para uso en red local (ej: `http://10.0.0.60:5000`)
- Los datos del tracker se almacenan en `~/.vela_tracker/`

## 👨‍💻 Autor

**Para Nito | SILVIACILENE ⛵**

## 📄 Licencia

Uso privado. Todos los derechos reservados.

---

*Proyecto desarrollado para gestión náutica y seguimiento personal*
