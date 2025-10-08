#!/usr/bin/env python3
"""
Simulador Cuantico - Demo Simple
Demostracion del simulador cuantico sin servidor web
"""

from quantum_simulator import simulate_molecule, analyze_interaction, quantum_simulator
import time

def print_header():
    """Imprime el encabezado del demo"""
    print("=" * 60)
    print("SIMULADOR CUANTICO - DEMO EN ACCION")
    print("=" * 60)
    print()

def print_section(title):
    """Imprime una seccion"""
    print(f"\n{title}")
    print("-" * 40)

def demo_molecules():
    """Demo: Informacion de moleculas"""
    print_section("INFORMACION DE MOLECULAS")
    
    molecules = quantum_simulator.list_available_molecules()
    print(f"Moleculas disponibles: {', '.join(molecules)}")
    print()
    
    for molecule in molecules:
        info = quantum_simulator.get_molecule_info(molecule)
        print(f"{molecule}:")
        print(f"   Atomos: {', '.join(info['atoms'])}")
        print(f"   Electrones: {info['electrons']}")
        print(f"   Orbitales: {info['orbitals']}")
        print(f"   Longitud de enlace: {info['bond_length']} A")
        print()

def demo_simulations():
    """Demo: Simulaciones cuanticas"""
    print_section("SIMULACIONES CUANTICAS")
    
    molecules = ['LiH', 'H2O', 'Li_GLYCINE']
    
    for molecule in molecules:
        print(f"Simulando {molecule}...")
        
        # Simular con callback de progreso
        progress_values = []
        def progress_callback(progress):
            progress_values.append(progress)
            print(f"   Progreso: {progress}%", end='\r')
        
        start_time = time.time()
        result = simulate_molecule(molecule, progress_callback=progress_callback)
        end_time = time.time()
        
        print(f"\n   Completado en {end_time - start_time:.2f} segundos")
        print(f"   Energia: {result['energy']} Ha")
        print(f"   Fuerza de interaccion: {result['interaction_strength']}")
        print(f"   Tiempo de computo: {result['computation_time']:.2f}s")
        print()

def demo_interactions():
    """Demo: Analisis de interacciones"""
    print_section("ANALISIS DE INTERACCIONES MOLECULARES")
    
    interactions = [
        ('LiH', 'H2O'),
        ('LiH', 'Li_GLYCINE'),
        ('H2O', 'Li_GLYCINE')
    ]
    
    for mol1, mol2 in interactions:
        print(f"Analizando interaccion {mol1} + {mol2}...")
        
        result = analyze_interaction(mol1, mol2)
        
        print(f"   Energia de interaccion: {result['interaction_energy']} Ha")
        print(f"   Tipo de interaccion: {result['interaction_type']}")
        print(f"   Estabilidad: {result['stability']}")
        print()

def demo_api_simulation():
    """Demo: Simulacion como API"""
    print_section("SIMULACION COMO API REST")
    
    # Simular llamada a API
    print("Simulando llamada a API REST...")
    print("   POST /api/quantum/simple")
    print("   Content-Type: application/json")
    print("   Body: {\"molecule\": \"LiH\"}")
    print()
    
    # Ejecutar simulacion
    result = simulate_molecule('LiH')
    
    # Simular respuesta JSON
    api_response = {
        "status": "success",
        "data": {
            "energy": result['energy'],
            "molecule": result['molecule'],
            "interaction_strength": result['interaction_strength'],
            "computation_time": f"{result['computation_time']:.2f} segundos",
            "message": f"Energia de {result['molecule']}: {result['energy']:.4f} Ha"
        }
    }
    
    print("Respuesta de la API:")
    print(f"   Status: {api_response['status']}")
    print(f"   Energia: {api_response['data']['energy']} Ha")
    print(f"   Fuerza: {api_response['data']['interaction_strength']}")
    print(f"   Tiempo: {api_response['data']['computation_time']}")
    print(f"   Mensaje: {api_response['data']['message']}")
    print()

def demo_websocket_simulation():
    """Demo: Simulacion WebSocket"""
    print_section("SIMULACION WEBSOCKET (TIEMPO REAL)")
    
    print("Simulando conexion WebSocket...")
    print("   ws://localhost:5000")
    print("   Evento: start_quantum_simulation")
    print()
    
    # Simular progreso en tiempo real
    molecule = 'Li_GLYCINE'
    print(f"Iniciando simulacion de {molecule}...")
    
    def progress_callback(progress):
        print(f"   Progreso: {progress}% - {progress * 0.1:.1f}s transcurridos")
        time.sleep(0.1)  # Simular tiempo de procesamiento
    
    result = simulate_molecule(molecule, progress_callback=progress_callback)
    
    print(f"\nSimulacion WebSocket completada!")
    print(f"   Energia: {result['energy']} Ha")
    print(f"   Fuerza: {result['interaction_strength']}")
    print(f"   Tiempo total: {result['computation_time']:.2f}s")
    print()

def demo_comparison():
    """Demo: Comparacion de APIs"""
    print_section("COMPARACION DE DIFERENTES METODOS")
    
    molecule = 'H2O'
    methods = [
        ("REST Simple", lambda: simulate_molecule(molecule)),
        ("REST Avanzado", lambda: simulate_molecule(molecule, {"basis_set": "6-31g"})),
        ("Mock API", lambda: {"energy": -0.845, "interaction_strength": "moderada", "computation_time": 1.2})
    ]
    
    print(f"Comparando metodos para {molecule}:")
    print()
    
    for method_name, method_func in methods:
        print(f"{method_name}:")
        
        start_time = time.time()
        result = method_func()
        end_time = time.time()
        
        print(f"   Energia: {result['energy']} Ha")
        print(f"   Fuerza: {result['interaction_strength']}")
        print(f"   Tiempo: {end_time - start_time:.2f}s")
        print()

def main():
    """Funcion principal del demo"""
    print_header()
    
    # Ejecutar demos
    demo_molecules()
    demo_simulations()
    demo_interactions()
    demo_api_simulation()
    demo_websocket_simulation()
    demo_comparison()
    
    # Finalizar
    print("=" * 60)
    print("DEMO COMPLETADO - SIMULADOR CUANTICO EN ACCION")
    print("=" * 60)
    print()
    print("Para usar la interfaz web:")
    print("   1. Ejecutar: python app.py")
    print("   2. Abrir: http://localhost:5000")
    print("   3. Demo interactivo: http://localhost:5000/demo")
    print()
    print("APIs disponibles:")
    print("   - POST /api/quantum/simple")
    print("   - POST /api/quantum/simulate")
    print("   - POST /api/mock/quantum-simulate")
    print("   - WebSocket: ws://localhost:5000")
    print()
    print("El simulador cuantico esta listo para usar!")

if __name__ == "__main__":
    main()