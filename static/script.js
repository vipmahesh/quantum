/**
 * 🧪 Simulador Cuántico - JavaScript Principal
 * Maneja todas las interacciones del frontend
 */

// Variables globales
let currentSimulationId = null;
let socket = null;
let isConnected = false;

// ============================================================================
// 🎯 PATRÓN 1: API REST SIMPLE
// ============================================================================

async function runSimpleSimulation() {
    const molecule = document.getElementById('moleculeSelect')?.value || 'LiH';
    const basisSet = document.getElementById('basisSet')?.value || 'sto3g';
    const optimizer = document.getElementById('optimizer')?.value || 'COBYLA';
    
    showLoading(true);
    hideProgress();
    
    try {
        const response = await fetch('http://localhost:5000/api/quantum/simple', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                molecule: molecule,
                parameters: {
                    basis_set: basisSet,
                    optimizer: optimizer
                }
            })
        });
        
        const result = await response.json();
        
        if (result.status === 'success') {
            showResult(`
                <div class="energy-display">⚡ Energía: ${result.data.energy} Ha</div>
                <div class="status-indicator status-success">${result.data.interaction_strength}</div>
                <p><strong>Molécula:</strong> ${result.data.molecule}</p>
                <p><strong>Tiempo de cómputo:</strong> ${result.data.computation_time}</p>
                <p><strong>Mensaje:</strong> ${result.data.message}</p>
                <div class="status-indicator status-success">Simulación Simple Completada</div>
            `);
        } else {
            showError(`Error: ${result.error}`);
        }
        
    } catch (error) {
        showError(`Error de conexión: ${error.message}`);
    } finally {
        showLoading(false);
    }
}

// ============================================================================
// ⚡ SIMULACIÓN AVANZADA (REST Completo)
// ============================================================================

async function runAdvancedSimulation() {
    const molecule = document.getElementById('moleculeSelect')?.value || 'LiH';
    const basisSet = document.getElementById('basisSet')?.value || 'sto3g';
    const optimizer = document.getElementById('optimizer')?.value || 'COBYLA';
    
    showLoading(true);
    hideProgress();
    
    try {
        const response = await fetch('http://localhost:5000/api/quantum/simulate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                molecule: molecule,
                parameters: {
                    basis_set: basisSet,
                    optimizer: optimizer
                }
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showResult(`
                <div class="energy-display">⚡ Energía: ${result.energy} Ha</div>
                <div class="status-indicator status-success">${result.interaction_strength}</div>
                <p><strong>Molécula:</strong> ${result.molecule}</p>
                <p><strong>Tiempo de cómputo:</strong> ${result.computation_time.toFixed(2)} segundos</p>
                <p><strong>Estado:</strong> ${result.status}</p>
                <p><strong>Mensaje:</strong> ${result.message}</p>
                <div class="status-indicator status-success">Simulación Avanzada Completada</div>
            `);
        } else {
            showError(`Error: ${result.error}`);
        }
        
    } catch (error) {
        showError(`Error de conexión: ${error.message}`);
    } finally {
        showLoading(false);
    }
}

// ============================================================================
// 🧪 SIMULACIÓN MOCK
// ============================================================================

async function runMockSimulation() {
    const molecule = document.getElementById('moleculeSelect')?.value || 'LiH';
    
    showLoading(true);
    hideProgress();
    
    try {
        const response = await fetch('http://localhost:5000/api/mock/quantum-simulate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                molecule: molecule
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showResult(`
                <div class="energy-display">🧪 Energía Mock: ${result.energy.toFixed(4)} Ha</div>
                <div class="status-indicator status-info">${result.interaction_strength}</div>
                <p><strong>Molécula:</strong> ${result.molecule}</p>
                <p><strong>Tiempo de cómputo:</strong> ${result.computation_time}</p>
                <p><strong>Mensaje:</strong> ${result.message}</p>
                <div class="status-indicator status-info">Simulación Mock - Para desarrollo</div>
            `);
        } else {
            showError(`Error: ${result.error}`);
        }
        
    } catch (error) {
        showError(`Error de conexión: ${error.message}`);
    } finally {
        showLoading(false);
    }
}

