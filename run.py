#!/usr/bin/env python3
"""
🚀 Simulador Cuántico - Script de Ejecución
Ejecuta el servidor con configuración optimizada
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def check_dependencies():
    """Verifica que las dependencias estén instaladas"""
    try:
        import flask
        import flask_socketio
        import numpy
        print("✅ Dependencias verificadas")
        return True
    except ImportError as e:
        print(f"❌ Dependencia faltante: {e}")
        print("💡 Ejecuta: pip install -r requirements.txt")
        return False

def check_port(port=5000):
    """Verifica si el puerto está disponible"""
    import socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
            print(f"✅ Puerto {port} disponible")
            return True
    except OSError:
        print(f"❌ Puerto {port} ocupado")
        print("💡 Cierra otros servicios o cambia el puerto")
        return False

def create_directories():
    """Crea directorios necesarios"""
    directories = ['templates', 'static', 'logs', 'data']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    print("✅ Directorios creados")

def run_server(host='0.0.0.0', port=5000, debug=True):
    """Ejecuta el servidor Flask"""
    print("🚀 Iniciando Simulador Cuántico...")
    print(f"📡 Servidor: http://{host}:{port}")
    print(f"🌐 Interfaz: http://localhost:{port}")
    print(f"🎮 Demo: http://localhost:{port}/demo")
    print("=" * 50)
    
    # Configurar variables de entorno
    os.environ['FLASK_APP'] = 'app.py'
    os.environ['FLASK_ENV'] = 'development' if debug else 'production'
    
    try:
        # Importar y ejecutar la aplicación
        from app import app, socketio
        socketio.run(app, host=host, port=port, debug=debug)
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido por el usuario")
    except Exception as e:
        print(f"❌ Error ejecutando servidor: {e}")
        sys.exit(1)

def main():
    """Función principal"""
    print("🧪 Simulador Cuántico - Iniciando...")
    print("=" * 50)
    
    # Verificar dependencias
    if not check_dependencies():
        sys.exit(1)
    
    # Crear directorios
    create_directories()
    
    # Verificar puerto
    port = 5000
    if not check_port(port):
        print(f"💡 Intentando puerto alternativo...")
        for alt_port in [5001, 5002, 5003, 8000, 8080]:
            if check_port(alt_port):
                port = alt_port
                break
        else:
            print("❌ No se encontró puerto disponible")
            sys.exit(1)
    
    # Ejecutar servidor
    run_server(port=port)

if __name__ == "__main__":
    main()
