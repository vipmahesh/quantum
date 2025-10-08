#!/usr/bin/env python3
"""
Simulador Cuantico - Servidor Simple
Version simplificada sin WebSocket para evitar problemas
"""

import os
from flask import Flask, jsonify, request, render_template
import json
from quantum_simulator import simulate_molecule, analyze_interaction, quantum_simulator

# Inicializar Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

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
    print("SIMULADOR CUANTICO - SERVIDOR SIMPLE")
    print("=" * 60)
    print("Servidor iniciando...")
    print("API REST disponible en: http://localhost:5000")
    print("Interfaz web en: http://localhost:5000")
    print("Demo en: http://localhost:5000/demo")
    print("=" * 60)
    print()
    print("Para detener el servidor: Ctrl+C")
    print()
    
    # Ejecutar servidor Flask simple
    app.run(host='0.0.0.0', port=5000, debug=True)