// ============================================================================
// 🔌 WEBSOCKET (Tiempo Real)
// ============================================================================

function startWebSocketSimulation() {
    const molecule = document.getElementById('moleculeSelect')?.value || 'LiH';
    const basisSet = document.getElementById('basisSet')?.value || 'sto3g';
    const optimizer = document.getElementById('optimizer')?.value || 'COBYLA';
    
    // Conectar WebSocket si no está conectado
    if (!socket || !isConnected) {
        connectWebSocket();
    }
    
    // Iniciar simulación
    showProgress(0);
    showResult('<p>🔄 Iniciando simulación WebSocket...</p>');
    
    socket.emit('start_quantum_simulation', {
        molecule: molecule,
        parameters: {
            basis_set: basisSet,
            optimizer: optimizer
        }
    });
}

function connectWebSocket() {
    if (typeof io === 'undefined') {
        showError('WebSocket no disponible. Asegúrate de que Socket.IO esté cargado.');
        return;
    }
    
    socket = io('http://localhost:5000');
    
    socket.on('connect', () => {
        isConnected = true;
        console.log('🔌 Conectado al servidor WebSocket');
    });
    
    socket.on('connected', (data) => {
        console.log('Conectado:', data.message);
    });
    
    socket.on('simulation_progress', (data) => {
        showProgress(data.progress);
        showResult(`<p>🔄 ${data.message}</p>`);
        console.log('Progreso:', data.message);
    });
    
    socket.on('simulation_complete', (data) => {
        showResult(`
            <div class="energy-display">⚡ Energía: ${data.energy} Ha</div>
            <div class="status-indicator status-success">${data.interaction_strength}</div>
            <p><strong>Molécula:</strong> ${data.molecule}</p>
            <p><strong>Tiempo de cómputo:</strong> ${data.computation_time.toFixed(2)} segundos</p>
            <div class="status-indicator status-success">Simulación WebSocket completada</div>
        `);
        hideProgress();
    });
    
    socket.on('simulation_error', (data) => {
        showError(`Error WebSocket: ${data.error}`);
        hideProgress();
    });
    
    socket.on('disconnect', () => {
        isConnected = false;
        console.log('🔌 Desconectado del servidor WebSocket');
    });
}

// ============================================================================
// 🚀 SIMULACIÓN POR LOTE
// ============================================================================

async function startBatchSimulation() {
    const molecule = document.getElementById('moleculeSelect')?.value || 'LiH';
    const basisSet = document.getElementById('basisSet')?.value || 'sto3g';
    const optimizer = document.getElementById('optimizer')?.value || 'COBYLA';
    
    showLoading(true);
    
    try {
        const response = await fetch('http://localhost:5000/api/quantum/start-simulation', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                molecule: molecule,
                parameters: {
                    basis_set: basisSet,
                    optimizer: optimizer
                }
            })
        });
        
        const result = await response.json();
        currentSimulationId = result.simulation_id;
        
        showResult(`
            <div class="status-indicator status-info">Simulación iniciada</div>
            <p><strong>ID:</strong> ${result.simulation_id}</p>
            <p><strong>Molécula:</strong> ${result.molecule}</p>
            <p><strong>Estado:</strong> ${result.status}</p>
            <p><strong>Mensaje:</strong> ${result.message}</p>
            <p>🔄 Verificando estado cada 2 segundos...</p>
        `);
        
        // Verificar estado cada 2 segundos
        checkSimulationStatus();
        
    } catch (error) {
        showError(`Error: ${error.message}`);
        showLoading(false);
    }
}

