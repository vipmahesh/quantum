# 🤝 Guía de Contribución

¡Gracias por tu interés en contribuir al Simulador Cuántico! Esta guía te ayudará a empezar.

## 📋 Tabla de Contenidos

- [Código de Conducta](#código-de-conducta)
- [¿Cómo Puedo Contribuir?](#cómo-puedo-contribuir)
- [Configuración del Entorno](#configuración-del-entorno)
- [Proceso de Desarrollo](#proceso-de-desarrollo)
- [Estándares de Código](#estándares-de-código)
- [Proceso de Pull Request](#proceso-de-pull-request)

## 📜 Código de Conducta

Este proyecto sigue un código de conducta. Al participar, se espera que mantengas un ambiente respetuoso y profesional.

## 🎯 ¿Cómo Puedo Contribuir?

### Reportar Bugs

Si encuentras un bug:

1. **Verifica** que no haya sido reportado previamente en [Issues](https://github.com/picapiedra123/quantum/issues)
2. **Crea un nuevo issue** con una descripción clara:
   - Título descriptivo
   - Pasos para reproducir
   - Comportamiento esperado vs actual
   - Versión de Python y sistema operativo
   - Logs o capturas de pantalla si es posible

### Sugerir Mejoras

Para sugerir nuevas características:

1. **Abre un issue** con la etiqueta "enhancement"
2. **Describe** claramente:
   - El problema que resuelve
   - Cómo lo implementarías
   - Ejemplos de uso
   - Beneficios para los usuarios

### Contribuir con Código

1. **Fork** el repositorio
2. **Crea una rama** para tu feature: `git checkout -b feature/mi-nueva-caracteristica`
3. **Desarrolla** siguiendo los estándares de código
4. **Prueba** tus cambios
5. **Commit** con mensajes descriptivos
6. **Push** a tu fork
7. **Abre un Pull Request**

## 🛠️ Configuración del Entorno

### Requisitos

- Python 3.8 o superior
- Git
- Cuenta en IBM Quantum (para features de IBM Quantum)

### Instalación

```bash
# Clonar tu fork
git clone https://github.com/TU_USUARIO/quantum.git
cd quantum

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales
```

### Configurar Remote Upstream

```bash
git remote add upstream https://github.com/picapiedra123/quantum.git
git fetch upstream
```

## 💻 Proceso de Desarrollo

### 1. Sincronizar con Upstream

Antes de empezar a trabajar:

```bash
git checkout main
git pull upstream main
git push origin main
```

### 2. Crear Rama de Feature

```bash
git checkout -b feature/nombre-descriptivo
```

Convenciones de nombres de ramas:
- `feature/` - Nuevas características
- `bugfix/` - Corrección de bugs
- `hotfix/` - Correcciones urgentes
- `docs/` - Documentación
- `refactor/` - Refactorización de código

### 3. Desarrollo

- Escribe código claro y bien documentado
- Agrega comentarios donde sea necesario
- Sigue los estándares de código (ver abajo)
- Escribe pruebas para nuevas funcionalidades

### 4. Testing

```bash
# Ejecutar tests
python test_simulator.py

# Verificar linting (opcional)
flake8 .
black --check .
```

### 5. Commit

Usa mensajes de commit descriptivos siguiendo [Conventional Commits](https://www.conventionalcommits.org/):

```bash
git commit -m "feat: agregar soporte para molécula CO2"
git commit -m "fix: corregir cálculo de energía en LiH"
git commit -m "docs: actualizar README con nuevos ejemplos"
```

Tipos de commit:
- `feat`: Nueva característica
- `fix`: Corrección de bug
- `docs`: Documentación
- `style`: Formato (no afecta el código)
- `refactor`: Refactorización
- `test`: Agregar o modificar tests
- `chore`: Tareas de mantenimiento

## 📝 Estándares de Código

### Python

- **PEP 8**: Sigue las convenciones de estilo de Python
- **Type Hints**: Usa type hints cuando sea posible
- **Docstrings**: Documenta funciones y clases

```python
def simulate_molecule(molecule: str, parameters: Dict = None) -> Dict:
    """
    Simula una molécula usando computación cuántica.
    
    Args:
        molecule: Nombre de la molécula (ej: 'LiH', 'H2O')
        parameters: Parámetros opcionales de simulación
        
    Returns:
        Dict con resultados de la simulación
        
    Raises:
        ValueError: Si la molécula no es soportada
    """
    pass
```

### JavaScript

- **ES6+**: Usa características modernas de JavaScript
- **Const/Let**: Evita `var`
- **Arrow Functions**: Usa funciones flecha cuando sea apropiado

### HTML/CSS

- **Semántico**: Usa HTML semántico
- **Responsive**: Asegura diseño responsive
- **Accesibilidad**: Incluye atributos ARIA cuando sea necesario

## 🔄 Proceso de Pull Request

### Antes de Crear el PR

- [ ] Código está actualizado con `main`
- [ ] Todos los tests pasan
- [ ] Código sigue los estándares
- [ ] Documentación actualizada
- [ ] Sin credenciales hardcodeadas
- [ ] Commits tienen mensajes descriptivos

### Crear el Pull Request

1. **Push** tu rama al fork:
   ```bash
   git push origin feature/mi-feature
   ```

2. **Abre un PR** en GitHub desde tu fork

3. **Completa la plantilla del PR**:
   - Descripción clara de los cambios
   - Referencias a issues relacionados
   - Capturas de pantalla si es relevante
   - Checklist de verificación

### Durante la Revisión

- **Responde** a los comentarios de manera constructiva
- **Realiza** los cambios solicitados
- **Mantén** el PR actualizado con `main`

### Después del Merge

```bash
git checkout main
git pull upstream main
git push origin main
git branch -d feature/mi-feature
```

## 🧪 Testing

### Ejecutar Tests

```bash
python test_simulator.py
```

### Agregar Tests

Agrega tests para nuevas funcionalidades en `test_simulator.py`:

```python
def test_nueva_funcionalidad():
    """Test para nueva funcionalidad"""
    resultado = nueva_funcionalidad()
    assert resultado == esperado
```

## 📚 Documentación

### Actualizar README

Si tu cambio afecta el uso del simulador, actualiza:
- Sección de características
- Ejemplos de uso
- Instrucciones de instalación

### Agregar Ejemplos

Agrega ejemplos en la carpeta de documentación o en el README.

## 🔒 Seguridad

### Reportar Vulnerabilidades

Si encuentras una vulnerabilidad de seguridad:

1. **NO** la publiques en un issue público
2. Contacta al mantenedor directamente
3. Proporciona detalles completos
4. Espera respuesta antes de divulgar

### Manejo de Credenciales

- **NUNCA** incluyas credenciales en el código
- Usa variables de entorno
- Verifica con `git grep` antes de commit
- Lee `SECURITY.md` para más información

## ❓ Preguntas

Si tienes preguntas sobre cómo contribuir:

- Abre un issue con la etiqueta "question"
- Revisa issues existentes
- Contacta a los mantenedores

## 🎉 Reconocimiento

Los contribuidores serán reconocidos en:
- Sección de contribuidores en el README
- Release notes cuando sea aplicable
- Agradecimientos especiales para contribuciones significativas

## 📖 Recursos

- [Documentación de Qiskit](https://qiskit.org/documentation/)
- [IBM Quantum Experience](https://quantum-computing.ibm.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Git Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows)

---

**¡Gracias por contribuir al Simulador Cuántico! 🚀⚛️**

