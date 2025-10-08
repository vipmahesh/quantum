# 🐳 Guía de Docker - Simulador Cuántico

## 📋 ¿Qué archivos Docker SE SUBEN al repositorio?

### ✅ Archivos que SÍ se deben subir:

- ✅ `Dockerfile` - Instrucciones para construir la imagen
- ✅ `docker-compose.yml` - Configuración de servicios
- ✅ `.dockerignore` - Archivos a excluir al construir
- ✅ `docker-run.sh` / `docker-run.bat` - Scripts de ejecución

### ❌ Archivos que NO se deben subir:

- ❌ Imágenes Docker construidas (`.tar`, `.tar.gz`)
- ❌ Contenedores en ejecución
- ❌ Volúmenes con datos sensibles
- ❌ `docker-compose.override.yml` (configuración local)
- ❌ Archivos `.env` con credenciales

## 🚀 Uso Rápido

### Opción 1: Con docker-compose (Recomendado)

```bash
# 1. Configurar variables de entorno
export IBM_QUANTUM_TOKEN=tu_token_aqui
export SECRET_KEY=tu_clave_secreta

# 2. Ejecutar
docker-compose up -d

# 3. Ver logs
docker-compose logs -f

# 4. Detener
docker-compose down
```

### Opción 2: Con Docker directo

```bash
# 1. Construir imagen
docker build -t quantum-simulator .

# 2. Ejecutar contenedor
docker run -d \
  -p 5000:5000 \
  -e IBM_QUANTUM_TOKEN=tu_token \
  -e SECRET_KEY=tu_clave \
  --name quantum-sim \
  quantum-simulator

# 3. Ver logs
docker logs -f quantum-sim

# 4. Detener
docker stop quantum-sim
docker rm quantum-sim
```

## 🔧 Configuración de Variables de Entorno

### Método 1: Variables de entorno del sistema

**Linux/Mac:**
```bash
export IBM_QUANTUM_TOKEN=tu_token_aqui
export SECRET_KEY=tu_clave_secreta
docker-compose up -d
```

**Windows PowerShell:**
```powershell
$env:IBM_QUANTUM_TOKEN="tu_token_aqui"
$env:SECRET_KEY="tu_clave_secreta"
docker-compose up -d
```

### Método 2: Archivo .env (Desarrollo local)

Crea un archivo `.env` en la raíz del proyecto:

```env
IBM_QUANTUM_TOKEN=tu_token_aqui
SECRET_KEY=tu_clave_secreta
FLASK_ENV=development
FLASK_DEBUG=True
```

**⚠️ IMPORTANTE:** El archivo `.env` está en `.gitignore` y NO debe ser subido al repositorio.

### Método 3: Docker Secrets (Producción)

Para entornos de producción, usa Docker Secrets:

```bash
# Crear secrets
echo "tu_token" | docker secret create ibm_quantum_token -
echo "tu_clave" | docker secret create secret_key -

# Usar en docker-compose
docker stack deploy -c docker-compose.prod.yml quantum
```

## 📦 Estructura de la Imagen Docker

```
Imagen: quantum-simulator
├── Base: python:3.11-slim
├── Dependencias:
│   ├── qiskit==0.45.0
│   ├── flask==2.3.3
│   ├── qiskit-ibm-runtime==0.15.0
│   └── requests==2.31.0
├── Puerto expuesto: 5000
└── Comando: python server_real_ibm.py
```

## 🔍 Comandos Útiles

### Gestión de Contenedores

```bash
# Ver contenedores en ejecución
docker ps

# Ver todos los contenedores
docker ps -a

# Ver logs
docker-compose logs -f quantum-simulator

# Entrar al contenedor
docker exec -it quantum-simulator bash

# Reiniciar contenedor
docker-compose restart

# Ver uso de recursos
docker stats quantum-simulator
```

### Gestión de Imágenes

```bash
# Listar imágenes
docker images

# Eliminar imagen
docker rmi quantum-simulator

# Reconstruir sin cache
docker-compose build --no-cache

# Ver historial de imagen
docker history quantum-simulator
```

### Limpieza

```bash
# Limpiar contenedores detenidos
docker container prune

# Limpiar imágenes sin usar
docker image prune

# Limpiar todo (¡CUIDADO!)
docker system prune -a

# Limpiar volúmenes
docker volume prune
```

## 🔒 Seguridad con Docker

### Buenas Prácticas

1. **No incluir credenciales en la imagen:**
   ```dockerfile
   # ❌ MAL
   ENV IBM_QUANTUM_TOKEN=Q8MuqQmCnwTc5...
   
   # ✅ BIEN
   ENV IBM_QUANTUM_TOKEN=${IBM_QUANTUM_TOKEN}
   ```

2. **Usar .dockerignore:**
   - Excluye archivos sensibles
   - Reduce tamaño de imagen
   - Mejora tiempo de build

3. **Usuario no-root:**
   ```dockerfile
   RUN useradd -m -u 1000 quantum
   USER quantum
   ```

4. **Escanear vulnerabilidades:**
   ```bash
   docker scan quantum-simulator
   ```

## 📊 Monitoreo

### Health Checks

El docker-compose incluye health checks automáticos:

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:5000/api/molecules"]
  interval: 30s
  timeout: 10s
  retries: 3
```

Ver estado:
```bash
docker inspect --format='{{.State.Health.Status}}' quantum-simulator
```

### Logs

```bash
# Ver logs en tiempo real
docker-compose logs -f

# Ver últimas 100 líneas
docker-compose logs --tail=100

# Ver logs de un servicio específico
docker-compose logs quantum-simulator
```

## 🌐 Despliegue en Producción

### Docker Swarm

```bash
# Inicializar swarm
docker swarm init

# Desplegar stack
docker stack deploy -c docker-compose.yml quantum

# Ver servicios
docker service ls

# Escalar
docker service scale quantum_quantum-simulator=3
```

### Kubernetes

Crear archivo `k8s-deployment.yml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: quantum-simulator
spec:
  replicas: 3
  selector:
    matchLabels:
      app: quantum-simulator
  template:
    metadata:
      labels:
        app: quantum-simulator
    spec:
      containers:
      - name: quantum-simulator
        image: quantum-simulator:latest
        ports:
        - containerPort: 5000
        env:
        - name: IBM_QUANTUM_TOKEN
          valueFrom:
            secretKeyRef:
              name: quantum-secrets
              key: ibm-token
```

## 🚨 Solución de Problemas

### Puerto 5000 ocupado

```bash
# Cambiar puerto en docker-compose.yml
ports:
  - "8080:5000"  # Usar puerto 8080 en el host
```

### Error de permisos

```bash
# Ejecutar como root (solo para debug)
docker-compose run --user root quantum-simulator bash
```

### Imagen muy grande

```bash
# Ver capas de la imagen
docker history quantum-simulator

# Optimizar Dockerfile con multi-stage builds
# Limpiar cache de pip
# Usar imágenes base más pequeñas
```

### Contenedor se detiene inmediatamente

```bash
# Ver logs de error
docker logs quantum-simulator

# Verificar comando de inicio
docker inspect quantum-simulator
```

## 📚 Recursos

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Best Practices for Dockerfile](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Docker Security](https://docs.docker.com/engine/security/)

## 🎓 Próximos Pasos

1. ✅ Construir la imagen localmente
2. ✅ Probar con docker-compose
3. ✅ Verificar health checks
4. ✅ Revisar logs
5. ✅ Configurar para producción

---

**¡Docker hace que el despliegue sea reproducible y consistente! 🐳🚀**

