#!/usr/bin/env python3
"""
Simulador Cuantico - Servidor Hibrido
Version que funciona con y sin WebSocket
"""

import os
from flask import Flask, jsonify, request, render_template
import json
import threading
import time
from quantum_simulator import simulate_molecule, analyze_interaction, quantum_simulator

# Inicializar Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

# Almacenamiento para simulaciones en lote
simulation_results = {}

# ============================================================================
# API REST ENDPOINTS
# ============================================================================

@app.route('/')
def index():
    """Pagina principal"""
    return render_template('index.html')

@app.route('/demo')
def demo():
    """Pagina de demo"""
    return render_template('demo.html')

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

@app.route('/api/mock/quantum-simulate', methods=['POST'])
def mock_simulation():
    """API Mock para desarrollo"""
    import random
    import time
    
    time.sleep(1)  # Simular tiempo de procesamiento
    
    mock_results = {
        'LiH': {'energy': -1.088, 'strength': 'fuerte'},
        'Li_GLYCINE': {'energy': -2.152, 'strength': 'muy_fuerte'},
        'H2O': {'energy': -0.845, 'strength': 'moderada'}
    }
    
    data = request.json or {}
    molecule = data.get('molecule', 'LiH')
    result = mock_results.get(molecule, mock_results['LiH'])
    
    return jsonify({
        'success': True,
        'energy': result['energy'] + random.uniform(-0.1, 0.1),
        'interaction_strength': result['strength'],
        'computation_time': f"{random.uniform(1, 5):.2f} segundos",
        'message': f'Simulacion mock de {molecule} completada',
        'molecule': molecule
    })

# ============================================================================
# SIMULACION POR LOTE (SIN WEBSOCKET)
# ============================================================================

@app.route('/api/quantum/start-simulation', methods=['POST'])
def start_simulation():
    """Inicia simulacion en segundo plano"""
    simulation_id = f"sim_{int(time.time())}"
    
    data = request.json or {}
    molecule = data.get('molecule', 'LiH')
    parameters = data.get('parameters', {})
    
    # Ejecutar en segundo plano
    def run_simulation():
        try:
            result = simulate_molecule(molecule, parameters)
            simulation_results[simulation_id] = {
                'status': 'completed',
                'result': result,
                'molecule': molecule
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
        'molecule': molecule
    })

@app.route('/api/quantum/status/<simulation_id>')
def get_status(simulation_id):
    """Obtiene estado de simulacion por ID"""
    result = simulation_results.get(simulation_id, {'status': 'not_found'})
    return jsonify(result)

# ============================================================================
# WEBSOCKET SIMULADO (POLLING)
# ============================================================================

@app.route('/api/websocket/simulate', methods=['POST'])
def websocket_simulation():
    """Simula WebSocket con polling"""
    data = request.json or {}
    molecule = data.get('molecule', 'LiH')
    parameters = data.get('parameters', {})
    
    # Crear ID de simulacion
    simulation_id = f"ws_{int(time.time())}"
    
    # Ejecutar simulacion con progreso
    def run_with_progress():
        progress_values = []
        
        def progress_callback(progress):
            progress_values.append(progress)
            simulation_results[f"{simulation_id}_progress"] = {
                'progress': progress,
                'message': f'Completado: {progress}%'
            }
        
        try:
            result = simulate_molecule(molecule, parameters, progress_callback=progress_callback)
            simulation_results[simulation_id] = {
                'status': 'completed',
                'result': result,
                'molecule': molecule
            }
        except Exception as e:
            simulation_results[simulation_id] = {
                'status': 'error',
                'error': str(e),
                'molecule': molecule
            }
    
    thread = threading.Thread(target=run_with_progress)
    thread.start()
    
    return jsonify({
        'simulation_id': simulation_id,
        'status': 'started',
        'message': 'Simulacion WebSocket iniciada'
    })

@app.route('/api/websocket/progress/<simulation_id>')
def get_websocket_progress(simulation_id):
    """Obtiene progreso de simulacion WebSocket"""
    progress = simulation_results.get(f"{simulation_id}_progress", {'progress': 0})
    result = simulation_results.get(simulation_id, {'status': 'running'})
    
    return jsonify({
        'progress': progress,
        'result': result
    })

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
    print("SIMULADOR CUANTICO - SERVIDOR HIBRIDO")
    print("=" * 60)
    print("Servidor iniciando...")
    print("API REST disponible en: http://localhost:5000")
    print("Interfaz web en: http://localhost:5000")
    print("Demo en: http://localhost:5000/demo")
    print("WebSocket simulado: /api/websocket/simulate")
    print("=" * 60)
    print()
    print("Para detener el servidor: Ctrl+C")
    print()
    
    # Ejecutar servidor Flask
    app.run(host='0.0.0.0', port=5000, debug=True)



