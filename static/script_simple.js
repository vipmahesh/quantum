/**
 * Simulador Cuantico - JavaScript Simplificado
 * Version que funciona sin WebSocket
 */

// Variables globales
let currentSimulationId = null;

// ============================================================================
// API REST SIMPLE
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
                <div class="energy-display">Energia: ${result.data.energy} Ha</div>
                <div class="status-indicator status-success">${result.data.interaction_strength}</div>
                <p><strong>Molecula:</strong> ${result.data.molecule}</p>
                <p><strong>Tiempo de computo:</strong> ${result.data.computation_time}</p>
                <p><strong>Mensaje:</strong> ${result.data.message}</p>
                <div class="status-indicator status-success">Simulacion Simple Completada</div>
            `);
        } else {
            showError(`Error: ${result.error}`);
        }
        
    } catch (error) {
        showError(`Error de conexion: ${error.message}`);
    } finally {
        showLoading(false);
    }
}

// ============================================================================
// SIMULACION AVANZADA
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
                <div class="energy-display">Energia: ${result.energy} Ha</div>
                <div class="status-indicator status-success">${result.interaction_strength}</div>
                <p><strong>Molecula:</strong> ${result.molecule}</p>
                <p><strong>Tiempo de computo:</strong> ${result.computation_time.toFixed(2)} segundos</p>
                <p><strong>Estado:</strong> ${result.status}</p>
                <p><strong>Mensaje:</strong> ${result.message}</p>
                <div class="status-indicator status-success">Simulacion Avanzada Completada</div>
            `);
        } else {
            showError(`Error: ${result.error}`);
        }
        
    } catch (error) {
        showError(`Error de conexion: ${error.message}`);
    } finally {
        showLoading(false);
    }
}

// ============================================================================
// SIMULACION MOCK
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
                <div class="energy-display">Energia Mock: ${result.energy.toFixed(4)} Ha</div>
                <div class="status-indicator status-info">${result.interaction_strength}</div>
                <p><strong>Molecula:</strong> ${result.molecule}</p>
                <p><strong>Tiempo de computo:</strong> ${result.computation_time}</p>
                <p><strong>Mensaje:</strong> ${result.message}</p>
                <div class="status-indicator status-info">Simulacion Mock - Para desarrollo</div>
            `);
        } else {
            showError(`Error: ${result.error}`);
        }
        
    } catch (error) {
        showError(`Error de conexion: ${error.message}`);
    } finally {
        showLoading(false);
    }
}

// ============================================================================
// WEBSOCKET SIMULADO (POLLING)
// ============================================================================

function startWebSocketSimulation() {
    const molecule = document.getElementById('moleculeSelect')?.value || 'LiH';
    const basisSet = document.getElementById('basisSet')?.value || 'sto3g';
    const optimizer = document.getElementById('optimizer')?.value || 'COBYLA';
    
    // Simular WebSocket con polling
    showProgress(0);
    showResult('<p>Iniciando simulacion WebSocket simulada...</p>');
    
    // Iniciar simulacion
    fetch('http://localhost:5000/api/websocket/simulate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            molecule: molecule,
            parameters: {
                basis_set: basisSet,
                optimizer: optimizer
            }
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'started') {
            // Polling para obtener progreso
            pollProgress(data.simulation_id);
        }
    })
    .catch(error => {
        showError(`Error WebSocket: ${error.message}`);
        hideProgress();
    });
}

function pollProgress(simulationId) {
    const pollInterval = setInterval(async () => {
        try {
            const response = await fetch(`http://localhost:5000/api/websocket/progress/${simulationId}`);
            const data = await response.json();
            
            if (data.progress && data.progress.progress !== undefined) {
                showProgress(data.progress.progress);
                showResult(`<p>Progreso: ${data.progress.message}</p>`);
            }
            
            if (data.result && data.result.status === 'completed') {
                clearInterval(pollInterval);
                const result = data.result.result;
                showResult(`
                    <div class="energy-display">Energia: ${result.energy} Ha</div>
                    <div class="status-indicator status-success">${result.interaction_strength}</div>
                    <p><strong>Molecula:</strong> ${result.molecule}</p>
                    <p><strong>Tiempo de computo:</strong> ${result.computation_time.toFixed(2)} segundos</p>
                    <div class="status-indicator status-success">Simulacion WebSocket completada</div>
                `);
                hideProgress();
            } else if (data.result && data.result.status === 'error') {
                clearInterval(pollInterval);
                showError(`Error WebSocket: ${data.result.error}`);
                hideProgress();
            }
        } catch (error) {
            clearInterval(pollInterval);
            showError(`Error verificando progreso: ${error.message}`);
            hideProgress();
        }
    }, 500); // Poll cada 500ms
}

// ============================================================================
// SIMULACION POR LOTE
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
            <div class="status-indicator status-info">Simulacion iniciada</div>
            <p><strong>ID:</strong> ${result.simulation_id}</p>
            <p><strong>Molecula:</strong> ${result.molecule}</p>
            <p><strong>Estado:</strong> ${result.status}</p>
            <p><strong>Mensaje:</strong> ${result.message}</p>
            <p>Verificando estado cada 2 segundos...</p>
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
                <div class="energy-display">Energia: ${status.result.energy} Ha</div>
                <div class="status-indicator status-success">${status.result.interaction_strength}</div>
                <p><strong>Molecula:</strong> ${status.molecule}</p>
                <p><strong>Tiempo de computo:</strong> ${status.result.computation_time.toFixed(2)} segundos</p>
                <div class="status-indicator status-success">Simulacion por lote completada</div>
            `);
            currentSimulationId = null;
            showLoading(false);
        } else if (status.status === 'error') {
            showError(`Error en simulacion: ${status.error}`);
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
// FUNCIONES DE UI
// ============================================================================

function showLoading(show) {
    const loading = document.getElementById('loading');
    if (loading) {
        loading.style.display = show ? 'block' : 'none';
    }
}

function showProgress(progress) {
    const progressBar = document.getElementById('progressBar');
    const progressFill = document.getElementById('progressFill');
    
    if (progressBar && progressFill) {
        progressBar.style.display = 'block';
        progressFill.style.width = progress + '%';
    }
}

function hideProgress() {
    const progressBar = document.getElementById('progressBar');
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
// INICIALIZACION
// ============================================================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('Simulador Cuantico cargado');
    console.log('APIs disponibles:');
    console.log('  - REST Simple: /api/quantum/simple');
    console.log('  - REST Completo: /api/quantum/simulate');
    console.log('  - Mock: /api/mock/quantum-simulate');
    console.log('  - WebSocket Simulado: /api/websocket/simulate');
});

// Exportar funciones para uso global
window.runSimpleSimulation = runSimpleSimulation;
window.runAdvancedSimulation = runAdvancedSimulation;
window.runMockSimulation = runMockSimulation;
window.startWebSocketSimulation = startWebSocketSimulation;
window.startBatchSimulation = startBatchSimulation;



