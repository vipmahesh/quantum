"""
Servidor Flask con conexión REAL a IBM Quantum
"""

from flask import Flask, render_template, request, jsonify
import json
import time

# Intentar importar el módulo REAL de IBM Quantum
try:
    from ibm_quantum_real_connection import (
        simulate_molecule_ibm_real, 
        get_available_backends_real,
        configure_ibm_quantum_real
    )
    IBM_QUANTUM_AVAILABLE = True
    print("IBM Quantum REAL disponible")
except ImportError as e:
    print(f"IBM Quantum REAL no disponible: {e}")
    IBM_QUANTUM_AVAILABLE = False

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/demo')
def demo():
    return render_template('demo.html')

@app.route('/ibm-quantum')
def ibm_quantum():
    return render_template('ibm_quantum.html')

@app.route('/api/ibm-quantum/configure', methods=['POST'])
def configure_ibm_quantum():
    """Configurar conexión REAL a IBM Quantum"""
    if not IBM_QUANTUM_AVAILABLE:
        return jsonify({
            'success': False,
            'message': 'IBM Quantum no disponible'
        })
    
    try:
        data = request.get_json()
        api_token = data.get('api_token', '')
        
        if not api_token:
            return jsonify({
                'success': False,
                'message': 'API token requerido'
            })
        
        # Configurar conexión REAL
        success = configure_ibm_quantum_real(api_token)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'IBM Quantum REAL configurado correctamente'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Error conectando a IBM Quantum REAL'
            })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

@app.route('/api/ibm-quantum/backends', methods=['GET'])
def get_ibm_backends():
    """Obtener backends REALES de IBM Quantum"""
    if not IBM_QUANTUM_AVAILABLE:
        return jsonify({
            'success': False,
            'backends': [],
            'message': 'IBM Quantum no disponible'
        })
    
    try:
        backends = get_available_backends_real()
        return jsonify({
            'success': True,
            'backends': backends,
            'count': len(backends)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'backends': [],
            'message': f'Error: {str(e)}'
        })

@app.route('/api/ibm-quantum/simulate', methods=['POST'])
def simulate_ibm_quantum():
    """Simular en hardware cuántico REAL"""
    if not IBM_QUANTUM_AVAILABLE:
        return jsonify({
            'success': False,
            'message': 'IBM Quantum no disponible'
        })
    
    try:
        data = request.get_json()
        molecule = data.get('molecule', 'LiH')
        backend = data.get('backend', None)
        
        # Simular en hardware REAL
        result = simulate_molecule_ibm_real(molecule, backend)
        
        return jsonify({
            'success': True,
            'result': result
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

@app.route('/api/ibm-quantum/status', methods=['GET'])
def get_ibm_status():
    """Obtener estado de IBM Quantum"""
    return jsonify({
        'available': IBM_QUANTUM_AVAILABLE,
        'connected': IBM_QUANTUM_AVAILABLE,
        'message': 'IBM Quantum REAL disponible' if IBM_QUANTUM_AVAILABLE else 'IBM Quantum no disponible'
    })

if __name__ == '__main__':
    print("============================================================")
    print("SIMULADOR CUANTICO - SERVIDOR CON IBM QUANTUM REAL")
    print("============================================================")
    print("Servidor iniciando...")
    print("API REST disponible en: http://localhost:5000")
    print("Interfaz web en: http://localhost:5000")
    print("Demo en: http://localhost:5000/demo")
    print("IBM Quantum REAL en: http://localhost:5000/ibm-quantum")
    print("============================================================")
    print("Para usar IBM Quantum REAL:")
    print("1. Obtener API token de: https://quantum-computing.ibm.com/")
    print("2. Configurar token en la interfaz web")
    print("3. Ejecutar simulaciones en hardware cuantico REAL")
    print("Para detener el servidor: Ctrl+C")
    
    app.run(host='0.0.0.0', port=5000, debug=True)