async function checkSimulationStatus() {
    if (!currentSimulationId) return;
    
    try {
        const response = await fetch(`http://localhost:5000/api/quantum/status/${currentSimulationId}`);
        const status = await response.json();
        
        if (status.status === 'completed') {
            showResult(`
                <div class="energy-display">⚡ Energía: ${status.result.energy} Ha</div>
                <div class="status-indicator status-success">${status.result.interaction_strength}</div>
                <p><strong>Molécula:</strong> ${status.molecule}</p>
                <p><strong>Tiempo de cómputo:</strong> ${status.result.computation_time.toFixed(2)} segundos</p>
                <div class="status-indicator status-success">Simulación por lote completada</div>
            `);
            currentSimulationId = null;
            showLoading(false);
        } else if (status.status === 'error') {
            showError(`Error en simulación: ${status.error}`);
            currentSimulationId = null;
            showLoading(false);
        } else {
            // Seguir verificando
            setTimeout(checkSimulationStatus, 2000);
        }
        
    } catch (error) {
        showError(`Error verificando estado: ${error.message}`);
        currentSimulationId = null;
        showLoading(false);
    }
}

// ============================================================================
// 🔬 ANÁLISIS DE INTERACCIÓN
// ============================================================================

async function analyzeInteraction(molecule1, molecule2) {
    try {
        const response = await fetch('http://localhost:5000/api/analyze-interaction', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                molecule1: molecule1,
                molecule2: molecule2
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            const interaction = result.interaction;
            return `
                <div class="energy-display">🔬 ${interaction.interaction_energy} Ha</div>
                <div class="status-indicator status-info">${interaction.interaction_type}</div>
                <p><strong>Molécula 1:</strong> ${interaction.molecule1}</p>
                <p><strong>Molécula 2:</strong> ${interaction.molecule2}</p>
                <p><strong>Energía de Interacción:</strong> ${interaction.interaction_energy} Ha</p>
                <p><strong>Tipo de Interacción:</strong> ${interaction.interaction_type}</p>
                <p><strong>Estabilidad:</strong> ${interaction.stability}</p>
            `;
        } else {
            return `<div class="status-indicator status-error">Error: ${result.error}</div>`;
        }
        
    } catch (error) {
        return `<div class="status-indicator status-error">Error: ${error.message}</div>`;
    }
}

// ============================================================================
// 📚 INFORMACIÓN DE MOLÉCULAS
// ============================================================================

async function getMoleculeInfo(molecule) {
    try {
        const response = await fetch(`http://localhost:5000/api/molecules/${molecule}`);
        const result = await response.json();
        
        if (result.success) {
            const info = result.info;
            return `
                <div class="molecule-info">
                    <h4>📚 ${molecule}</h4>
                    <ul>
                        <li><strong>Átomos:</strong> ${info.atoms.join(', ')}</li>
                        <li><strong>Longitud de enlace:</strong> ${info.bond_length} Å</li>
                        <li><strong>Electrones:</strong> ${info.electrons}</li>
                        <li><strong>Orbitales:</strong> ${info.orbitals}</li>
                    </ul>
                </div>
            `;
        } else {
            return `<div class="status-indicator status-error">Error: ${result.error}</div>`;
        }
        
    } catch (error) {
        return `<div class="status-indicator status-error">Error: ${error.message}</div>`;
    }
}

async function listAvailableMolecules() {
    try {
        const response = await fetch('http://localhost:5000/api/molecules');
        const result = await response.json();
        
        if (result.molecules) {
            return `
                <div class="molecule-info">
                    <h4>📚 Moléculas Disponibles (${result.count})</h4>
                    <ul>
                        ${result.molecules.map(mol => `<li><strong>${mol}</strong></li>`).join('')}
                    </ul>
                </div>
            `;
        } else {
            return `<div class="status-indicator status-error">Error obteniendo moléculas</div>`;
        }
        
    } catch (error) {
        return `<div class="status-indicator status-error">Error: ${error.message}</div>`;
    }
}

// ============================================================================
// 🎨 FUNCIONES DE UI
// ============================================================================

function showLoading(show) {
    const loading = document.getElementById('loading');
    if (loading) {
        loading.style.display = show ? 'block' : 'none';
    }
}

function showProgress(progress) {
    const progressBar = document.getElementById('progressBar') || document.getElementById('wsProgress');
    const progressFill = document.getElementById('progressFill') || document.getElementById('wsProgressFill');
    
    if (progressBar && progressFill) {
        progressBar.style.display = 'block';
        progressFill.style.width = progress + '%';
    }
}

