#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Portal Náutico SILVIACILENE - Versión Final con Iconos + Modo Oscuro
# Autor: Para Nito | ⛵

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json
import gpxpy
import gpxpy.gpx
from math import atan2, radians, degrees, sin, cos
from dotenv import load_dotenv

# Cargar variables de entorno desde .env si existe
load_dotenv()

app = Flask(__name__)
app.config['STATIC_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
# Secret key desde variable de entorno o valor por defecto (debe cambiarse en producción)
app.secret_key = os.getenv('SECRET_KEY', 'silviacilene_secret_key_2026_nito_secure')
auth = HTTPBasicAuth()

# Configuración
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
ICONOS_DIR = os.path.join(STATIC_DIR, 'iconos')

# Archivos de datos
ARCHIVO_ENLACES = os.path.join(DATA_DIR, 'enlaces.json')
ARCHIVO_EMERGENCIA = os.path.join(DATA_DIR, 'emergencia.json')
ARCHIVO_FONDEO = os.path.join(DATA_DIR, 'fondeo.json')

# Usuario y contraseña desde variables de entorno (CAMBIAR EN PRODUCCIÓN)
USUARIO = os.getenv('USUARIO', 'nito')
CONTRASENA_HASH = generate_password_hash(os.getenv('CONTRASENA', 'nito2002'))

@auth.verify_password
def verificar_contrasena(usuario, contrasena):
    if usuario == USUARIO:
        return check_password_hash(CONTRASENA_HASH, contrasena)
    return False

def cargar_json(archivo, default):
    if not os.path.exists(archivo):
        os.makedirs(os.path.dirname(archivo), exist_ok=True)
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(default, f, ensure_ascii=False, indent=2)
        return default
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return default

def guardar_json(archivo, datos):
    os.makedirs(os.path.dirname(archivo), exist_ok=True)
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)

def cargar_enlaces():
    default = [
        {"nombre": "Yr.no", "url": "https://www.yr.no", "icono": "🌤️", "categoria": "Clima"},
        {"nombre": "Windy", "url": "https://www.windy.com", "icono": "💨", "categoria": "Clima"},
        {"nombre": "OpenCPN", "url": "https://opencpn.org", "icono": "🗺️", "categoria": "Navegación"},
        {"nombre": "Tracker Web", "url": "http://10.0.0.60:5001", "icono": "📊", "categoria": "Sistema"},
    ]
    return cargar_json(ARCHIVO_ENLACES, default)

def guardar_enlaces(enlaces):
    guardar_json(ARCHIVO_ENLACES, enlaces)

def cargar_emergencia():
    default = {"contacto": "+47 113", "mensaje": "SOS - Emergencia marítima"}
    return cargar_json(ARCHIVO_EMERGENCIA, default)

def guardar_emergencia(emergencia):
    guardar_json(ARCHIVO_EMERGENCIA, emergencia)

def cargar_fondeo():
    default = {"waypoints": [], "courses": []}
    return cargar_json(ARCHIVO_FONDEO, default)

def guardar_fondeo(fondeo):
    guardar_json(ARCHIVO_FONDEO, fondeo)

def listar_iconos():
    """Lista todos los iconos disponibles en la carpeta static/iconos"""
    if os.path.exists(ICONOS_DIR):
        iconos = [f for f in os.listdir(ICONOS_DIR) if f.endswith(('.png', '.jpg', '.jpeg', '.svg', '.ico'))]
        # También agregar emojis por defecto
        emojis = ["🌤️", "💨", "🗺️", "📊", "⛵", "", "", "⚓", "🧭", ""]
        return emojis + iconos
    return ["🌤️", "💨", "🗺️", "📊", "⛵", "🔗", "", "⚓", "🧭", "🌊"]

def calcular_rumbo(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    x = sin(dlon) * cos(lat2)
    y = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dlon)
    rumbo = degrees(atan2(x, y))
    return (rumbo + 360) % 360

