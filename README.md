# 🧪 Simulador Cuántico

Un simulador cuántico completo implementado con Flask y JavaScript, que permite simular moléculas usando métodos cuánticos avanzados.

## 🚀 Características

- **API REST Simple**: Simulación cuántica básica con respuesta inmediata
- **WebSocket Tiempo Real**: Progreso en tiempo real durante la simulación
- **API Mock**: Respuestas predefinidas para desarrollo frontend
- **Simulación por Lote**: Procesamiento en segundo plano para simulaciones largas
- **Análisis de Interacción**: Estudio de interacciones entre moléculas
- **Interfaz Web Moderna**: UI responsive con animaciones

## 📋 Requisitos

- Python 3.8+
- Flask 2.3.3+
- Node.js (para desarrollo frontend)
- Navegador web moderno

## 🛠️ Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone <repository-url>
   cd cuantica
   ```

2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar variables de entorno** (opcional, para IBM Quantum):
   ```bash
   # En Linux/Mac
   export IBM_QUANTUM_TOKEN=tu_api_key_de_ibm_quantum
   
   # En Windows PowerShell
   $env:IBM_QUANTUM_TOKEN="tu_api_key_de_ibm_quantum"
   ```
   
   O crea un archivo `.env` (no lo subas a Git):
   ```
   IBM_QUANTUM_TOKEN=tu_api_key_de_ibm_quantum
   SECRET_KEY=tu_clave_secreta_aleatoria
   ```
   
   **IMPORTANTE**: Nunca agregues tu API key directamente en el código fuente.

4. **Ejecutar el servidor**:
   ```bash
   python app.py
   ```

5. **Abrir en el navegador**:
   - Interfaz principal: http://localhost:5000
   - Demo interactivo: http://localhost:5000/demo
   - IBM Quantum: http://localhost:5000/ibm-quantum

## 🎯 APIs Disponibles

### 1. API REST Simple
```http
POST /api/quantum/simple
Content-Type: application/json

{
    "molecule": "LiH",
    "parameters": {
        "basis_set": "sto3g",
        "optimizer": "COBYLA"
    }
}
```

### 2. API REST Completo
```http
POST /api/quantum/simulate
Content-Type: application/json

{
    "molecule": "LiH",
    "parameters": {
        "basis_set": "sto3g",
        "optimizer": "COBYLA"
    }
}
```

### 3. API Mock
```http
POST /api/mock/quantum-simulate
Content-Type: application/json

{
    "molecule": "LiH"
}
```

### 4. WebSocket
```javascript
const socket = io('http://localhost:5000');
socket.emit('start_quantum_simulation', {
    molecule: 'LiH',
    parameters: {}
});
```

### 5. Simulación por Lote
```http
POST /api/quantum/start-simulation
GET /api/quantum/status/{simulation_id}
```

### 6. Análisis de Interacción
```http
POST /api/analyze-interaction
Content-Type: application/json

{
    "molecule1": "LiH",
    "molecule2": "H2O"
}
```

### 7. Información de Moléculas
```http
GET /api/molecules
GET /api/molecules/{molecule_name}
```

## 🧪 Moléculas Soportadas

- **LiH**: Litio-Hidrógeno
- **Li_GLYCINE**: Litio-Glicina
- **H2O**: Agua

## 🎮 Uso del Simulador

### Interfaz Principal
1. Selecciona una molécula del dropdown
2. Configura los parámetros (conjunto base, optimizador)
3. Elige el tipo de simulación:
   - **Simulación Simple**: Respuesta inmediata
   - **Simulación Avanzada**: Con más detalles
   - **Simulación Mock**: Para desarrollo
   - **WebSocket**: Con progreso en tiempo real

### Demo Interactivo
Visita `/demo` para probar todas las funcionalidades:
- Comparación de APIs
- Análisis de interacciones
- Información de moléculas
- Pruebas de rendimiento

## 🔧 Desarrollo

### Estructura del Proyecto
```
cuantica/
├── app.py                 # Servidor Flask principal
├── quantum_simulator.py   # Módulo de simulación cuántica
├── requirements.txt       # Dependencias Python
├── templates/            # Plantillas HTML
│   ├── index.html       # Interfaz principal
│   └── demo.html        # Demo interactivo
├── static/              # Archivos estáticos
│   ├── style.css       # Estilos CSS
│   └── script.js       # JavaScript
└── README.md           # Documentación
```

### Agregar Nueva Molécula
1. Edita `quantum_simulator.py`
2. Agrega la molécula al diccionario `molecule_data`
3. Actualiza el frontend si es necesario

### Agregar Nueva API
1. Define el endpoint en `app.py`
2. Implementa la lógica de negocio
3. Actualiza la documentación

## 📊 Ejemplos de Uso

### JavaScript (Frontend)
```javascript
// Simulación simple
async function runSimulation() {
    const response = await fetch('http://localhost:5000/api/quantum/simple', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            molecule: 'LiH',
            parameters: {
                basis_set: 'sto3g',
                optimizer: 'COBYLA'
            }
        })
    });
    
    const result = await response.json();
    console.log('Energía:', result.data.energy);
}

// WebSocket
const socket = io('http://localhost:5000');
socket.on('simulation_complete', (data) => {
    console.log('Simulación completada:', data.energy);
});
```

### Python (Backend)
```python
from quantum_simulator import simulate_molecule

# Simular molécula
result = simulate_molecule('LiH', {
    'basis_set': 'sto3g',
    'optimizer': 'COBYLA'
})

print(f"Energía: {result['energy']} Ha")
print(f"Fuerza de interacción: {result['interaction_strength']}")
```

## 🚀 Despliegue

### Desarrollo Local
```bash
python app.py
```

### Producción
```bash
# Usando Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Usando Docker
docker build -t quantum-simulator .
docker run -p 5000:5000 quantum-simulator
```

## 🐛 Solución de Problemas

### Error de Conexión
- Verifica que el servidor esté ejecutándose en el puerto 5000
- Revisa que no haya otros servicios usando el puerto

### WebSocket No Funciona
- Asegúrate de que Socket.IO esté cargado
- Verifica la consola del navegador para errores

### Simulación Lenta
- Usa la API Mock para desarrollo
- Considera usar simulación por lote para cálculos largos

## 📈 Próximas Mejoras

- [ ] Soporte para más moléculas
- [ ] Visualización 3D de moléculas
- [ ] Exportación de resultados
- [ ] Autenticación de usuarios
- [ ] Base de datos para historial
- [ ] API de machine learning

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 📞 Soporte

Si tienes problemas o preguntas:
- Abre un issue en GitHub
- Contacta al equipo de desarrollo
- Revisa la documentación

---

**¡Disfruta simulando el mundo cuántico! 🚀⚛️**
