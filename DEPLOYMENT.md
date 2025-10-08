# 🚀 Guía de Despliegue - Simulador Cuántico

## 📋 Requisitos Previos

### Sistema
- Python 3.8 o superior
- Git
- Navegador web moderno

### Dependencias Python
```bash
pip install -r requirements.txt
```

## 🏠 Despliegue Local

### 1. Clonar el Repositorio
```bash
git clone https://github.com/picapiedra123/cuantica.git
cd cuantica
```

### 2. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 3. Ejecutar el Simulador
```bash
# Opción 1: Script principal
python app.py

# Opción 2: Script optimizado
python run.py

# Opción 3: Con configuración específica
FLASK_ENV=development python app.py
```

### 4. Acceder a la Aplicación
- **Interfaz Principal:** http://localhost:5000
- **Demo Interactivo:** http://localhost:5000/demo
- **APIs:** http://localhost:5000/api/

## 🌐 Despliegue en Producción

### Opción 1: Heroku

1. **Crear archivo Procfile:**
```procfile
web: gunicorn app:app
```

2. **Configurar variables de entorno:**
```bash
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=tu_secret_key_aqui
```

3. **Desplegar:**
```bash
git push heroku main
```

### Opción 2: Docker

1. **Crear Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "app.py"]
```

2. **Construir y ejecutar:**
```bash
docker build -t quantum-simulator .
docker run -p 5000:5000 quantum-simulator
```

### Opción 3: VPS/Cloud

1. **Configurar servidor:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip nginx

# Instalar dependencias
pip3 install -r requirements.txt
```

2. **Configurar Nginx:**
```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

3. **Ejecutar con Gunicorn:**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🔧 Configuración Avanzada

### Variables de Entorno
```bash
# Configuración del servidor
export HOST=0.0.0.0
export PORT=5000
export FLASK_ENV=production

# Configuración de seguridad
export SECRET_KEY=tu_secret_key_muy_seguro

# IBM Quantum API (obtén tu token desde https://quantum-computing.ibm.com/)
export IBM_QUANTUM_TOKEN=tu_api_key_de_ibm_quantum

# Configuración de simulación
export MAX_SIMULATION_TIME=600
export MOCK_SIMULATIONS=false
```

**⚠️ IMPORTANTE - SEGURIDAD DE CREDENCIALES:**
- NUNCA incluyas API keys o tokens directamente en el código
- NUNCA subas archivos `.env` al repositorio de Git
- Usa variables de entorno o servicios de gestión de secretos
- Rota tus API keys regularmente
- Para producción, usa servicios como AWS Secrets Manager, Azure Key Vault, o HashiCorp Vault

### Configuración de Base de Datos
```python
# Para producción, configurar base de datos
DATABASE_URL=postgresql://usuario:password@localhost/quantum_simulator
```

### Configuración de Logging
```python
# En config.py
LOG_LEVEL = 'WARNING'  # Para producción
LOG_FILE = '/var/log/quantum_simulator.log'
```

## 📊 Monitoreo y Mantenimiento

### Logs
```bash
# Ver logs en tiempo real
tail -f logs/quantum_simulator.log

# Ver logs de errores
grep ERROR logs/quantum_simulator.log
```

### Health Check
```bash
# Verificar estado del servidor
curl http://localhost:5000/api/molecules

# Verificar WebSocket
curl -i -N -H "Connection: Upgrade" -H "Upgrade: websocket" http://localhost:5000
```

### Backup
```bash
# Backup de la base de datos (si se usa)
pg_dump quantum_simulator > backup_$(date +%Y%m%d).sql

# Backup del código
tar -czf quantum_simulator_backup_$(date +%Y%m%d).tar.gz .
```

## 🚨 Solución de Problemas

### Error: Puerto ocupado
```bash
# Encontrar proceso usando el puerto
lsof -i :5000

# Matar proceso
kill -9 PID_DEL_PROCESO
```

### Error: Módulo no encontrado
```bash
# Verificar instalación
pip list | grep flask

# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

### Error: WebSocket no funciona
```bash
# Verificar que Socket.IO esté instalado
pip install flask-socketio

# Verificar configuración de CORS
# En app.py, verificar cors_allowed_origins
```

### Error: Permisos
```bash
# Dar permisos de ejecución
chmod +x run.py

# Verificar permisos de directorios
chmod 755 templates/ static/
```

## 📈 Optimización

### Para Alto Tráfico
```python
# Usar Gunicorn con múltiples workers
gunicorn -w 8 -b 0.0.0.0:5000 app:app

# Configurar Redis para caché
# Configurar load balancer
```

### Para Simulaciones Intensivas
```python
# Usar Celery para tareas en segundo plano
# Configurar queue de Redis
# Implementar rate limiting
```

## 🔒 Seguridad

### Configuración de Seguridad
```python
# En config.py
SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave_muy_segura'
CORS_ORIGINS = ['https://tu-dominio.com']  # Solo dominios permitidos
```

### HTTPS
```nginx
# Configurar SSL en Nginx
server {
    listen 443 ssl;
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
    }
}
```

## 📱 Despliegue Móvil

### PWA (Progressive Web App)
```html
<!-- En templates/index.html -->
<link rel="manifest" href="/static/manifest.json">
<meta name="theme-color" content="#3498db">
```

### Responsive Design
- La aplicación ya incluye diseño responsive
- Compatible con dispositivos móviles
- Touch-friendly para tablets

## 🧪 Testing en Producción

### Tests de Carga
```bash
# Instalar Apache Bench
sudo apt install apache2-utils

# Test de carga
ab -n 1000 -c 10 http://localhost:5000/api/molecules
```

### Tests de API
```bash
# Test de todas las APIs
curl -X POST http://localhost:5000/api/quantum/simple \
  -H "Content-Type: application/json" \
  -d '{"molecule": "LiH"}'
```

## 📞 Soporte

### Logs de Debug
```bash
# Habilitar debug
export FLASK_DEBUG=1
python app.py
```

### Contacto
- **GitHub Issues:** https://github.com/picapiedra123/cuantica/issues
- **Documentación:** Ver README.md
- **Tests:** python test_simulator.py

---

**¡El Simulador Cuántico está listo para el mundo! 🚀⚛️**