def extraer_datos_gpx(ruta_archivo):
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo_gpx:
            gpx = gpxpy.parse(archivo_gpx)
        
        puntos_ruta = []
        courses = []

        for ruta in gpx.routes:
            for i in range(len(ruta.points)):
                wp_actual = ruta.points[i]
                
                if i < len(ruta.points) - 1:
                    wp_siguiente = ruta.points[i + 1]
                    course = calcular_rumbo(wp_actual.latitude, wp_actual.longitude, 
                                          wp_siguiente.latitude, wp_siguiente.longitude)
                    rumbo = course
                else:
                    rumbo = None

                puntos_ruta.append({
                    "nombre": wp_actual.name or f"WP{i+1}",
                    "latitud": round(wp_actual.latitude, 6),
                    "longitud": round(wp_actual.longitude, 6),
                    "rumbo": round(rumbo, 1) if rumbo else None
                })

                if i < len(ruta.points) - 1:
                    courses.append({
                        "desde": wp_actual.name or f"WP{i+1}",
                        "hasta": wp_siguiente.name or f"WP{i+2}",
                        "course": round(course, 1)
                    })

        return puntos_ruta, courses
    except Exception as e:
        print(f"Error al procesar el archivo GPX: {e}")
        return [], []

# CSS Estilos (verde marino + MODO OSCURO/CLARO + ICONOS)
CSS_ESTILOS = '''
<style>
    :root {
        --bg-primary: linear-gradient(135deg, #134E5E 0%, #71B280 100%);
        --bg-card: #ffffff;
        --text-primary: #333333;
        --text-secondary: #134E5E;
        --text-muted: #666666;
        --border-color: #B8E6D5;
        --shadow: 0 4px 15px rgba(0,0,0,0.2);
        --link-card-bg: linear-gradient(135deg, #B8E6D5, #98D6C5);
        --table-header: #134E5E;
        --table-row-hover: #f5f5f5;
        --emergency-bg: linear-gradient(135deg, #fadbd8, #f5b7b1);
        --waypoint-bg: #f8f9fa;
        --input-border: #B8E6D5;
        --input-bg: #ffffff;
        --coord-color: #134E5E;
        --course-color: #0D5C4E;
    }
    [data-theme="dark"] {
        --bg-primary: linear-gradient(135deg, #0D3B47 0%, #5A8A70 100%);
        --bg-card: #1a1a2e;
        --text-primary: #e0e0e0;
        --text-secondary: #B8E6D5;
        --text-muted: #a0a0a0;
        --border-color: #2d2d44;
        --shadow: 0 4px 15px rgba(0,0,0,0.4);
        --link-card-bg: linear-gradient(135deg, #2d4a3e, #3d5a4e);
        --table-header: #0D3B47;
        --table-row-hover: #2a2a3e;
        --emergency-bg: linear-gradient(135deg, #4a2d2d, #5a3d3d);
        --waypoint-bg: #2a2a3e;
        --input-border: #2d2d44;
        --input-bg: #1a1a2e;
        --coord-color: #B8E6D5;
        --course-color: #98D6C5;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; transition: background-color 0.3s ease, color 0.3s ease; }
    body { 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: var(--bg-primary); 
        min-height: 100vh;
        color: var(--text-primary);
        padding: 20px;
    }
    .container { max-width: 1200px; margin: 0 auto; }
    .header {
        background: var(--bg-card);
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: var(--shadow);
        text-align: center;
        position: relative;
    }
    .header h1 { color: var(--text-secondary); font-size: 32px; margin-bottom: 10px; }
    .header p { color: var(--text-muted); font-size: 16px; }
    .theme-toggle {
        position: absolute;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #3498DB, #2980B9);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 20px;
        font-size: 14px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    .theme-toggle:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.3); }
    .nav-bar {
        background: var(--bg-card);
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        box-shadow: var(--shadow);
    }
    .nav-btn {
        flex: 1; min-width: 150px; padding: 12px 20px; border: none; border-radius: 8px;
        font-size: 15px; font-weight: bold; cursor: pointer; text-decoration: none;
        text-align: center; color: white; transition: all 0.3s;
    }
    .nav-btn:hover { transform: translateY(-2px); box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
    .nav-admin { background: linear-gradient(135deg, #9B59B6, #8E44AD); }
    .nav-home { background: linear-gradient(135deg, #3498DB, #2980B9); }
    .card {
        background: var(--bg-card); border-radius: 15px; padding: 25px; margin-bottom: 20px;
        box-shadow: var(--shadow);
    }
    .card h2 { color: var(--text-secondary); margin-bottom: 20px; padding-bottom: 10px; border-bottom: 3px solid var(--border-color); }
    .links-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; }
    .link-card {
        background: var(--link-card-bg); border-radius: 10px; padding: 20px;
        text-align: center; text-decoration: none; color: var(--text-secondary); transition: all 0.3s;
    }
    .link-card:hover { transform: translateY(-5px); box-shadow: 0 6px 20px rgba(0,0,0,0.2); }
    .link-icon { font-size: 40px; margin-bottom: 10px; }
    .link-icon img { width: 40px; height: 40px; object-fit: contain; }
    .link-name { font-size: 18px; font-weight: bold; margin-bottom: 5px; }
    .link-category { font-size: 12px; color: var(--text-muted); }
    .emergency-box {
        background: var(--emergency-bg); border-left: 5px solid #e74c3c;
        padding: 20px; border-radius: 8px; margin: 15px 0;
    }
    .emergency-contact { font-size: 24px; font-weight: bold; color: #e74c3c; }
    .waypoint-card {
        background: var(--waypoint-bg); border-left: 4px solid var(--text-secondary);
        padding: 15px; margin: 10px 0; border-radius: 5px;
    }
    .waypoint-name { font-weight: normal; color: var(--text-primary); font-size: 16px; }
    .waypoint-coords { color: var(--text-muted); font-size: 14px; margin: 5px 0; }
    .coord-highlight {
        font-weight: bold; color: var(--coord-color); font-family: 'Courier New', monospace;
    }
    .course-highlight {
        font-weight: bold; color: var(--course-color); font-size: 15px;
    }
    .form-group { margin: 15px 0; }
    label { display: block; margin-bottom: 5px; color: var(--text-secondary); font-weight: bold; }
    input, select, textarea {
        width: 100%; padding: 12px; border: 2px solid var(--input-border); 
        border-radius: 8px; font-size: 16px; background: var(--input-bg); color: var(--text-primary);
    }
    /* Icon Selector Grid */
    .icon-selector {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(50px, 1fr));
        gap: 10px;
        max-height: 200px;
        overflow-y: auto;
        padding: 10px;
        border: 2px solid var(--input-border);
        border-radius: 8px;
        background: var(--input-bg);
    }
    .icon-option {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 10px;
        border: 2px solid var(--border-color);
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s;
    }
    .icon-option:hover { border-color: var(--text-secondary); background: var(--link-card-bg); }
    .icon-option.selected { border-color: var(--text-secondary); background: var(--table-header); }
    .icon-option span { font-size: 24px; margin-bottom: 5px; }
    .icon-option img { width: 32px; height: 32px; object-fit: contain; }
    .icon-option label { font-size: 10px; color: var(--text-muted); margin: 0; }
    .btn {
        padding: 12px 24px; border: none; border-radius: 8px; font-size: 16px; font-weight: bold;
        cursor: pointer; transition: all 0.3s; text-decoration: none; display: inline-block;
    }
    .btn-primary { background: linear-gradient(135deg, #3498DB, #2980B9); color: white; }
    .btn-danger { background: linear-gradient(135deg, #e74c3c, #c0392b); color: white; }
    .btn:hover { transform: translateY(-2px); box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
    table { width: 100%; border-collapse: collapse; margin: 15px 0; }
    th, td { padding: 12px; text-align: left; border-bottom: 2px solid var(--border-color); color: var(--text-primary); }
    th { background: var(--table-header); color: white; }
    tr:hover { background: var(--table-row-hover); }
    .alert { padding: 15px; border-radius: 8px; margin: 10px 0; }
    .alert-success { background: #d4edda; color: #155724; }
    .footer { text-align: center; padding: 20px; color: white; margin-top: 30px; }
</style>
'''

