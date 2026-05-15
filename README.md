# Portal Náutico SILVIACILENE ⛵

Sistema de gestión y monitoreo náutico con integración de bot Telegram y tracker personal.

**Autor:** Para Nito

---

## 📋 Descripción

Este proyecto consiste en una aplicación web Flask que proporciona:

1. **Portal Náutico (app.py)**: Panel de administración para enlaces, emergencias, fondeo y configuración de bot integrado
2. **Tracker Web (tracker_web.py)**: Sistema de seguimiento personal para glucosa, práctica de vela, lectura, sueño, nutrición e hidratación

---

## 🚀 Características

### Portal Náutico
- Autenticación HTTP Basic
- Gestión de enlaces útiles
- Registro de emergencias
- Control de fondeo
- Integración con SignalK y Telegram Bot
- Monitoreo de batería y tanques
- Soporte para archivos GPX

### Tracker Personal
- Seguimiento de glucosa
- Registro de práctica de vela
- Control de lectura diaria
- Monitoreo de sueño
- Registro nutricional
- Control de hidratación

---

## 📁 Estructura del Proyecto

```
/workspace
├── app.py              # Portal Náutico principal
├── tracker_web.py      # Aplicación de tracker personal
├── config.json         # Configuración del bot (no subir al repo)
├── data/
│   └── vela_tracker/   # Datos CSV del tracker
├── static/
│   ├── css/            # Hojas de estilo
│   ├── iconos/         # Iconos de la aplicación
│   └── js/             # Scripts JavaScript
├── templates/
│   ├── admin.html      # Plantilla de administración
│   ├── back-admin.htm  # Backup admin
│   ├── base.html       # Plantilla base
│   ├── index.html      # Página principal
│   └── tracker.html    # Plantilla del tracker
└── .gitignore          # Archivos ignorados por Git
```

---

## 🔧 Instalación

### Requisitos Previos

- Python 3.8+
- pip

### Dependencias

Las principales dependencias incluyen:
- Flask
- Flask-HTTPAuth
- gpxpy
- werkzeug

### Pasos de Instalación

1. Clonar el repositorio:
```bash
git clone <repository-url>
cd <project-directory>
```

2. Crear entorno virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows
```

3. Instalar dependencias:
```bash
pip install flask flask-httpauth gpxpy
```

4. Configurar el bot (opcional):
   - Copiar `config.json.example` a `config.json` (si existe)
   - Editar `config.json` con tus credenciales de Telegram y SignalK

5. Ejecutar la aplicación:
```bash
# Portal Náutico
python app.py

# O Tracker Web
python tracker_web.py
```

---

## ⚙️ Configuración

### config.json

El archivo `config.json` contiene la configuración del bot:

```json
{
  "telegram_token": "",
  "sk_url": "http://127.0.0.1:3000/signalk/v1/api/vessels/self",
  "sk_token": "",
  "sk_path": "Interior",
  "chat_id": "",
  "report_interval_min": 30,
  "webui_port": 8081,
  "bat_low": 11.8,
  "bat_crit": 11.4,
  "tank_low": 20.0,
  "tank_crit": 10.0
}
```

**⚠️ Importante:** Este archivo está en `.gitignore` y NO debe subirse al repositorio.

---

## 🔐 Credenciales por Defecto

- **Usuario:** `nito`
- **Contraseña:** `nito2002`

**⚠️ Seguridad:** Cambia estas credenciales en producción.

---

## 📊 Archivos de Datos

### Portal Náutico
- `data/enlaces.json` - Enlaces guardados
- `data/emergencia.json` - Contactos de emergencia
- `data/fondeo.json` - Información de fondeo

### Tracker Web
Los datos se almacenan en `~/.vela_tracker/`:
- `glucosa.csv` - Registros de glucosa
- `practica_vela.csv` - Práctica de vela
- `lectura.csv` - Registro de lectura
- `sueno.csv` - Control de sueño
- `nutricion.csv` - Registro nutricional
- `agua.csv` - Control de hidratación

---

## 🌐 Puertos

- **Portal Náutico:** 8081 (configurable en `config.json`)
- **Tracker Web:** Puerto por defecto de Flask

---

## 🛡️ Archivos Sensibles

Los siguientes archivos están en `.gitignore` y no deben subirse:
- `config.json` - Contiene tokens y credenciales
- `*.log` - Logs de la aplicación
- `venv/` - Entorno virtual
- `__pycache__/` - Caché de Python
- `data/*.json` - Datos sensibles
- `.env` - Variables de entorno

---

## 📝 Uso

### Portal Náutico

1. Acceder a `http://localhost:8081`
2. Iniciar sesión con las credenciales
3. Gestionar enlaces, emergencias y configuración del bot

### Tracker Web

1. Ejecutar `python tracker_web.py`
2. Acceder a la URL mostrada en consola
3. Registrar datos diarios de salud y actividades

---

## 🤝 Contribución

Para contribuir al proyecto:
1. Fork el repositorio
2. Crea una rama (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios (`git commit -m 'Añadir nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto es de uso personal.

---

## ⛵ Contacto

**Autor:** Para Nito  
**Proyecto:** SILVIACILENE

---

## 🙏 Agradecimientos

- Flask por el framework web
- SignalK por la integración de datos náuticos
- Telegram por la API del bot

---

*Última actualización: 2026*
