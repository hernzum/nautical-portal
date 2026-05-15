// ============================================
// PORTAL SILVIACILENE - CONTROL DE TEMAS
// Modo Oscuro/Claro
// ============================================

// Verificar tema guardado o preferencia del sistema
function getPreferredTheme() {
    const savedTheme = localStorage.getItem('silviacilene-theme');
    if (savedTheme) {
        return savedTheme;
    }
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

// Aplicar tema
function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('silviacilene-theme', theme);
    updateToggleButton(theme);
}

// Actualizar botón de toggle
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

// Toggle tema
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    applyTheme(newTheme);
}

// Inicializar al cargar
document.addEventListener('DOMContentLoaded', function() {
    const theme = getPreferredTheme();
    applyTheme(theme);
    
    // Event listener para el botón
    const toggleBtn = document.getElementById('theme-toggle');
    if (toggleBtn) {
        toggleBtn.addEventListener('click', toggleTheme);
    }
    
    // Escuchar cambios del sistema
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
        if (!localStorage.getItem('silviacilene-theme')) {
            applyTheme(e.matches ? 'dark' : 'light');
        }
    });
});

// Cargar waypoints desde API
async function cargarWaypoints() {
    try {
        const response = await fetch('/api/fondeo');
        const data = await response.json();
        
        const container = document.getElementById('waypoints-container');
        if (container && data.waypoints && data.waypoints.length > 0) {
            let html = '';
            data.waypoints.forEach((wp, index) => {
                html += `
                    <div class="waypoint-card">
                        <div class="waypoint-name">📍 ${wp.nombre || 'WP' + (index + 1)}</div>
                        <div class="waypoint-coords">
                            Lat: ${wp.latitud?.toFixed(6) || 'N/A'} | 
                            Lon: ${wp.longitud?.toFixed(6) || 'N/A'}
                        </div>
                        ${wp.rumbo ? `<div class="waypoint-course">🧭 Rumbo: ${wp.rumbo}°</div>` : ''}
                        ${wp.distancia_nm ? `<div class="waypoint-course">📏 Distancia: ${wp.distancia_nm} NM</div>` : ''}
                    </div>
                `;
            });
            container.innerHTML = html;
        }
    } catch (error) {
        console.error('Error cargando waypoints:', error);
    }
}

// Cargar waypoints al iniciar si existe el contenedor
if (document.getElementById('waypoints-container')) {
    cargarWaypoints();
}