# JavaScript para Modo Oscuro/Claro + Selector de Iconos
JS_THEME = '''
<script>
    function getPreferredTheme() {
        const savedTheme = localStorage.getItem('silviacilene-theme');
        if (savedTheme) { return savedTheme; }
        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
    function applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('silviacilene-theme', theme);
        updateToggleButton(theme);
    }
    function updateToggleButton(theme) {
        const btn = document.getElementById('theme-toggle');
        if (btn) {
            if (theme === 'dark') {
                btn.innerHTML = '☀️ Modo Claro';
                btn.setAttribute('data-theme', 'dark');
            } else {
                btn.innerHTML = '🌙 Modo Oscuro';
                btn.setAttribute('data-theme', 'light');
            }
        }
    }
    function toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        applyTheme(newTheme);
    }
    // Selector de Iconos
    function selectIcon(iconValue, element) {
        document.getElementById('iconoSeleccionado').value = iconValue;
        document.querySelectorAll('.icon-option').forEach(opt => opt.classList.remove('selected'));
        element.classList.add('selected');
    }
    document.addEventListener('DOMContentLoaded', function() {
        const theme = getPreferredTheme();
        applyTheme(theme);
    });
</script>
'''

@app.route('/')
def index():
    enlaces = cargar_enlaces()
    emergencia = cargar_emergencia()
    fondeo = cargar_fondeo()
    return render_template('index.html', enlaces=enlaces, emergencia=emergencia, 
                         fondeo=fondeo, estilos=CSS_ESTILOS, js_theme=JS_THEME, static_dir='/static')