function hideProgress() {
    const progressBar = document.getElementById('progressBar') || document.getElementById('wsProgress');
    if (progressBar) {
        progressBar.style.display = 'none';
    }
}

function showResult(html) {
    const result = document.getElementById('result');
    if (result) {
        result.innerHTML = html;
        result.classList.add('show');
    }
}

function showError(message) {
    const result = document.getElementById('result');
    if (result) {
        result.innerHTML = `
            <div class="status-indicator status-error">Error</div>
            <p>${message}</p>
        `;
        result.classList.add('show');
    }
}

// ============================================================================
// 🎮 FUNCIONES DE DEMO
// ============================================================================

async function demoSimpleAPI() {
    const molecule = document.getElementById('simpleMolecule')?.value || 'LiH';
    const result = document.getElementById('simpleResult');
    
    if (result) {
        result.innerHTML = '<p>🔄 Ejecutando simulación simple...</p>';
        
        try {
            const response = await fetch('http://localhost:5000/api/quantum/simple', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ molecule: molecule })
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                result.innerHTML = `
                    <div class="energy-display">⚡ ${data.data.energy} Ha</div>
                    <div class="status-indicator status-success">${data.data.interaction_strength}</div>
                    <p><strong>Molécula:</strong> ${data.data.molecule}</p>
                    <p><strong>Tiempo:</strong> ${data.data.computation_time}</p>
                    <p><strong>Mensaje:</strong> ${data.data.message}</p>
                `;
            } else {
                result.innerHTML = `<div class="status-indicator status-error">Error: ${data.error}</div>`;
            }
            
        } catch (error) {
            result.innerHTML = `<div class="status-indicator status-error">Error: ${error.message}</div>`;
        }
    }
}

async function demoWebSocket() {
    const molecule = document.getElementById('wsMolecule')?.value || 'LiH';
    const result = document.getElementById('wsResult');
    const progressBar = document.getElementById('wsProgress');
    const progressFill = document.getElementById('wsProgressFill');
    
    if (result) {
        // Conectar WebSocket si no está conectado
        if (!socket || !isConnected) {
            connectWebSocket();
        }
        
        // Iniciar simulación
        result.innerHTML = '<p>🔄 Iniciando simulación WebSocket...</p>';
        if (progressBar) progressBar.style.display = 'block';
        if (progressFill) progressFill.style.width = '0%';
        
        socket.emit('start_quantum_simulation', {
            molecule: molecule,
            parameters: {}
        });
    }
}

async function demoMockAPI() {
    const molecule = document.getElementById('mockMolecule')?.value || 'LiH';
    const result = document.getElementById('mockResult');
    
    if (result) {
        result.innerHTML = '<p>🔄 Ejecutando simulación mock...</p>';
        
        try {
            const response = await fetch('http://localhost:5000/api/mock/quantum-simulate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ molecule: molecule })
            });
            
            const data = await response.json();
            
            if (data.success) {
                result.innerHTML = `
                    <div class="energy-display">🧪 ${data.energy.toFixed(4)} Ha</div>
                    <div class="status-indicator status-info">${data.interaction_strength}</div>
                    <p><strong>Molécula:</strong> ${data.molecule}</p>
                    <p><strong>Tiempo:</strong> ${data.computation_time}</p>
                    <p><strong>Mensaje:</strong> ${data.message}</p>
                    <div class="status-indicator status-info">Simulación Mock</div>
                `;
            } else {
                result.innerHTML = `<div class="status-indicator status-error">Error: ${data.error}</div>`;
            }
            
        } catch (error) {
            result.innerHTML = `<div class="status-indicator status-error">Error: ${error.message}</div>`;
        }
    }
}

