#!/usr/bin/env python3
"""
Simulador Cuantico - Servidor con IBM Quantum
Version que integra hardware cuantico real de IBM
"""

import os
from flask import Flask, jsonify, request, render_template
import json
import threading
import time
from quantum_simulator import simulate_molecule, analyze_interaction, quantum_simulator
try:
    from ibm_quantum_real import simulate_molecule_ibm, ibm_quantum_simulator
    print("IBM Quantum REAL cargado correctamente")
except ImportError as e:
    print(f"Error cargando IBM Quantum Real: {e}")
    # Fallback si no se puede importar IBM Quantum
    simulate_molecule_ibm = None
    ibm_quantum_simulator = None

# Inicializar Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

# Almacenamiento para simulaciones en lote
simulation_results = {}

# ============================================================================
# PAGINAS WEB
# ============================================================================

@app.route('/')
def index():
    """Pagina principal"""
    return render_template('index.html')

@app.route('/demo')
def demo():
    """Pagina de demo"""
    return render_template('demo.html')

@app.route('/ibm-quantum')
def ibm_quantum_page():
    """Pagina de IBM Quantum"""
    return render_template('ibm_quantum.html')

# ============================================================================
# API REST ENDPOINTS
# ============================================================================

@app.route('/api/quantum/simple', methods=['POST'])
def simple_simulation():
    """API REST simple para simulacion cuantica"""
    try:
        data = request.json or {}
        molecule = data.get('molecule', 'LiH')
        parameters = data.get('parameters', {})
        
        result = simulate_molecule(molecule, parameters)
        
        return jsonify({
            'status': 'success',
            'data': {
                'energy': round(result['energy'], 4),
                'molecule': molecule,
                'interaction_strength': result['interaction_strength'],
                'computation_time': f"{result['computation_time']:.2f} segundos",
                'message': f'Energia de {molecule}: {result["energy"]:.4f} Ha'
            }
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/api/quantum/simulate', methods=['POST'])
def advanced_simulation():
    """API REST avanzada para simulacion cuantica"""
    try:
        data = request.json or {}
        molecule = data.get('molecule', 'LiH')
        parameters = data.get('parameters', {})
        
        result = simulate_molecule(molecule, parameters)
        
        return jsonify({
            'success': True,
            'energy': result['energy'],
            'interaction_strength': result.get('interaction_strength', 'medium'),
            'computation_time': result.get('computation_time', 0),
            'message': f'Simulacion de {molecule} completada',
            'molecule': molecule,
            'status': 'completed'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Error en simulacion cuantica'
        }), 500

# ============================================================================
# IBM QUANTUM ENDPOINTS
# ============================================================================

@app.route('/api/ibm-quantum/simulate', methods=['POST'])
def ibm_quantum_simulation():
    """Simulacion usando IBM Quantum hardware real"""
    try:
        if not simulate_molecule_ibm:
            return jsonify({
                'success': False,
                'error': 'IBM Quantum no disponible',
                'message': 'Módulo IBM Quantum no instalado correctamente'
            }), 500
        
        data = request.json or {}
        molecule = data.get('molecule', 'LiH')
        parameters = data.get('parameters', {})
        api_token = data.get('api_token')
        
        # Ejecutar simulacion en IBM Quantum
        result = simulate_molecule_ibm(molecule, parameters, api_token)
        
        return jsonify({
            'success': True,
            'energy': result['energy'],
            'interaction_strength': result['interaction_strength'],
            'computation_time': result['computation_time'],
            'molecule': molecule,
            'backend_used': result.get('backend_used', 'local'),
            'quantum_circuit_depth': result.get('quantum_circuit_depth', 0),
            'shots': result.get('shots', 1024),
            'message': f'Simulacion IBM Quantum de {molecule} completada',
            'status': 'completed'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Error en simulacion IBM Quantum'
        }), 500

@app.route('/api/ibm-quantum/backends')
def get_ibm_backends():
    """Obtiene lista de backends de IBM Quantum disponibles"""
    try:
        if not ibm_quantum_simulator:
            return jsonify({
                'success': False,
                'error': 'IBM Quantum no disponible',
                'message': 'Módulo IBM Quantum no instalado correctamente'
            }), 500
        
        backends = ibm_quantum_simulator.get_available_backends()
        
        return jsonify({
            'success': True,
            'backends': backends,
            'count': len(backends)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Error obteniendo backends de IBM Quantum'
        }), 500

@app.route('/api/ibm-quantum/status')
def get_ibm_status():
    """Obtiene estado del backend actual de IBM Quantum"""
    try:
        if not ibm_quantum_simulator:
            return jsonify({
                'success': False,
                'error': 'IBM Quantum no disponible',
                'message': 'Módulo IBM Quantum no instalado correctamente'
            }), 500
        
        status = ibm_quantum_simulator.get_backend_status()
        
        return jsonify({
            'success': True,
            'status': status
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Error obteniendo estado de IBM Quantum'
        }), 500

@app.route('/api/ibm-quantum/configure', methods=['POST'])
def configure_ibm_quantum():
    """Configura IBM Quantum con API token"""
    try:
        data = request.json or {}
        api_token = data.get('api_token')
        
        if not api_token:
            return jsonify({
                'success': False,
                'error': 'API token requerido',
                'message': 'Proporciona tu API token de IBM Quantum'
            }), 400
        
        # Configurar simulador con nuevo token
        if not simulate_molecule_ibm:
            return jsonify({
                'success': False,
                'error': 'IBM Quantum no disponible',
                'message': 'Módulo IBM Quantum no instalado correctamente'
            }), 500
        
        # Configurar simulador con nuevo token
        global ibm_quantum_simulator
        try:
            from ibm_quantum_real import IBMQuantumReal
            ibm_quantum_simulator = IBMQuantumReal(api_token)
        except ImportError:
            return jsonify({
                'success': False,
                'error': 'IBM Quantum no disponible',
                'message': 'Módulo IBM Quantum no instalado correctamente'
            }), 500
        
        return jsonify({
            'success': True,
            'message': 'IBM Quantum configurado correctamente',
            'backends_available': len(ibm_quantum_simulator.get_available_backends())
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Error configurando IBM Quantum'
        }), 500

# ============================================================================
# SIMULACION POR LOTE
# ============================================================================

@app.route('/api/quantum/start-simulation', methods=['POST'])
def start_simulation():
    """Inicia simulacion en segundo plano"""
    simulation_id = f"sim_{int(time.time())}"
    
    data = request.json or {}
    molecule = data.get('molecule', 'LiH')
    parameters = data.get('parameters', {})
    use_ibm_quantum = data.get('use_ibm_quantum', False)
    api_token = data.get('api_token')
    
    # Ejecutar en segundo plano
    def run_simulation():
        try:
            if use_ibm_quantum:
                result = simulate_molecule_ibm(molecule, parameters, api_token)
            else:
                result = simulate_molecule(molecule, parameters)
            
            simulation_results[simulation_id] = {
                'status': 'completed',
                'result': result,
                'molecule': molecule,
                'backend_used': result.get('backend_used', 'local')
            }
        except Exception as e:
            simulation_results[simulation_id] = {
                'status': 'error', 
                'error': str(e),
                'molecule': molecule
            }
    
    thread = threading.Thread(target=run_simulation)
    thread.start()
    
    return jsonify({
        'simulation_id': simulation_id,
        'status': 'started',
        'message': 'Simulacion iniciada en segundo plano',
        'molecule': molecule,
        'use_ibm_quantum': use_ibm_quantum
    })

@app.route('/api/quantum/status/<simulation_id>')
def get_status(simulation_id):
    """Obtiene estado de simulacion por ID"""
    result = simulation_results.get(simulation_id, {'status': 'not_found'})
    return jsonify(result)

# ============================================================================
# OTROS ENDPOINTS
# ============================================================================

@app.route('/api/molecules')
def list_molecules():
    """Lista moleculas disponibles"""
    molecules = quantum_simulator.list_available_molecules()
    return jsonify({
        'molecules': molecules,
        'count': len(molecules)
    })

@app.route('/api/molecules/<molecule>')
def get_molecule_info(molecule):
    """Obtiene informacion de una molecula especifica"""
    try:
        info = quantum_simulator.get_molecule_info(molecule)
        return jsonify({
            'success': True,
            'molecule': molecule,
            'info': info
        })
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404

@app.route('/api/analyze-interaction', methods=['POST'])
def analyze_molecular_interaction():
    """Analiza interaccion entre dos moleculas"""
    try:
        data = request.json or {}
        molecule1 = data.get('molecule1', 'LiH')
        molecule2 = data.get('molecule2', 'H2O')
        
        result = analyze_interaction(molecule1, molecule2)
        
        return jsonify({
            'success': True,
            'interaction': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================================================
# EJECUTAR SERVIDOR
# ============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("SIMULADOR CUANTICO - SERVIDOR CON IBM QUANTUM")
    print("=" * 60)
    print("Servidor iniciando...")
    print("API REST disponible en: http://localhost:5000")
    print("Interfaz web en: http://localhost:5000")
    print("Demo en: http://localhost:5000/demo")
    print("IBM Quantum en: http://localhost:5000/ibm-quantum")
    print("=" * 60)
    print()
    print("Para usar IBM Quantum:")
    print("1. Obtener API token de: https://quantum-computing.ibm.com/")
    print("2. Configurar token en la interfaz web")
    print("3. Ejecutar simulaciones en hardware cuantico real")
    print()
    print("Para detener el servidor: Ctrl+C")
    print()
    
    # Ejecutar servidor Flask
    app.run(host='0.0.0.0', port=5000, debug=True)
