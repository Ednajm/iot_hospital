// Configuration
const API_BASE_URL = 'http://localhost:5000/api';
const UPDATE_INTERVAL = 5000; // 5 seconds
let patientChart = null;
let roomChart = null;
let assetChart = null;

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', function() {
    console.log('🏥 IOT Hospital Dashboard inizializzata');
    
    // Update current date
    updateCurrentDate();
    
    // Initialize charts with smooth transitions
    initializeCharts();
    
    // Load initial data
    loadDashboardData();
    
    // Auto-refresh data
    setInterval(loadDashboardData, UPDATE_INTERVAL);
    
    // Setup navigation
    setupNavigation();
    
    // Add scroll animations
    setupScrollAnimations();
});

// Setup navigation
function setupNavigation() {
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const sidebar = document.getElementById('sidebar');
    const sidebarOverlay = document.getElementById('sidebar-overlay');
    
    // Mobile menu toggle
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', function() {
            sidebar.classList.toggle('show');
            sidebarOverlay.classList.toggle('show');
        });
    }
    
    // Close sidebar when clicking overlay
    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', function() {
            sidebar.classList.remove('show');
            sidebarOverlay.classList.remove('show');
        });
    }
    
    // Close mobile menu when clicking a link
    const navLinks = document.querySelectorAll('.sidebar .nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (window.innerWidth <= 992) {
                sidebar.classList.remove('show');
                sidebarOverlay.classList.remove('show');
            }
        });
    });
    
    // Navbar actions
    const notificationBtn = document.querySelector('.navbar-btn[title="Notifiche"]');
    if (notificationBtn) {
        notificationBtn.addEventListener('click', function() {
            showNotification('Hai 3 nuove notifiche', 'info');
        });
    }
}

// Load all dashboard data
async function loadDashboardData() {
    try {
        await Promise.all([
            loadPatientData(),
            loadRoomData(),
            loadAssetData(),
            loadAlerts(),
            loadRecentActivity()
        ]);
        
        updateLastRefreshTime();
    } catch (error) {
        console.error(' Errore nel caricamento dati:', error);
        showNotification('Errore nel caricamento dati', 'danger');
    }
}

// Load patient data
async function loadPatientData() {
    try {
        // Simulated API call - replace with actual API endpoint
        const data = await fetchAPI('/patients/latest');
        
        // Update stats
        document.getElementById('total-patients').textContent = data.total || '5,000';
        document.getElementById('critical-patients').textContent = data.critical || '12';
        
        // Update chart
        if (patientChart) {
            updatePatientChart(data.timeSeries || generateMockPatientData());
        }
        
        // Update patient table
        updatePatientTable(data.patients || []);
        
    } catch (error) {
        console.error('Errore caricamento dati pazienti:', error);
        // Use mock data if API fails
        updatePatientChart(generateMockPatientData());
    }
}

// Load room data
async function loadRoomData() {
    try {
        const data = await fetchAPI('/rooms/status');
        
        document.getElementById('total-rooms').textContent = data.total || '500';
        document.getElementById('occupied-rooms').textContent = data.occupied || '423';
        
        if (roomChart) {
            updateRoomChart(data.environmental || generateMockRoomData());
        }
        
    } catch (error) {
        console.error('Errore caricamento dati stanze:', error);
        updateRoomChart(generateMockRoomData());
    }
}

// Load asset data
async function loadAssetData() {
    try {
        const data = await fetchAPI('/assets/status');
        
        document.getElementById('total-assets').textContent = data.total || '199';
        document.getElementById('active-assets').textContent = data.active || '187';
        
        if (assetChart) {
            updateAssetChart(data.statusBreakdown || generateMockAssetData());
        }
        
    } catch (error) {
        console.error('Errore caricamento dati asset:', error);
        updateAssetChart(generateMockAssetData());
    }
}

// Load alerts
async function loadAlerts() {
    try {
        const data = await fetchAPI('/alerts/active');
        
        const alertsContainer = document.getElementById('alerts-container');
        const notificationBadge = document.getElementById('notification-badge');
        
        if (!alertsContainer) return;
        
        const alerts = data.alerts || generateMockAlerts();
        
        document.getElementById('active-alerts').textContent = alerts.length;
        
        // Update notification badge
        if (notificationBadge) {
            notificationBadge.textContent = alerts.length;
        }
        
        alertsContainer.innerHTML = alerts.map(alert => `
            <div class="alert-box fade-in">
                <div class="alert-icon">
                    <i class="bi bi-exclamation-triangle-fill"></i>
                </div>
                <div class="alert-content">
                    <h6>${alert.title}</h6>
                    <p>${alert.description} - ${alert.time}</p>
                </div>
            </div>
        `).join('');
        
    } catch (error) {
        console.error('Errore caricamento alert:', error);
    }
}

