@echo off
echo 🐳 Construyendo imagen Docker...
docker build -t simulador-cuantico .

echo 🚀 Ejecutando simulador cuántico...
docker run -p 5000:5000 --name simulador-cuantico simulador-cuantico



