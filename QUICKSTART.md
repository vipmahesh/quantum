# ⚡ Guía de Inicio Rápido

Pon en marcha el Simulador Cuántico en menos de 5 minutos.

## 🚀 Opción 1: Inicio Rápido (Sin IBM Quantum)

Para probar el simulador sin configurar IBM Quantum:

```bash
# 1. Clonar el repositorio
git clone https://github.com/picapiedra123/quantum.git
cd quantum

# 2. Instalar dependencias
pip install flask flask-socketio numpy scipy

# 3. Ejecutar el servidor
python app.py
```

**¡Listo!** Abre tu navegador en http://localhost:5000

## 🔬 Opción 2: Con IBM Quantum (Recomendado)

Para usar hardware cuántico real de IBM:

### Paso 1: Obtener API Token

1. Visita https://quantum-computing.ibm.com/
2. Crea una cuenta gratuita
3. Ve a tu perfil → API Token
4. Copia tu token

### Paso 2: Instalar

```bash
# Clonar e instalar dependencias completas
git clone https://github.com/picapiedra123/quantum.git
cd quantum
pip install -r requirements.txt
```

### Paso 3: Configurar

**Windows PowerShell:**
```powershell
$env:IBM_QUANTUM_TOKEN="tu_token_aqui"
$env:SECRET_KEY="clave_secreta_aleatoria"
```

**Linux/Mac:**
```bash
export IBM_QUANTUM_TOKEN="tu_token_aqui"
export SECRET_KEY="clave_secreta_aleatoria"
```

**O crear archivo `.env`:**
```bash
cp .env.example .env
# Editar .env con tu token
```

### Paso 4: Ejecutar

```bash
python app.py
```

## 🐳 Opción 3: Con Docker

La forma más fácil de ejecutar sin preocuparte por dependencias:

```bash
# Clonar
git clone https://github.com/picapiedra123/quantum.git
cd quantum

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# Ejecutar con Docker
docker-compose up -d
```

Accede en http://localhost:5000

## 📱 Primeros Pasos

### 1. Interfaz Web

Abre http://localhost:5000 en tu navegador:

1. **Selecciona una molécula**: LiH, H2O, o Li_GLYCINE
2. **Elige el tipo de simulación**:
   - Simulación Simple (más rápida)
   - Simulación Avanzada (más detalles)
   - IBM Quantum (hardware real)
3. **Haz clic en "Simular"**
4. **Observa los resultados**: Energía, tiempo de cómputo, gráficos

### 2. API REST

Prueba la API con curl o Postman:

```bash
curl -X POST http://localhost:5000/api/quantum/simple \
  -H "Content-Type: application/json" \
  -d '{"molecule": "LiH"}'
```

Respuesta:
```json
{
  "status": "success",
  "data": {
    "energy": -7.8634,
    "molecule": "LiH",
    "interaction_strength": "fuerte",
    "computation_time": "2.34 segundos"
  }
}
```

### 3. Ejemplos Interactivos

Visita http://localhost:5000/demo para:
- Comparar diferentes tipos de simulación
- Analizar interacciones moleculares
- Ver ejemplos de código
- Probar todas las APIs

## 📊 Tu Primera Simulación con Python

Crea un archivo `test_simulacion.py`:

```python
from quantum_simulator import simulate_molecule

# Simular molécula de Litio-Hidrógeno
resultado = simulate_molecule('LiH', {
    'basis_set': 'sto3g',
    'optimizer': 'COBYLA'
})

print(f"Energía calculada: {resultado['energy']:.4f} Hartree")
print(f"Fuerza de interacción: {resultado['interaction_strength']}")
print(f"Tiempo de cómputo: {resultado['computation_time']:.2f}s")
```

Ejecuta:
```bash
python test_simulacion.py
```

## 🧪 Moléculas Disponibles

| Molécula | Descripción | Complejidad |
|----------|-------------|-------------|
| `LiH` | Litio-Hidrógeno | Simple |
| `H2O` | Agua | Media |
| `Li_GLYCINE` | Litio-Glicina | Compleja |

## 🎯 Endpoints Principales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/quantum/simple` | Simulación básica |
| POST | `/api/quantum/simulate` | Simulación avanzada |
| POST | `/api/ibm-quantum/simulate` | Usar IBM Quantum |
| GET | `/api/molecules` | Lista de moléculas |
| POST | `/api/analyze-interaction` | Analizar interacciones |

## 🔧 Solución de Problemas Rápida

### Puerto 5000 ocupado
```bash
# Cambiar puerto
python app.py --port 8000
```

### Error de dependencias
```bash
# Reinstalar todo
pip install -r requirements.txt --force-reinstall
```

### WebSocket no funciona
```bash
# Instalar dependencias de WebSocket
pip install flask-socketio python-socketio
```

### Error de IBM Quantum
```bash
# Verificar token
echo $IBM_QUANTUM_TOKEN
# O en PowerShell
echo $env:IBM_QUANTUM_TOKEN
```

## 📚 Siguiente Paso

- 📖 Lee la [Documentación Completa](README.md)
- 🤝 Aprende a [Contribuir](CONTRIBUTING.md)
- 🔒 Revisa [Seguridad](SECURITY.md)
- 🚀 Lee la [Guía de Despliegue](DEPLOYMENT.md)

## 💡 Consejos

1. **Desarrollo**: Usa `MOCK_SIMULATIONS=True` para simulaciones más rápidas
2. **Debug**: Habilita `FLASK_DEBUG=True` para ver errores detallados
3. **Producción**: Cambia `SECRET_KEY` a algo seguro y aleatorio
4. **Performance**: Usa Gunicorn en lugar de Flask dev server

## 🎓 Recursos de Aprendizaje

- [Qiskit Textbook](https://qiskit.org/textbook/)
- [IBM Quantum Learning](https://learning.quantum.ibm.com/)
- [Documentación de Flask](https://flask.palletsprojects.com/)

## ❓ Ayuda

¿Problemas? 
- Abre un [Issue en GitHub](https://github.com/picapiedra123/quantum/issues)
- Revisa la documentación completa
- Consulta los ejemplos en `/demo`

---

**¡Bienvenido al mundo de la computación cuántica! 🚀⚛️**

