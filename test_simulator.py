#!/usr/bin/env python3
"""
🧪 Simulador Cuántico - Tests
Pruebas unitarias para el simulador cuántico
"""

import unittest
import sys
import os
import time
import json
from unittest.mock import patch, MagicMock

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from quantum_simulator import QuantumSimulator, simulate_molecule, analyze_interaction

class TestQuantumSimulator(unittest.TestCase):
    """Tests para el simulador cuántico"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.simulator = QuantumSimulator()
    
    def test_simulator_initialization(self):
        """Test: Inicialización del simulador"""
        self.assertIsInstance(self.simulator, QuantumSimulator)
        self.assertIsNotNone(self.simulator.molecule_data)
    
    def test_available_molecules(self):
        """Test: Moléculas disponibles"""
        molecules = self.simulator.list_available_molecules()
        self.assertIn('LiH', molecules)
        self.assertIn('Li_GLYCINE', molecules)
        self.assertIn('H2O', molecules)
        self.assertEqual(len(molecules), 3)
    
    def test_molecule_info(self):
        """Test: Información de moléculas"""
        # LiH
        lih_info = self.simulator.get_molecule_info('LiH')
        self.assertEqual(lih_info['atoms'], ['Li', 'H'])
        self.assertEqual(lih_info['electrons'], 4)
        
        # Li_GLYCINE
        glycine_info = self.simulator.get_molecule_info('Li_GLYCINE')
        self.assertEqual(glycine_info['atoms'], ['Li', 'C', 'N', 'O', 'H'])
        self.assertEqual(glycine_info['electrons'], 32)
        
        # H2O
        h2o_info = self.simulator.get_molecule_info('H2O')
        self.assertEqual(h2o_info['atoms'], ['H', 'O', 'H'])
        self.assertEqual(h2o_info['electrons'], 10)
    
    def test_invalid_molecule(self):
        """Test: Molécula inválida"""
        with self.assertRaises(ValueError):
            self.simulator.get_molecule_info('INVALID')
    
    def test_simulate_molecule(self):
        """Test: Simulación de molécula"""
        result = self.simulator.simulate_molecule('LiH')
        
        # Verificar estructura del resultado
        self.assertIn('energy', result)
        self.assertIn('interaction_strength', result)
        self.assertIn('computation_time', result)
        self.assertIn('molecule', result)
        self.assertIn('status', result)
        
        # Verificar tipos de datos
        self.assertIsInstance(result['energy'], float)
        self.assertIsInstance(result['interaction_strength'], str)
        self.assertIsInstance(result['computation_time'], float)
        self.assertEqual(result['molecule'], 'LiH')
        self.assertEqual(result['status'], 'success')
    
    def test_simulate_with_parameters(self):
        """Test: Simulación con parámetros"""
        parameters = {
            'basis_set': 'sto3g',
            'optimizer': 'COBYLA'
        }
        
        result = self.simulator.simulate_molecule('LiH', parameters)
        
        self.assertIn('parameters_used', result)
        self.assertEqual(result['parameters_used'], parameters)
    
    def test_progress_callback(self):
        """Test: Callback de progreso"""
        progress_values = []
        
        def progress_callback(progress):
            progress_values.append(progress)
        
        result = self.simulator.simulate_molecule('LiH', progress_callback=progress_callback)
        
        # Verificar que se llamó el callback
        self.assertGreater(len(progress_values), 0)
        self.assertEqual(progress_values[-1], 100)  # Último valor debe ser 100%
    
    def test_classify_interaction(self):
        """Test: Clasificación de interacciones"""
        # Muy fuerte
        self.assertEqual(self.simulator._classify_interaction(-2.5), "muy_fuerte")
        
        # Fuerte
        self.assertEqual(self.simulator._classify_interaction(-1.8), "fuerte")
        
        # Moderada
        self.assertEqual(self.simulator._classify_interaction(-1.2), "moderada")
        
        # Débil
        self.assertEqual(self.simulator._classify_interaction(-0.8), "debil")
        
        # Muy débil
        self.assertEqual(self.simulator._classify_interaction(-0.2), "muy_debil")
    
    def test_calculate_energy(self):
        """Test: Cálculo de energía"""
        energy = self.simulator._calculate_energy('LiH', {})
        self.assertIsInstance(energy, float)
        self.assertLess(energy, 0)  # Energía debe ser negativa
    
    def test_calculate_orbitals(self):
        """Test: Cálculo de orbitales"""
        orbitals = self.simulator._calculate_orbitals('LiH')
        
        self.assertIsInstance(orbitals, list)
        self.assertEqual(len(orbitals), 2)  # LiH tiene 2 orbitales
        
        for orbital in orbitals:
            self.assertIn('index', orbital)
            self.assertIn('energy', orbital)
            self.assertIn('occupation', orbital)
            self.assertIn('symmetry', orbital)
    
    def test_calculate_electron_density(self):
        """Test: Cálculo de densidad electrónica"""
        density = self.simulator._calculate_electron_density('LiH')
        
        self.assertIsInstance(density, list)
        self.assertEqual(len(density), 50)  # 50 puntos
        
        for point in density:
            self.assertIsInstance(point, float)
            self.assertGreaterEqual(point, 0)  # Densidad no negativa

class TestSimulationFunctions(unittest.TestCase):
    """Tests para funciones de simulación"""
    
    def test_simulate_molecule_function(self):
        """Test: Función simulate_molecule"""
        result = simulate_molecule('LiH')
        
        self.assertIn('energy', result)
        self.assertIn('interaction_strength', result)
        self.assertEqual(result['molecule'], 'LiH')
    
    def test_analyze_interaction(self):
        """Test: Análisis de interacción"""
        result = analyze_interaction('LiH', 'H2O')
        
        self.assertIn('molecule1', result)
        self.assertIn('molecule2', result)
        self.assertIn('interaction_energy', result)
        self.assertIn('interaction_type', result)
        self.assertIn('stability', result)
        
        self.assertEqual(result['molecule1'], 'LiH')
        self.assertEqual(result['molecule2'], 'H2O')
        self.assertIsInstance(result['interaction_energy'], float)

class TestAPIIntegration(unittest.TestCase):
    """Tests de integración con la API"""
    
    def setUp(self):
        """Configuración para tests de API"""
        self.app = None
        self.client = None
    
    def test_app_import(self):
        """Test: Importación de la aplicación Flask"""
        try:
            from app import app
            self.assertIsNotNone(app)
            self.app = app
        except ImportError as e:
            self.fail(f"No se pudo importar la aplicación Flask: {e}")
    
    def test_app_configuration(self):
        """Test: Configuración de la aplicación"""
        if self.app:
            self.assertIsNotNone(self.app.config.get('SECRET_KEY'))
    
    def test_quantum_simulator_import(self):
        """Test: Importación del simulador cuántico"""
        try:
            from quantum_simulator import quantum_simulator
            self.assertIsNotNone(quantum_simulator)
        except ImportError as e:
            self.fail(f"No se pudo importar el simulador cuántico: {e}")

class TestPerformance(unittest.TestCase):
    """Tests de rendimiento"""
    
    def test_simulation_speed(self):
        """Test: Velocidad de simulación"""
        start_time = time.time()
        result = simulate_molecule('LiH')
        end_time = time.time()
        
        simulation_time = end_time - start_time
        
        # La simulación debe completarse en menos de 5 segundos
        self.assertLess(simulation_time, 5.0)
        
        # Verificar que el tiempo reportado es razonable
        self.assertLess(result['computation_time'], 5.0)
    
    def test_multiple_simulations(self):
        """Test: Múltiples simulaciones"""
        molecules = ['LiH', 'H2O', 'Li_GLYCINE']
        results = []
        
        start_time = time.time()
        
        for molecule in molecules:
            result = simulate_molecule(molecule)
            results.append(result)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Verificar que todas las simulaciones se completaron
        self.assertEqual(len(results), 3)
        
        # Verificar que el tiempo total es razonable
        self.assertLess(total_time, 15.0)
        
        # Verificar que cada resultado es válido
        for result in results:
            self.assertIn('energy', result)
            self.assertIn('status', result)
            self.assertEqual(result['status'], 'success')

class TestErrorHandling(unittest.TestCase):
    """Tests de manejo de errores"""
    
    def test_invalid_molecule_simulation(self):
        """Test: Simulación con molécula inválida"""
        with self.assertRaises(ValueError):
            simulate_molecule('INVALID_MOLECULE')
    
    def test_simulation_with_none_parameters(self):
        """Test: Simulación con parámetros None"""
        result = simulate_molecule('LiH', None)
        self.assertIn('energy', result)
        self.assertEqual(result['status'], 'success')
    
    def test_analyze_interaction_invalid_molecules(self):
        """Test: Análisis con moléculas inválidas"""
        # Esto debería funcionar ya que analyze_interaction no valida las moléculas
        result = analyze_interaction('INVALID1', 'INVALID2')
        self.assertIn('molecule1', result)
        self.assertIn('molecule2', result)

def run_tests():
    """Ejecuta todos los tests"""
    print("Ejecutando tests del Simulador Cuantico...")
    print("=" * 50)
    
    # Crear suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar tests
    suite.addTests(loader.loadTestsFromTestCase(TestQuantumSimulator))
    suite.addTests(loader.loadTestsFromTestCase(TestSimulationFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestAPIIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformance))
    suite.addTests(loader.loadTestsFromTestCase(TestErrorHandling))
    
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Mostrar resumen
    print("\n" + "=" * 50)
    print(f"Tests ejecutados: {result.testsRun}")
    print(f"Fallos: {len(result.failures)}")
    print(f"Errores: {len(result.errors)}")
    
    if result.failures:
        print("\nFallos:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    if result.errors:
        print("\nErrores:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    if result.wasSuccessful():
        print("\nTodos los tests pasaron correctamente!")
        return True
    else:
        print("\nAlgunos tests fallaron")
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
