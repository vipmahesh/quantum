"""
🧪 Simulador Cuántico - Configuración
Configuración centralizada para el simulador cuántico
"""

import os
from pathlib import Path

# ============================================================================
# 🏗️ CONFIGURACIÓN BASE
# ============================================================================

class Config:
    """Configuración base"""
    
    # Configuración de la aplicación
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'quantum_simulator_secret_key_2024'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Configuración del servidor
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    
    # Configuración de WebSocket
    SOCKETIO_ASYNC_MODE = 'eventlet'
    SOCKETIO_CORS_ALLOWED_ORIGINS = "*"
    
    # Configuración de logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = 'logs/quantum_simulator.log'
    
    # Configuración de simulación
    MAX_SIMULATION_TIME = 300  # 5 minutos
    DEFAULT_BASIS_SET = 'sto3g'
    DEFAULT_OPTIMIZER = 'COBYLA'
    
    # Moléculas soportadas
    SUPPORTED_MOLECULES = [
        'LiH',
        'Li_GLYCINE', 
        'H2O'
    ]
    
    # Configuración de API
    API_RATE_LIMIT = 100  # requests por minuto
    API_TIMEOUT = 30  # segundos
    
    # Configuración de desarrollo
    DEVELOPMENT_MODE = os.environ.get('DEVELOPMENT_MODE', 'True').lower() == 'true'
    MOCK_SIMULATIONS = os.environ.get('MOCK_SIMULATIONS', 'False').lower() == 'true'

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    DEVELOPMENT_MODE = True
    MOCK_SIMULATIONS = True
    
    # Configuración de logging para desarrollo
    LOG_LEVEL = 'DEBUG'
    
    # Configuración de simulación para desarrollo
    MAX_SIMULATION_TIME = 60  # 1 minuto en desarrollo

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    DEVELOPMENT_MODE = False
    MOCK_SIMULATIONS = False
    
    # Configuración de logging para producción
    LOG_LEVEL = 'WARNING'
    
    # Configuración de simulación para producción
    MAX_SIMULATION_TIME = 600  # 10 minutos en producción

class TestingConfig(Config):
    """Configuración para testing"""
    DEBUG = True
    TESTING = True
    MOCK_SIMULATIONS = True
    
    # Configuración de simulación para testing
    MAX_SIMULATION_TIME = 10  # 10 segundos para tests

# ============================================================================
# 🧪 CONFIGURACIÓN DE SIMULACIÓN CUÁNTICA
# ============================================================================

class QuantumConfig:
    """Configuración específica para simulación cuántica"""
    
    # Parámetros de simulación
    DEFAULT_PARAMETERS = {
        'basis_set': 'sto3g',
        'optimizer': 'COBYLA',
        'max_iterations': 100,
        'convergence_threshold': 1e-6,
        'random_seed': 42
    }
    
    # Configuración de moléculas
    MOLECULE_CONFIGS = {
        'LiH': {
            'atoms': ['Li', 'H'],
            'bond_length': 1.6,
            'electrons': 4,
            'orbitals': 2,
            'complexity': 'simple'
        },
        'Li_GLYCINE': {
            'atoms': ['Li', 'C', 'N', 'O', 'H'],
            'bond_length': 2.1,
            'electrons': 32,
            'orbitals': 16,
            'complexity': 'complex'
        },
        'H2O': {
            'atoms': ['H', 'O', 'H'],
            'bond_length': 0.96,
            'electrons': 10,
            'orbitals': 5,
            'complexity': 'simple'
        }
    }
    
    # Configuración de conjuntos base
    BASIS_SETS = {
        'sto3g': {
            'description': 'STO-3G - Conjunto base mínimo',
            'complexity': 'low',
            'accuracy': 'medium'
        },
        '6-31g': {
            'description': '6-31G - Conjunto base split-valence',
            'complexity': 'medium',
            'accuracy': 'high'
        },
        'cc-pvdz': {
            'description': 'cc-pVDZ - Conjunto base correlacionado',
            'complexity': 'high',
            'accuracy': 'very_high'
        }
    }
    
    # Configuración de optimizadores
    OPTIMIZERS = {
        'COBYLA': {
            'description': 'Constrained Optimization BY Linear Approximation',
            'type': 'gradient_free',
            'convergence': 'fast'
        },
        'SPSA': {
            'description': 'Simultaneous Perturbation Stochastic Approximation',
            'type': 'stochastic',
            'convergence': 'medium'
        },
        'L_BFGS_B': {
            'description': 'Limited-memory BFGS with bounds',
            'type': 'gradient_based',
            'convergence': 'slow'
        }
    }

# ============================================================================
# 🌐 CONFIGURACIÓN DE API
# ============================================================================

class APIConfig:
    """Configuración de la API REST"""
    
    # Endpoints principales
    ENDPOINTS = {
        'simple_simulation': '/api/quantum/simple',
        'advanced_simulation': '/api/quantum/simulate',
        'mock_simulation': '/api/mock/quantum-simulate',
        'batch_simulation': '/api/quantum/start-simulation',
        'simulation_status': '/api/quantum/status',
        'analyze_interaction': '/api/analyze-interaction',
        'list_molecules': '/api/molecules',
        'molecule_info': '/api/molecules'
    }
    
    # Configuración de respuestas
    RESPONSE_FORMATS = {
        'success': {
            'status': 'success',
            'data': {},
            'message': '',
            'timestamp': ''
        },
        'error': {
            'status': 'error',
            'error': '',
            'message': '',
            'timestamp': ''
        }
    }
    
    # Configuración de WebSocket
    WEBSOCKET_EVENTS = {
        'connect': 'connect',
        'disconnect': 'disconnect',
        'start_simulation': 'start_quantum_simulation',
        'simulation_progress': 'simulation_progress',
        'simulation_complete': 'simulation_complete',
        'simulation_error': 'simulation_error'
    }

