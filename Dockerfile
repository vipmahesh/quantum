# Usar Python 3.11 en Ubuntu
FROM python:3.11-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos del proyecto
COPY . .

# Instalar dependencias de Python - evitar conflicto entre provider y runtime
RUN pip install --no-cache-dir qiskit==0.45.0
RUN pip install --no-cache-dir flask==2.3.3 requests==2.31.0
RUN pip install --no-cache-dir qiskit-ibm-runtime==0.15.0

# Exponer puerto
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "server_real_ibm.py"]