async function demoComparison() {
    const molecule = document.getElementById('compareMolecule')?.value || 'LiH';
    const result = document.getElementById('compareResult');
    
    if (result) {
        result.innerHTML = '<p>🔄 Comparando APIs...</p>';
        
        const apis = [
            { name: 'REST Simple', url: '/api/quantum/simple' },
            { name: 'REST Completo', url: '/api/quantum/simulate' },
            { name: 'Mock API', url: '/api/mock/quantum-simulate' }
        ];
        
        const results = [];
        
        for (const api of apis) {
            try {
                const startTime = Date.now();
                const response = await fetch(`http://localhost:5000${api.url}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ molecule: molecule })
                });
                const endTime = Date.now();
                const data = await response.json();
                
                results.push({
                    name: api.name,
                    success: true,
                    time: endTime - startTime,
                    data: data
                });
            } catch (error) {
                results.push({
                    name: api.name,
                    success: false,
                    error: error.message
                });
            }
        }
        
        // Mostrar resultados en tabla
        let tableHTML = '<table class="comparison-table"><tr><th>API</th><th>Estado</th><th>Tiempo</th><th>Energía</th></tr>';
        
        results.forEach(result => {
            if (result.success) {
                const energy = result.data.data?.energy || result.data.energy || result.data.data?.energy || 'N/A';
                tableHTML += `
                    <tr>
                        <td>${result.name}</td>
                        <td><span class="status-indicator status-success">✓</span></td>
                        <td>${result.time}ms</td>
                        <td>${energy}</td>
                    </tr>
                `;
            } else {
                tableHTML += `
                    <tr>
                        <td>${result.name}</td>
                        <td><span class="status-indicator status-error">✗</span></td>
                        <td>N/A</td>
                        <td>Error</td>
                    </tr>
                `;
            }
        });
        
        tableHTML += '</table>';
        result.innerHTML = tableHTML;
    }
}

async function demoInteraction() {
    const mol1 = document.getElementById('mol1')?.value || 'LiH';
    const mol2 = document.getElementById('mol2')?.value || 'H2O';
    const result = document.getElementById('interactionResult');
    
    if (result) {
        result.innerHTML = '<p>🔄 Analizando interacción molecular...</p>';
        
        const interactionHTML = await analyzeInteraction(mol1, mol2);
        result.innerHTML = interactionHTML;
    }
}

async function demoMoleculeInfo() {
    const result = document.getElementById('infoResult');
    
    if (result) {
        result.innerHTML = '<p>🔄 Obteniendo información de moléculas...</p>';
        
        const infoHTML = await listAvailableMolecules();
        result.innerHTML = infoHTML;
    }
}

// ============================================================================
// 🚀 INICIALIZACIÓN
// ============================================================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('🧪 Simulador Cuántico cargado');
    console.log('📡 APIs disponibles:');
    console.log('  - REST Simple: /api/quantum/simple');
    console.log('  - REST Completo: /api/quantum/simulate');
    console.log('  - Mock: /api/mock/quantum-simulate');
    console.log('  - WebSocket: ws://localhost:5000');
    console.log('  - Análisis: /api/analyze-interaction');
    console.log('  - Moléculas: /api/molecules');
    
    // Verificar si estamos en la página de demo
    if (window.location.pathname.includes('demo')) {
        console.log('🎮 Modo Demo activado');
    }
});

// ============================================================================
// 🔧 UTILIDADES
// ============================================================================

function formatNumber(num, decimals = 4) {
    return parseFloat(num).toFixed(decimals);
}

function formatTime(seconds) {
    if (seconds < 1) {
        return `${(seconds * 1000).toFixed(0)}ms`;
    } else {
        return `${seconds.toFixed(2)}s`;
    }
}

function getStatusColor(status) {
    const colors = {
        'success': 'status-success',
        'error': 'status-error',
        'info': 'status-info',
        'warning': 'status-warning'
    };
    return colors[status] || 'status-info';
}

// Exportar funciones para uso global
window.runSimpleSimulation = runSimpleSimulation;
window.runAdvancedSimulation = runAdvancedSimulation;
window.runMockSimulation = runMockSimulation;
window.startWebSocketSimulation = startWebSocketSimulation;
window.startBatchSimulation = startBatchSimulation;
window.demoSimpleAPI = demoSimpleAPI;
window.demoWebSocket = demoWebSocket;
window.demoMockAPI = demoMockAPI;
window.demoComparison = demoComparison;
window.demoInteraction = demoInteraction;
window.demoMoleculeInfo = demoMoleculeInfo;