# ============================================================================
# 🎨 CONFIGURACIÓN DE UI
# ============================================================================

class UIConfig:
    """Configuración de la interfaz de usuario"""
    
    # Configuración de temas
    THEMES = {
        'default': {
            'primary_color': '#3498db',
            'secondary_color': '#2c3e50',
            'success_color': '#27ae60',
            'warning_color': '#f39c12',
            'danger_color': '#e74c3c'
        },
        'dark': {
            'primary_color': '#1abc9c',
            'secondary_color': '#34495e',
            'success_color': '#2ecc71',
            'warning_color': '#f39c12',
            'danger_color': '#e74c3c'
        }
    }
    
    # Configuración de animaciones
    ANIMATIONS = {
        'fade_in_duration': 0.5,
        'slide_duration': 0.3,
        'pulse_duration': 2.0,
        'bounce_duration': 1.0
    }
    
    # Configuración de responsive
    BREAKPOINTS = {
        'mobile': 480,
        'tablet': 768,
        'desktop': 1024,
        'large': 1200
    }

# ============================================================================
# 🔧 CONFIGURACIÓN DE DESARROLLO
# ============================================================================

class DevelopmentConfig:
    """Configuración específica para desarrollo"""
    
    # Configuración de hot reload
    HOT_RELOAD = True
    AUTO_RELOAD = True
    
    # Configuración de debugging
    DEBUG_TOOLBAR = True
    PROFILER = True
    
    # Configuración de testing
    TEST_DATABASE = 'test_quantum.db'
    TEST_SIMULATIONS = True
    
    # Configuración de logging
    VERBOSE_LOGGING = True
    CONSOLE_LOGGING = True

# ============================================================================
# 🚀 CONFIGURACIÓN DE DESPLIEGUE
# ============================================================================

class DeploymentConfig:
    """Configuración para despliegue"""
    
    # Configuración de servidor
    SERVER_CONFIG = {
        'host': '0.0.0.0',
        'port': 5000,
        'workers': 4,
        'timeout': 30
    }
    
    # Configuración de base de datos
    DATABASE_CONFIG = {
        'url': os.environ.get('DATABASE_URL', 'sqlite:///quantum_simulator.db'),
        'pool_size': 10,
        'max_overflow': 20
    }
    
    # Configuración de caché
    CACHE_CONFIG = {
        'type': 'redis',
        'url': os.environ.get('REDIS_URL', 'redis://localhost:6379'),
        'ttl': 3600
    }
    
    # Configuración de monitoreo
    MONITORING_CONFIG = {
        'enabled': True,
        'metrics_endpoint': '/metrics',
        'health_check': '/health'
    }

# ============================================================================
# 🎯 CONFIGURACIÓN POR ENTORNO
# ============================================================================

def get_config():
    """Obtiene la configuración según el entorno"""
    env = os.environ.get('FLASK_ENV', 'development')
    
    configs = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig
    }
    
    return configs.get(env, DevelopmentConfig)

def get_quantum_config():
    """Obtiene la configuración cuántica"""
    return QuantumConfig()

def get_api_config():
    """Obtiene la configuración de la API"""
    return APIConfig()

def get_ui_config():
    """Obtiene la configuración de la UI"""
    return UIConfig()

# ============================================================================
# 🔍 VALIDACIÓN DE CONFIGURACIÓN
# ============================================================================

def validate_config():
    """Valida la configuración actual"""
    config = get_config()
    errors = []
    
    # Validar configuración básica
    if not config.SECRET_KEY:
        errors.append("SECRET_KEY no configurada")
    
    if config.PORT < 1000 or config.PORT > 65535:
        errors.append(f"Puerto inválido: {config.PORT}")
    
    # Validar configuración cuántica
    quantum_config = get_quantum_config()
    for molecule in config.SUPPORTED_MOLECULES:
        if molecule not in quantum_config.MOLECULE_CONFIGS:
            errors.append(f"Configuración faltante para molécula: {molecule}")
    
    if errors:
        raise ValueError(f"Errores de configuración: {', '.join(errors)}")
    
    return True

# ============================================================================
# 🚀 INICIALIZACIÓN
# ============================================================================

if __name__ == "__main__":
    # Validar configuración
    try:
        validate_config()
        print("✅ Configuración válida")
    except ValueError as e:
        print(f"❌ Error de configuración: {e}")
        exit(1)
    
    # Mostrar configuración actual
    config = get_config()
    print(f"🔧 Entorno: {os.environ.get('FLASK_ENV', 'development')}")
    print(f"🌐 Host: {config.HOST}")
    print(f"📡 Puerto: {config.PORT}")
    print(f"🐛 Debug: {config.DEBUG}")
    print(f"🧪 Mock: {config.MOCK_SIMULATIONS}")
