#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Tracker Web Nito - Versión Verde Marina
# Autor: Para Nito | SILVIACILENE ⛵

from flask import Flask, render_template_string, request, redirect
import os
import csv
from datetime import datetime, timedelta

app = Flask(__name__)

TRACKER_DIR = os.path.expanduser('~/.vela_tracker')
GLUCOSA_FILE = os.path.join(TRACKER_DIR, 'glucosa.csv')
PRACTICA_FILE = os.path.join(TRACKER_DIR, 'practica_vela.csv')
LECTURA_FILE = os.path.join(TRACKER_DIR, 'lectura.csv')
SUENO_FILE = os.path.join(TRACKER_DIR, 'sueno.csv')
NUTRICION_FILE = os.path.join(TRACKER_DIR, 'nutricion.csv')
AGUA_FILE = os.path.join(TRACKER_DIR, 'agua.csv')

os.makedirs(TRACKER_DIR, exist_ok=True)

def leer_csv_real(filepath):
    registros = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                registros.append(row)
    except: pass
    return registros

def filtrar_por_hoy(registros):
    hoy = datetime.now().strftime('%Y-%m-%d')
    return [r for r in registros if r.get('fecha', '').startswith(hoy)]

def leer_ultimo(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            if rows:
                return rows[-1]
    except: pass
    return {}

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧠⛵ Tracker Nito</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { 
            font-family: Arial, sans-serif; 
            max-width: 600px; 
            margin: 0 auto; 
            padding: 15px; 
            background: linear-gradient(135deg, #134E5E 0%, #71B280 100%); 
            min-height: 100vh; 
        }
        h1 { 
            color: white; 
            text-align: center; 
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3); 
            margin-bottom: 10px; 
            font-size: 24px; 
        }
        h2 { color: #134E5E; margin: 15px 0 10px 0; font-size: 18px; }
        h3 { color: #0D5C4E; font-size: 16px; margin: 12px 0 8px 0; }
        .subtitle { 
            color: #B8E6D5; 
            text-align: center; 
            margin-bottom: 20px; 
            font-size: 14px; 
        }
        .card { 
            background: white; 
            border-radius: 15px; 
            padding: 20px; 
            margin: 10px 0; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.2); 
        }
        .btn { 
            display: block; 
            width: 100%; 
            padding: 16px; 
            margin: 8px 0; 
            border: none; 
            border-radius: 10px; 
            font-size: 16px; 
            font-weight: bold; 
            cursor: pointer; 
            text-decoration: none; 
            text-align: center; 
            color: white; 
            transition: all 0.2s; 
        }
        .btn:active { transform: scale(0.98); }
        .btn-glucosa { background: linear-gradient(135deg, #134E5E, #0D5C4E); }
        .btn-practica { background: linear-gradient(135deg, #2E8B9E, #1E6B7E); }
        .btn-lectura { background: linear-gradient(135deg, #2E7D5E, #1E5D4E); }
        .btn-sueno { background: linear-gradient(135deg, #3D5E8E, #2D4E6E); }
        .btn-nutricion { background: linear-gradient(135deg, #E67E22, #D66E12); }
        .btn-agua { background: linear-gradient(135deg, #3498DB, #2488CB); }
        .btn-registros { background: linear-gradient(135deg, #1ABC9C, #16A085); }
        .btn-estadisticas { background: linear-gradient(135deg, #9B59B6, #8E44AD); }
        .btn-back { 
            background: linear-gradient(135deg, #7F8C8D, #6F7C7D); 
            margin-top: 15px;
        }
        input, select, textarea { 
            width: 100%; 
            padding: 14px; 
            margin: 8px 0; 
            border: 2px solid #B8E6D5; 
            border-radius: 8px; 
            font-size: 16px; 
        }
        label { 
            font-weight: bold; 
            color: #134E5E; 
            display: block; 
            margin-top: 12px; 
        }
        .back { 
            display: inline-block; 
            margin: 15px 0; 
            color: #134E5E; 
            text-decoration: none; 
            font-weight: bold; 
            background: #B8E6D5;
            padding: 10px 20px;
            border-radius: 8px;
        }
        .data-row { 
            padding: 10px; 
            border-bottom: 1px solid #B8E6D5; 
            font-size: 14px; 
        }
        .stat-box { 
            background: linear-gradient(135deg, #B8E6D5, #98D6C5); 
            padding: 15px; 
            border-radius: 10px; 
            margin: 10px 0; 
            text-align: center; 
        }
        .stat-number { 
            font-size: 32px; 
            font-weight: bold; 
            color: #134E5E; 
        }
        .stat-label { 
            color: #0D5C4E; 
            font-size: 14px; 
            margin-top: 5px; 
        }
        .menu-grid { 
            display: grid; 
            grid-template-columns: 1fr 1fr; 
            gap: 10px; 
        }
        .status { 
            background: #B8E6D5; 
            color: #0D5C4E; 
            padding: 10px; 
            border-radius: 8px; 
            margin: 10px 0; 
            text-align: center; 
            font-size: 12px; 
        }
        .nav-tabs { 
            display: flex; 
            gap: 5px; 
            margin: 10px 0; 
            flex-wrap: wrap; 
        }
        .nav-tab { 
            flex: 1; 
            padding: 10px; 
            background: white; 
            border: none; 
            border-radius: 8px; 
            cursor: pointer; 
            font-weight: bold; 
            text-decoration: none; 
            text-align: center; 
            color: #134E5E; 
            min-width: 100px; 
        }
        .nav-tab.active { 
            background: #134E5E; 
            color: white; 
        }
        .book-option {
            background: #B8E6D5;
            padding: 10px;
            border-radius: 8px;
            margin: 5px 0;
        }
    </style>
</head>
<body>
    <h1>🧠⛵ Tracker Nito</h1>
    <p class="subtitle">SILVIACILENE - Versión Verde Marina</p>
    
    {% if pagina == "inicio" %}
    
    <div class="nav-tabs">
        <a href="/" class="nav-tab active">🏠 Inicio</a>
        <a href="/registros_hoy" class="nav-tab">📋 Hoy</a>
        <a href="/estadisticas" class="nav-tab">📊 Stats</a>
    </div>
    
    <div class="card">
        <h2>📊 Registrar</h2>
        <div class="menu-grid">
            <a href="/glucosa" class="btn btn-glucosa">🩸 Glucosa</a>
            <a href="/practica" class="btn btn-practica">⛵ Práctica</a>
            <a href="/lectura" class="btn btn-lectura">📚 Lectura</a>
            <a href="/sueno" class="btn btn-sueno">😴 Sueño</a>
            <a href="/nutricion" class="btn btn-nutricion">🍽️ Comida</a>
            <a href="/agua" class="btn btn-agua">💧 Agua</a>
        </div>
    </div>
    
    <div class="card">
        <h2>📈 Últimos Registros</h2>
        <div class="data-row">🩸 <strong>Glucosa:</strong> {{ glucosa.get('valor_mg_dl', 'Sin registros') }} mmol/L</div>
        <div class="data-row">⛵ <strong>Práctica:</strong> {{ practica.get('tipo', 'Sin registros') }}</div>
        <div class="data-row">📚 <strong>Lectura:</strong> {{ lectura.get('capitulo', 'Sin registros') }}</div>
        <div class="data-row">😴 <strong>Sueño:</strong> {{ sueno.get('calidad_1_10', 'Sin registros') }}/10</div>
        <div class="data-row">💧 <strong>Agua hoy:</strong> {{ agua_count }} vasos</div>
    </div>
    
    <div class="status">
        ✅ http://10.0.0.60:5001<br>
        📁 ~/.vela_tracker/ (formato original)<br>
        🌊 Versión Verde Marina
    </div>
    
    {% elif pagina == "registros_hoy" %}
    
    <div class="nav-tabs">
        <a href="/" class="nav-tab">🏠 Inicio</a>
        <a href="/registros_hoy" class="nav-tab active">📋 Hoy</a>
        <a href="/estadisticas" class="nav-tab">📊 Stats</a>
    </div>
    
    <div class="card">
        <h2>📋 Registros de Hoy</h2>
        <p style="text-align:center;color:#0D5C4E;margin-bottom:15px;">{{ fecha_hoy }}</p>
        
        <h3>🩸 Glucosa ({{ stats_glucosa.total }})</h3>
        {% if registros_glucosa_hoy %}
            {% for r in registros_glucosa_hoy %}
            <div class="data-row">{{ r.get('hora','?') }} - {{ r.get('tipo','?') }}: <strong>{{ r.get('valor_mg_dl','?') }} mmol/L</strong></div>
            {% endfor %}
        {% else %}<p style="text-align:center;color:#999;">Sin registros</p>{% endif %}
        
        <h3>⛵ Práctica ({{ stats_practica.sesiones }} - {{ stats_practica.total_min }} min)</h3>
        {% if registros_practica_hoy %}
            {% for r in registros_practica_hoy %}
            <div class="data-row">{{ r.get('tipo','?') }}: <strong>{{ r.get('duracion_min','?') }} min</strong></div>
            {% endfor %}
        {% else %}<p style="text-align:center;color:#999;">Sin práctica</p>{% endif %}
        
        <h3>📚 Lectura</h3>
        {% if registros_lectura_hoy %}
            {% for r in registros_lectura_hoy %}
            <div class="data-row">{{ r.get('libro','?') }} - {{ r.get('capitulo','?') }}: <strong>{{ r.get('tiempo_min','?') }} min</strong></div>
            {% endfor %}
        {% else %}<p style="text-align:center;color:#999;">Sin lectura</p>{% endif %}
        
        <h3>😴 Sueño</h3>
        {% if registros_sueno_hoy %}
            {% for r in registros_sueno_hoy %}
            <div class="data-row">{{ r.get('tipo','?') }}: Calidad <strong>{{ r.get('calidad_1_10','?') }}/10</strong></div>
            {% endfor %}
        {% else %}<p style="text-align:center;color:#999;">Sin sueño</p>{% endif %}
        
        <h3>💧 Agua</h3>
        {% if registros_agua_hoy %}
            <div class="data-row"><strong>{{ registros_agua_hoy|length }} vasos registrados hoy</strong></div>
        {% else %}<p style="text-align:center;color:#999;">Sin registros</p>{% endif %}
    </div>
    
    <a href="/" class="back">← Volver al Inicio</a>
    
    {% elif pagina == "estadisticas" %}
    
    <div class="nav-tabs">
        <a href="/" class="nav-tab">🏠 Inicio</a>
        <a href="/registros_hoy" class="nav-tab">📋 Hoy</a>
        <a href="/estadisticas" class="nav-tab active">📊 Stats</a>
    </div>
    
    <div class="card">
        <h2>📊 Estadísticas Semanales</h2>
        <p style="text-align:center;color:#0D5C4E;margin-bottom:15px;">Últimos 7 días</p>
        
        <h3>🩸 Glucosa</h3>
        <div class="stat-box">
            <div class="stat-number">{{ glucosa_stats.promedio }}</div>
            <div class="stat-label">Promedio mmol/L ({{ glucosa_stats.total }} registros)</div>
        </div>
        <div style="display:flex;justify-content:space-around;margin:10px 0;">
            <div style="text-align:center;"><div style="font-size:24px;font-weight:bold;color:#134E5E;">{{ glucosa_stats.min }}</div><div style="font-size:12px;color:#0D5C4E;">Mín</div></div>
            <div style="text-align:center;"><div style="font-size:24px;font-weight:bold;color:#2E8B5E;">{{ glucosa_stats.max }}</div><div style="font-size:12px;color:#0D5C4E;">Máx</div></div>
        </div>
        
        <h3>⛵ Práctica</h3>
        <div class="stat-box">
            <div class="stat-number">{{ practica_stats.total_horas }}h</div>
            <div class="stat-label">{{ practica_stats.total_min }} min totales</div>
        </div>
        <div style="display:flex;justify-content:space-around;margin:10px 0;">
            <div style="text-align:center;"><div style="font-size:24px;font-weight:bold;color:#2E8B9E;">{{ practica_stats.sesiones }}</div><div style="font-size:12px;color:#0D5C4E;">Sesiones</div></div>
            <div style="text-align:center;"><div style="font-size:24px;font-weight:bold;color:#1ABC9C;">{{ (practica_stats.total_min/practica_stats.sesiones)|round(1) if practica_stats.sesiones>0 else 0 }}min</div><div style="font-size:12px;color:#0D5C4E;">Promedio</div></div>
        </div>
        
        <h3>📚 Lectura</h3>
        <div class="stat-box">
            <div class="stat-number">{{ lectura_count }}</div>
            <div class="stat-label">Sesiones esta semana</div>
        </div>
        
        <h3>😴 Sueño</h3>
        <div class="stat-box">
            <div class="stat-number">{{ sueno_stats.promedio_calidad }}/10</div>
            <div class="stat-label">Calidad promedio ({{ sueno_stats.total }} registros)</div>
        </div>
        
        <h3>💧 Agua</h3>
        <div class="stat-box">
            <div class="stat-number">{{ agua_semanal }}</div>
            <div class="stat-label">Vasos esta semana</div>
        </div>
    </div>
    
    <a href="/" class="back">← Volver al Inicio</a>
    
    {% elif pagina == "glucosa" %}
    <div class="card">
        <h2>🩸 Registrar Glucosa</h2>
        <p style="text-align:center;color:#0D5C4E;font-size:13px;margin-bottom:10px;">🇳🇴 Formato noruego: <strong>mmol/L</strong></p>
        <form method="POST" action="/guardar_glucosa">
            <label>Valor (mmol/L):</label>
            <input type="number" step="0.1" name="valor" placeholder="ej: 6.4" required>
            <label>Tipo:</label>
            <select name="tipo">
                <option value="Ayunas">Ayunas</option>
                <option value="Pre-prandial">Pre-prandial</option>
                <option value="Post-prandial">Post-prandial</option>
                <option value="Pre-turno">Pre-turno</option>
            </select>
            <label>Notas:</label>
            <textarea name="notas" placeholder="ej: post-almuerzo" rows="2"></textarea>
            <button type="submit" class="btn btn-glucosa" style="margin-top:15px;">💾 Guardar</button>
        </form>
    </div>
    <a href="/" class="back">← Volver al Inicio</a>
    
    {% elif pagina == "practica" %}
    <div class="card">
        <h2>⛵ Registrar Práctica</h2>
        <form method="POST" action="/guardar_practica">
            <label>Tipo:</label>
            <select name="tipo">
                <option value="Teoria">Teoría</option>
                <option value="Knots3D">Knots3D</option>
                <option value="Simulador">Simulador</option>
                <option value="Agua">En Agua</option>
                <option value="OpenCPN">OpenCPN</option>
            </select>
            <label>Duración (min):</label>
            <input type="number" name="duracion" placeholder="20" required>
            <label>Maniobras:</label>
            <input type="text" name="maniobras" placeholder="ej: lectura_p26">
            <label>Notas:</label>
            <textarea name="notas" placeholder="ej: términos ES/NO" rows="2"></textarea>
            <button type="submit" class="btn btn-practica" style="margin-top:15px;">💾 Guardar</button>
        </form>
    </div>
    <a href="/" class="back">← Volver al Inicio</a>
    
    {% elif pagina == "lectura" %}
    <div class="card">
        <h2>📚 Registrar Lectura</h2>
        <form method="POST" action="/guardar_lectura">
            <label>Libro:</label>
            <select name="libro">
                <option value="Mosenthal_Aprender_a_navegar">📖 Mosenthal - Aprender a Navegar</option>
                <option value="Laer_a_seile_Bent_Aarre">⛵ Lær å Seile - Bent Aarre</option>
            </select>
            <label>Capítulo:</label>
            <input type="text" name="capitulo" placeholder="ej: Cap2_Terminologia" required>
            <label>Tiempo (min):</label>
            <input type="number" name="tiempo" placeholder="15" required>
            <label>Términos nuevos:</label>
            <input type="text" name="terminos" placeholder="ej: Styrbord, Skjøte">
            <button type="submit" class="btn btn-lectura" style="margin-top:15px;">💾 Guardar</button>
        </form>
    </div>
    <a href="/" class="back">← Volver al Inicio</a>
    
    {% elif pagina == "sueno" %}
    <div class="card">
        <h2>😴 Registrar Sueño</h2>
        <form method="POST" action="/guardar_sueno">
            <label>Tipo:</label>
            <select name="tipo">
                <option value="Principal_diurno">Principal Diurno</option>
                <option value="Principal_nocturno">Principal Nocturno</option>
                <option value="Siesta">Siesta</option>
            </select>
            <label>Hora inicio:</label>
            <input type="text" name="hora_inicio" placeholder="ej: 22:00">
            <label>Hora fin:</label>
            <input type="text" name="hora_fin" placeholder="ej: 06:00">
            <label>Calidad (1-10):</label>
            <input type="number" name="calidad" min="1" max="10" placeholder="8" required>
            <button type="submit" class="btn btn-sueno" style="margin-top:15px;">💾 Guardar</button>
        </form>
    </div>
    <a href="/" class="back">← Volver al Inicio</a>
    
    {% elif pagina == "nutricion" %}
    <div class="card">
        <h2>🍽️ Registrar Nutrición</h2>
        <form method="POST" action="/guardar_nutricion">
            <label>Tipo:</label>
            <select name="tipo">
                <option value="Desayuno">Desayuno</option>
                <option value="Almuerzo">Almuerzo</option>
                <option value="Cena">Cena</option>
                <option value="Snack">🍪 Snack</option>
            </select>
            <label>Descripción:</label>
            <textarea name="descripcion" placeholder="ej: Tostadas con huevo" rows="3" required></textarea>
            <button type="submit" class="btn btn-nutricion" style="margin-top:15px;">💾 Guardar</button>
        </form>
    </div>
    <a href="/" class="back">← Volver al Inicio</a>
    
    {% elif pagina == "agua" %}
    <div class="card">
        <h2>💧 Registrar Agua</h2>
        <p style="text-align:center;color:#0D5C4E;font-size:13px;margin-bottom:10px;">🇳🇴 Meta diaria: <strong>8 vasos</strong> (≈2L)</p>
        <form method="POST" action="/guardar_agua">
            <label>Cantidad:</label>
            <select name="cantidad">
                <option value="1">1 vaso (250ml)</option>
                <option value="2">2 vasos (500ml)</option>
                <option value="3">3 vasos (750ml)</option>
            </select>
            <label>Notas:</label>
            <textarea name="notas" placeholder="ej: despues_de_comida" rows="2"></textarea>
            <button type="submit" class="btn btn-agua" style="margin-top:15px;">💾 Guardar</button>
        </form>
    </div>
    <a href="/" class="back">← Volver al Inicio</a>
    {% endif %}
</body>
</html>
'''

# Routes de visualización
@app.route('/')
def inicio():
    agua_hoy = filtrar_por_hoy(leer_csv_real(AGUA_FILE))
    agua_count = sum(int(r.get('cantidad', 0)) for r in agua_hoy)
    return render_template_string(HTML, pagina="inicio",
        glucosa=leer_ultimo(GLUCOSA_FILE),
        practica=leer_ultimo(PRACTICA_FILE),
        lectura=leer_ultimo(LECTURA_FILE),
        sueno=leer_ultimo(SUENO_FILE),
        agua_count=agua_count)

@app.route('/registros_hoy')
def registros_hoy():
    hoy = datetime.now().strftime('%Y-%m-%d')
    agua_hoy = filtrar_por_hoy(leer_csv_real(AGUA_FILE))
    return render_template_string(HTML, pagina="registros_hoy",
        fecha_hoy=hoy,
        registros_glucosa_hoy=filtrar_por_hoy(leer_csv_real(GLUCOSA_FILE)),
        registros_practica_hoy=filtrar_por_hoy(leer_csv_real(PRACTICA_FILE)),
        registros_lectura_hoy=filtrar_por_hoy(leer_csv_real(LECTURA_FILE)),
        registros_sueno_hoy=filtrar_por_hoy(leer_csv_real(SUENO_FILE)),
        registros_agua_hoy=agua_hoy,
        stats_glucosa=calcular_estadisticas_glucosa(filtrar_por_hoy(leer_csv_real(GLUCOSA_FILE))),
        stats_practica=calcular_estadisticas_practica(filtrar_por_hoy(leer_csv_real(PRACTICA_FILE))),
        stats_sueno=calcular_estadisticas_sueno(filtrar_por_hoy(leer_csv_real(SUENO_FILE))))

@app.route('/estadisticas')
def estadisticas():
    agua_semanal = sum(int(r.get('cantidad', 0)) for r in filtrar_semana(leer_csv_real(AGUA_FILE)))
    return render_template_string(HTML, pagina="estadisticas",
        glucosa_stats=calcular_estadisticas_glucosa(filtrar_semana(leer_csv_real(GLUCOSA_FILE))),
        practica_stats=calcular_estadisticas_practica(filtrar_semana(leer_csv_real(PRACTICA_FILE))),
        sueno_stats=calcular_estadisticas_sueno(filtrar_semana(leer_csv_real(SUENO_FILE))),
        lectura_count=len(filtrar_semana(leer_csv_real(LECTURA_FILE))),
        agua_semanal=agua_semanal)

def calcular_estadisticas_glucosa(registros):
    if not registros:
        return {"promedio": "-", "min": "-", "max": "-", "total": 0}
    valores = []
    for r in registros:
        try:
            val = r.get('valor_mg_dl', '')
            if val:
                val_num = float(str(val).replace(',', '.'))
                if val_num > 20:
                    val_num = val_num / 18
                valores.append(val_num)
        except: pass
    if not valores:
        return {"promedio": "-", "min": "-", "max": "-", "total": 0}
    return {
        "promedio": f"{sum(valores)/len(valores):.1f}",
        "min": f"{min(valores):.1f}",
        "max": f"{max(valores):.1f}",
        "total": len(valores)
    }

def calcular_estadisticas_practica(registros):
    if not registros:
        return {"total_min": 0, "total_horas": "0", "sesiones": 0}
    total_min = 0
    for r in registros:
        try:
            dur = r.get('duracion_min', '0')
            total_min += int(str(dur).replace('min','').strip())
        except: pass
    return {
        "total_min": total_min,
        "total_horas": f"{total_min/60:.1f}",
        "sesiones": len(registros)
    }

def calcular_estadisticas_sueno(registros):
    if not registros:
        return {"promedio_calidad": "-", "total": 0}
    calidades = []
    for r in registros:
        try:
            cal = r.get('calidad_1_10', '')
            if cal:
                calidades.append(int(cal))
        except: pass
    return {
        "promedio_calidad": f"{sum(calidades)/len(calidades):.1f}" if calidades else "-",
        "total": len(registros)
    }

def filtrar_semana(registros):
    hace_7_dias = datetime.now() - timedelta(days=7)
    resultado = []
    for r in registros:
        try:
            fecha_str = r.get('fecha', '')[:10]
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
            if fecha >= hace_7_dias:
                resultado.append(r)
        except: pass
    return resultado

# Routes de guardado
@app.route('/guardar_glucosa', methods=['POST'])
def guardar_glucosa():
    hoy = datetime.now().strftime('%Y-%m-%d')
    hora = datetime.now().strftime('%H:%M')
    valor = request.form.get('valor', '')
    tipo = request.form.get('tipo', '')
    notas = request.form.get('notas', '')
    try:
        val_num = float(str(valor).replace(',', '.'))
        if val_num > 20:
            val_num = val_num / 18
        valor_final = f"{val_num:.1f}"
    except:
        valor_final = valor
    with open(GLUCOSA_FILE, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([hoy, hora, tipo, valor_final, '', '', notas])
    return redirect('/')

@app.route('/guardar_practica', methods=['POST'])
def guardar_practica():
    hoy = datetime.now().strftime('%Y-%m-%d')
    tipo = request.form.get('tipo', '')
    duracion = request.form.get('duracion', '')
    maniobras = request.form.get('maniobras', '')
    notas = request.form.get('notas', '')
    with open(PRACTICA_FILE, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([hoy, tipo, duracion, maniobras, '', '', '', notas])
    return redirect('/')

@app.route('/guardar_lectura', methods=['POST'])
def guardar_lectura():
    hoy = datetime.now().strftime('%Y-%m-%d')
    libro = request.form.get('libro', '')
    capitulo = request.form.get('capitulo', '')
    tiempo = request.form.get('tiempo', '')
    terminos = request.form.get('terminos', '')
    with open(LECTURA_FILE, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([hoy, libro, capitulo, '', terminos, tiempo, ''])
    return redirect('/')

@app.route('/guardar_sueno', methods=['POST'])
def guardar_sueno():
    hoy = datetime.now().strftime('%Y-%m-%d')
    tipo = request.form.get('tipo', '')
    hora_inicio = request.form.get('hora_inicio', '')
    hora_fin = request.form.get('hora_fin', '')
    calidad = request.form.get('calidad', '')
    with open(SUENO_FILE, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([hoy, tipo, hora_inicio, hora_fin, '', calidad, '', ''])
    return redirect('/')

@app.route('/guardar_nutricion', methods=['POST'])
def guardar_nutricion():
    hoy = datetime.now().strftime('%Y-%m-%d')
    hora = datetime.now().strftime('%H:%M')
    tipo = request.form.get('tipo', '')
    descripcion = request.form.get('descripcion', '')
    with open(NUTRICION_FILE, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([hoy, hora, tipo, descripcion, '', '', '', '', ''])
    return redirect('/')

@app.route('/guardar_agua', methods=['POST'])
def guardar_agua():
    hoy = datetime.now().strftime('%Y-%m-%d')
    hora = datetime.now().strftime('%H:%M')
    cantidad = request.form.get('cantidad', '1')
    notas = request.form.get('notas', '')
    with open(AGUA_FILE, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([hoy, hora, cantidad, notas])
    return redirect('/')

@app.route('/glucosa', methods=['GET'])
def glucosa_form():
    return render_template_string(HTML, pagina="glucosa")

@app.route('/practica', methods=['GET'])
def practica_form():
    return render_template_string(HTML, pagina="practica")

@app.route('/lectura', methods=['GET'])
def lectura_form():
    return render_template_string(HTML, pagina="lectura")

@app.route('/sueno', methods=['GET'])
def sueno_form():
    return render_template_string(HTML, pagina="sueno")

@app.route('/nutricion', methods=['GET'])
def nutricion_form():
    return render_template_string(HTML, pagina="nutricion")

@app.route('/agua', methods=['GET'])
def agua_form():
    return render_template_string(HTML, pagina="agua")

if __name__ == '__main__':
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    print("\n" + "="*60)
    print("  🧠⛵ TRACKER WEB - VERSIÓN VERDE MARINA")
    print("="*60)
    print(f"  🌐 http://{ip}:5001")
    print(f"  📁 {TRACKER_DIR}")
    print("  ✅ Color: Verde marino")
    print("  ✅ Botón Atrás en todas las páginas")
    print("  ✅ Libros: Mosenthal + Lær å seile")
    print("  ✅ Snack en Nutrición + Registro de Agua")
    print("="*60 + "\n")
    app.run(host='0.0.0.0', port=5001, debug=False)