@app.route('/admin', methods=['GET', 'POST'])
@auth.login_required
def admin():
    if request.method == 'POST':
        if 'nombre' in request.form:
            nuevo_enlace = {
                "nombre": request.form['nombre'],
                "url": request.form['url'],
                "icono": request.form.get('icono', '🔗'),
                "categoria": request.form.get('categoria', 'General')
            }
            enlaces = cargar_enlaces()
            enlaces.append(nuevo_enlace)
            guardar_enlaces(enlaces)
            flash('✅ Enlace agregado correctamente', 'success')
            
        elif 'gpx' in request.files:
            archivo_gpx = request.files['gpx']
            if archivo_gpx.filename:
                try:
                    ruta_temporal = os.path.join("/tmp", archivo_gpx.filename)
                    archivo_gpx.save(ruta_temporal)
                    waypoints, courses = extraer_datos_gpx(ruta_temporal)
                    fondeo = cargar_fondeo()
                    fondeo["waypoints"] = waypoints
                    fondeo["courses"] = courses
                    guardar_fondeo(fondeo)
                    os.remove(ruta_temporal)
                    flash('✅ Archivo GPX importado correctamente', 'success')
                except Exception as e:
                    flash(f'❌ Error al procesar GPX: {str(e)}', 'error')
                    
        elif 'contacto' in request.form:
            emergencia = {
                "contacto": request.form['contacto'],
                "mensaje": request.form['mensaje']
            }
            guardar_emergencia(emergencia)
            flash('✅ Información de emergencia actualizada', 'success')
        
        return redirect(url_for('admin'))
    
    enlaces = cargar_enlaces()
    iconos = listar_iconos()
    emergencia = cargar_emergencia()
    fondeo = cargar_fondeo()
    return render_template('admin.html', enlaces=enlaces, iconos=iconos, emergencia=emergencia, 
                         fondeo=fondeo, estilos=CSS_ESTILOS, js_theme=JS_THEME, static_dir='/static')

@app.route('/eliminar', methods=['POST'])
@auth.login_required
def eliminar_enlace():
    url = request.form['url']
    enlaces = cargar_enlaces()
    enlaces = [e for e in enlaces if e['url'] != url]
    guardar_enlaces(enlaces)
    flash('✅ Enlace eliminado', 'success')
    return redirect(url_for('admin'))

if __name__ == '__main__':
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    
    print("\n" + "="*60)
    print("  🧠⛵ PORTAL NÁUTICO SILVIACILENE")
    print("="*60)
    print(f"  🌐 http://{ip}:5002")
    print(f"  📁 {BASE_DIR}")
    print(f"  🎨 Iconos: {ICONOS_DIR}")
    print("  ✅ Modo Oscuro/Claro")
    print("  ✅ Selector de Iconos en Admin")
    print("  ✅ Coordenadas y Rumbo RESALTADOS")
    print("  ✅ 15 errores corregidos")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=5002, debug=True)