// Load recent activity
async function loadRecentActivity() {
    try {
        const data = await fetchAPI('/activity/recent');
        const activities = data.activities || [];
        
        // Update activity table if exists
        const activityTable = document.getElementById('activity-table-body');
        if (activityTable && activities.length > 0) {
            activityTable.innerHTML = activities.map(act => `
                <tr>
                    <td>${act.timestamp}</td>
                    <td>${act.type}</td>
                    <td>${act.description}</td>
                    <td><span class="badge bg-${act.status === 'success' ? 'success' : 'warning'}">${act.status}</span></td>
                </tr>
            `).join('');
        }
    } catch (error) {
        console.error('Errore caricamento attività:', error);
    }
}

// Initialize all charts
function initializeCharts() {
    // Patient vital signs chart
    const patientCtx = document.getElementById('patientChart');
    if (patientCtx) {
        patientChart = new Chart(patientCtx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Battito Cardiaco (bpm)',
                    data: [],
                    borderColor: '#dc3545',
                    backgroundColor: 'rgba(220, 53, 69, 0.1)',
                    tension: 0.4,
                    fill: true
                }, {
                    label: 'SpO2 (%)',
                    data: [],
                    borderColor: '#0dcaf0',
                    backgroundColor: 'rgba(13, 202, 240, 0.1)',
                    tension: 0.4,
                    fill: true
                }, {
                    label: 'Temperatura (°C)',
                    data: [],
                    borderColor: '#ffc107',
                    backgroundColor: 'rgba(255, 193, 7, 0.1)',
                    tension: 0.4,
                    fill: true,
                    yAxisID: 'y1'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    intersect: false,
                    mode: 'index'
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        padding: 12,
                        cornerRadius: 8
                    }
                },
                scales: {
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: {
                            display: true,
                            text: 'BPM / SpO2'
                        }
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        title: {
                            display: true,
                            text: 'Temperatura (°C)'
                        },
                        grid: {
                            drawOnChartArea: false
                        }
                    }
                }
            }
        });
    }

    // Room environmental chart
    const roomCtx = document.getElementById('roomChart');
    if (roomCtx) {
        roomChart = new Chart(roomCtx, {
            type: 'bar',
            data: {
                labels: [],
                datasets: [{
                    label: 'Temperatura (°C)',
                    data: [],
                    backgroundColor: '#198754',
                    borderRadius: 6
                }, {
                    label: 'Umidità (%)',
                    data: [],
                    backgroundColor: '#0dcaf0',
                    borderRadius: 6
                }, {
                    label: 'CO2 (ppm)',
                    data: [],
                    backgroundColor: '#ffc107',
                    borderRadius: 6,
                    yAxisID: 'y1'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Temperatura / Umidità'
                        }
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        title: {
                            display: true,
                            text: 'CO2 (ppm)'
                        },
                        grid: {
                            drawOnChartArea: false
                        }
                    }
                }
            }
        });
    }
    const assetCtx = document.getElementById('assetChart');
    if (assetCtx) {
        assetChart = new Chart(assetCtx, {
            type: 'doughnut',
            data: {
                labels: ['Attivi', 'Standby', 'Manutenzione'],
                datasets: [{
                    data: [0, 0, 0],
                    backgroundColor: ['#198754', '#ffc107', '#dc3545'],
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.parsed || 0;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((value / total) * 100).toFixed(1);
                                return `${label}: ${value} (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });
    }
}

// Update patient chart
function updatePatientChart(data) {
    if (!patientChart || !data) return;
    
    patientChart.data.labels = data.labels || [];
    patientChart.data.datasets[0].data = data.heartRate || [];
    patientChart.data.datasets[1].data = data.spo2 || [];
    patientChart.data.datasets[2].data = data.temperature || [];
    patientChart.update('none');
}

// Update room chart
function updateRoomChart(data) {
    if (!roomChart || !data) return;
    
    roomChart.data.labels = data.labels || [];
    roomChart.data.datasets[0].data = data.temperature || [];
    roomChart.data.datasets[1].data = data.humidity || [];
    roomChart.data.datasets[2].data = data.co2 || [];
    roomChart.update('none');
}

// Update asset chart
function updateAssetChart(data) {
    if (!assetChart || !data) return;
    
    assetChart.data.datasets[0].data = [
        data.active || 0,
        data.standby || 0,
        data.maintenance || 0
    ];
    assetChart.update('none');
}

// Update patient table
function updatePatientTable(patients) {
    const tableBody = document.getElementById('patient-table-body');
    if (!tableBody) return;
    
    if (patients.length === 0) {
        patients = generateMockPatients();
    }
    
    tableBody.innerHTML = patients.slice(0, 10).map(patient => `
        <tr>
            <td><strong>${patient.id}</strong></td>
            <td>${patient.name}</td>
            <td><span class="badge bg-${getHeartRateColor(patient.heartRate)}">${patient.heartRate} bpm</span></td>
            <td>${patient.temperature}°C</td>
            <td>${patient.spo2}%</td>
            <td><span class="status-badge badge bg-${patient.status === 'Normal' ? 'success' : 'danger'}">
                <i class="bi bi-circle-fill"></i> ${patient.status}
            </span></td>
        </tr>
    `).join('');
}

// Utility: Get heart rate color
function getHeartRateColor(rate) {
    if (rate < 60 || rate > 100) return 'danger';
    if (rate < 70 || rate > 90) return 'warning';
    return 'success';
}

// Update last refresh time
function updateLastRefreshTime() {
    const timeElement = document.getElementById('last-refresh-time');
    if (timeElement) {
        const now = new Date();
        timeElement.innerHTML = `<i class="bi bi-clock me-1"></i>Ultimo aggiornamento: ${now.toLocaleTimeString('it-IT')}`;
    }
}

// Update current date
function updateCurrentDate() {
    const dateElement = document.getElementById('current-date');
    if (dateElement) {
        const now = new Date();
        const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        dateElement.textContent = now.toLocaleDateString('it-IT', options);
    }
}

// Setup scroll animations
function setupScrollAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, {
        threshold: 0.1
    });

    document.querySelectorAll('.stat-card, .chart-card, .data-table').forEach((el) => {
        observer.observe(el);
    });
}

// Show notification
function showNotification(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    document.body.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    setTimeout(() => toast.remove(), 3000);
}

// API fetch helper
async function fetchAPI(endpoint) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.warn(`API ${endpoint} non disponibile, uso dati mock`);
        throw error;
    }
}

// Mock data generators (for development/testing)
function generateMockPatientData() {
    const labels = [];
    const heartRate = [];
    const spo2 = [];
    const temperature = [];
    
    for (let i = 10; i >= 0; i--) {
        const time = new Date(Date.now() - i * 30000);
        labels.push(time.toLocaleTimeString('it-IT', { hour: '2-digit', minute: '2-digit' }));
        heartRate.push(Math.floor(Math.random() * 30) + 70);
        spo2.push(Math.floor(Math.random() * 5) + 95);
        temperature.push(+(Math.random() * 1.5 + 36.5).toFixed(1));
    }
    
    return { labels, heartRate, spo2, temperature };
}

function generateMockRoomData() {
    const rooms = ['Room1', 'Room2', 'Room3', 'Room4', 'Room5'];
    return {
        labels: rooms,
        temperature: rooms.map(() => +(Math.random() * 5 + 22).toFixed(1)),
        humidity: rooms.map(() => Math.floor(Math.random() * 20) + 45),
        co2: rooms.map(() => Math.floor(Math.random() * 300) + 400)
    };
}

function generateMockAssetData() {
    return {
        active: Math.floor(Math.random() * 20) + 170,
        standby: Math.floor(Math.random() * 10) + 15,
        maintenance: Math.floor(Math.random() * 8) + 5
    };
}

function generateMockAlerts() {
    return [
        {
            title: 'Paziente 2341 - Battito Anomalo',
            description: 'Battito cardiaco sopra 120 bpm',
            time: '2 min fa'
        },
        {
            title: 'Room156 - CO2 Elevato',
            description: 'Livello CO2: 980 ppm',
            time: '5 min fa'
        },
        {
            title: 'Asset127 - Batteria Bassa',
            description: 'Livello batteria: 18%',
            time: '8 min fa'
        }
    ];
}

function generateMockPatients() {
    const names = ['Mario Rossi', 'Luigi Bianchi', 'Anna Verdi', 'Paolo Neri', 'Sara Gialli'];
    return Array.from({ length: 5 }, (_, i) => ({
        id: `P${1000 + i}`,
        name: names[i],
        heartRate: Math.floor(Math.random() * 40) + 65,
        temperature: +(Math.random() * 1.5 + 36.5).toFixed(1),
        spo2: Math.floor(Math.random() * 8) + 93,
        status: Math.random() > 0.7 ? 'Alert' : 'Normal'
    }));
}

// Refresh button handler
document.addEventListener('DOMContentLoaded', function() {
    const refreshBtn = document.getElementById('refresh-btn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', function() {
            this.style.transform = 'scale(1.1) rotate(360deg)';
            loadDashboardData();
            setTimeout(() => {
                this.style.transform = '';
            }, 600);
        });
    }
});
