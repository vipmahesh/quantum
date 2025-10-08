# 🔒 Guía de Seguridad - Simulador Cuántico

## ⚠️ Información Importante

Este documento describe las mejores prácticas de seguridad para el Simulador Cuántico.

## 🔑 Gestión de Credenciales

### API Keys y Tokens

**NUNCA** incluyas credenciales directamente en el código fuente:

❌ **INCORRECTO:**
```python
API_KEY = 'Q8MuqQmCnwTc5NaN...'  # ¡NO HAGAS ESTO!
```

✅ **CORRECTO:**
```python
import os
API_KEY = os.getenv('IBM_QUANTUM_TOKEN')  # Usa variables de entorno
```

### Configuración de Variables de Entorno

#### Linux/Mac
```bash
export IBM_QUANTUM_TOKEN=tu_api_key_aqui
export SECRET_KEY=tu_clave_secreta_aleatoria
```

#### Windows PowerShell
```powershell
$env:IBM_QUANTUM_TOKEN="tu_api_key_aqui"
$env:SECRET_KEY="tu_clave_secreta_aleatoria"
```

#### Archivo .env (para desarrollo local)
Crea un archivo `.env` en la raíz del proyecto:
```
IBM_QUANTUM_TOKEN=tu_api_key_aqui
SECRET_KEY=tu_clave_secreta_aleatoria
FLASK_ENV=development
```

**IMPORTANTE**: El archivo `.env` está en `.gitignore` y NO debe ser subido al repositorio.

## 🛡️ Obtención de API Keys

### IBM Quantum
1. Visita https://quantum-computing.ibm.com/
2. Crea una cuenta o inicia sesión
3. Ve a tu perfil → API Token
4. Copia tu token
5. Configúralo como variable de entorno (NO lo pegues en el código)

## 📋 Checklist de Seguridad

Antes de publicar tu proyecto:

- [ ] Verificar que no hay API keys en el código
- [ ] Verificar que no hay contraseñas hardcodeadas
- [ ] Verificar que `.env` está en `.gitignore`
- [ ] Verificar que no hay archivos de credenciales en Git
- [ ] Revisar el historial de Git por credenciales accidentales
- [ ] Cambiar todas las claves secretas por defecto
- [ ] Usar HTTPS en producción
- [ ] Configurar CORS correctamente
- [ ] Habilitar rate limiting
- [ ] Configurar logging seguro (sin exponer credenciales)

## 🔄 Rotación de Credenciales

Si accidentalmente expones una API key:

1. **Revoca inmediatamente** la API key comprometida en IBM Quantum
2. **Genera una nueva** API key
3. **Actualiza** las variables de entorno en todos los ambientes
4. **Limpia el historial de Git** si la clave fue commiteada:
   ```bash
   # CUIDADO: Esto reescribe la historia
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch archivo_con_credenciales.py" \
     --prune-empty --tag-name-filter cat -- --all
   ```
5. **Notifica** a tu equipo sobre el incidente

## 🏭 Producción

### Servicios de Gestión de Secretos

Para entornos de producción, considera usar:

- **AWS Secrets Manager**: Para aplicaciones en AWS
- **Azure Key Vault**: Para aplicaciones en Azure
- **Google Secret Manager**: Para aplicaciones en GCP
- **HashiCorp Vault**: Para cualquier infraestructura
- **Heroku Config Vars**: Para despliegues en Heroku

### Ejemplo con AWS Secrets Manager
```python
import boto3
from botocore.exceptions import ClientError

def get_secret(secret_name):
    client = boto3.client('secretsmanager', region_name='us-east-1')
    try:
        response = client.get_secret_value(SecretId=secret_name)
        return response['SecretString']
    except ClientError as e:
        raise e

# Uso
API_KEY = get_secret('ibm_quantum_token')
```

## 🚨 Reportar Vulnerabilidades

Si encuentras una vulnerabilidad de seguridad:

1. **NO** la publiques en issues públicos
2. Contacta al equipo de desarrollo directamente
3. Proporciona detalles sobre la vulnerabilidad
4. Espera una respuesta antes de divulgar públicamente

## 📚 Recursos Adicionales

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [IBM Quantum Security Best Practices](https://quantum-computing.ibm.com/)
- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)
- [Git Guardian](https://www.gitguardian.com/)

## 🔍 Herramientas de Escaneo

### Detectar secretos en el código
```bash
# Instalar git-secrets
git clone https://github.com/awslabs/git-secrets.git
cd git-secrets
make install

# Configurar
git secrets --register-aws
git secrets --scan
```

### TruffleHog
```bash
pip install truffleHog
truffleHog --regex --entropy=True .
```

---

**Recuerda: La seguridad es responsabilidad de todos. Mantén tus credenciales seguras. 🔐**

