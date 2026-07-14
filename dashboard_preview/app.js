document.addEventListener('DOMContentLoaded', () => {
    // Current filter states
    let activeYear = 'All';
    let activeCategory = 'All';
    let currentTab = 'executive-summary';

    // Chart instances
    let trendChart = null;
    let subcatChart = null;
    let mapInstance = null;
    let mapMarkers = [];

    // Tab Switching
    const menuItems = document.querySelectorAll('.menu-item');
    menuItems.forEach(item => {
        item.addEventListener('click', (e) => {
            const selectedTab = e.currentTarget.getAttribute('data-tab');
            if (selectedTab) {
                // Remove active classes
                menuItems.forEach(m => m.classList.remove('active'));
                document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
                
                // Add active classes
                e.currentTarget.classList.add('active');
                document.getElementById(selectedTab).classList.add('active');
                currentTab = selectedTab;
                
                // Trigger map refresh if map tab is chosen
                if (selectedTab === 'regional-mapping') {
                    setTimeout(initMap, 100);
                }
            }
        });
    });

    // Control Select Listeners
    const yearSelect = document.getElementById('year-select');
    const categorySelect = document.getElementById('category-select');

    yearSelect.addEventListener('change', (e) => {
        activeYear = e.target.value;
        updateDashboard();
    });

    categorySelect.addEventListener('change', (e) => {
        activeCategory = e.target.value;
        updateDashboard();
    });

    // Main Update Pipeline
    function updateDashboard() {
        const data = getFilteredData();
        renderKPIs(data);
        renderTrendChart(data);
        renderSubcatChart(data);
        renderMatrixTable(data);
        updateMap(data);
    }

    // Filter Logic
    function getFilteredData() {
        let states = dashboardData.states;
        let trend = dashboardData.trend;
        let matrix = dashboardData.matrix;
        let subcat = dashboardData.subcat;

        // Filter by Year
        if (activeYear !== 'All') {
            const yr = parseInt(activeYear);
            states = states.filter(x => x.year === yr);
            trend = trend.filter(x => x.year === yr);
            matrix = matrix.filter(x => x.year === yr);
            subcat = subcat.filter(x => x.year === yr);
        }

        // Filter by Category
        if (activeCategory !== 'All') {
            matrix = matrix.filter(x => x.category === activeCategory);
            subcat = subcat.filter(x => x.category === activeCategory);
        }

        return { states, trend, matrix, subcat };
    }

    // Render KPIs
    function renderKPIs(data) {
        // Calculate totals dynamically from states data
        const totalSales = data.states.reduce((acc, curr) => acc + curr.sales, 0);
        const totalProfit = data.states.reduce((acc, curr) => acc + curr.profit, 0);
        const margin = totalSales > 0 ? (totalProfit / totalSales) * 100 : 0;
        
        // Approximate orders based on filtered scale
        const scaleFactor = activeYear === 'All' ? 1 : 0.25;
        const totalOrders = Math.round(dashboardData.summary.orders * scaleFactor);

        document.getElementById('sales-kpi').textContent = '$' + totalSales.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2});
        document.getElementById('profit-kpi').textContent = '$' + totalProfit.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2});
        document.getElementById('margin-kpi').textContent = margin.toFixed(2) + '%';
        document.getElementById('orders-kpi').textContent = totalOrders.toLocaleString();
        
        // Format positive/negative margin color
        const marginEl = document.getElementById('margin-kpi');
        if (totalProfit < 0) {
            marginEl.style.color = 'var(--danger-color)';
        } else {
            marginEl.style.color = 'var(--success-color)';
        }
    }

    // Render Trend Chart (Sales & Profit MoM)
    function renderTrendChart(data) {
        // Aggregate by month name
        const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        const monthlySales = Array(12).fill(0);
        const monthlyProfit = Array(12).fill(0);

        const monthMap = {
            'Jan': 0, 'Feb': 1, 'Mar': 2, 'Apr': 3, 'May': 4, 'Jun': 5,
            'Jul': 6, 'Aug': 7, 'Sep': 8, 'Oct': 9, 'Nov': 10, 'Dec': 11
        };

        data.trend.forEach(t => {
            const idx = monthMap[t.month];
            if (idx !== undefined) {
                monthlySales[idx] += t.sales;
                monthlyProfit[idx] += t.profit;
            }
        });

        const ctx = document.getElementById('trendChart').getContext('2d');

        if (trendChart) {
            trendChart.destroy();
        }

        trendChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: months,
                datasets: [
                    {
                        label: 'Revenue ($)',
                        data: monthlySales,
                        backgroundColor: '#3b82f6',
                        yAxisID: 'y'
                    },
                    {
                        label: 'Net Profit ($)',
                        data: monthlyProfit,
                        borderColor: '#10b981',
                        backgroundColor: 'rgba(16, 185, 129, 0.1)',
                        type: 'line',
                        yAxisID: 'y1',
                        fill: true
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: { display: true, text: 'Revenue ($)' }
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        grid: { drawOnChartArea: false },
                        title: { display: true, text: 'Net Profit ($)' }
                    }
                }
            }
        });
    }

    // Render Subcategory Bar Chart (Tornado style/Positive-Negative bars)
    function renderSubcatChart(data) {
        // Group by subcategory
        const subcatMap = {};
        data.subcat.forEach(s => {
            if (!subcatMap[s.subCategory]) {
                subcatMap[s.subCategory] = { sales: 0, profit: 0 };
            }
            subcatMap[s.subCategory].sales += s.sales;
            subcatMap[s.subCategory].profit += s.profit;
        });

        const subcategories = Object.keys(subcatMap);
        const profitValues = subcategories.map(name => subcatMap[name].profit);
        
        // Sort descending by profit
        const zip = subcategories.map((k, i) => [k, profitValues[i]]);
        zip.sort((a, b) => b[1] - a[1]);

        const labels = zip.map(x => x[0]);
        const dataValues = zip.map(x => x[1]);

        const ctx = document.getElementById('subcatChart').getContext('2d');

        if (subcatChart) {
            subcatChart.destroy();
        }

        subcatChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Net Profit ($)',
                    data: dataValues,
                    backgroundColor: dataValues.map(v => v < 0 ? '#ef4444' : '#10b981')
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                }
            }
        });
    }

    // Render Category/Segment Matrix Grid
    function renderMatrixTable(data) {
        const segments = ['Consumer', 'Corporate', 'Home Office'];
        const categories = ['Furniture', 'Office Supplies', 'Technology'];
        
        const grid = {};
        categories.forEach(c => {
            grid[c] = {};
            segments.forEach(s => {
                grid[c][s] = { sales: 0, profit: 0 };
            });
        });

        data.matrix.forEach(m => {
            if (grid[m.category] && grid[m.category][m.segment]) {
                grid[m.category][m.segment].sales += m.sales;
                grid[m.category][m.segment].profit += m.profit;
            }
        });

        const tbody = document.getElementById('matrix-body');
        tbody.innerHTML = '';

        categories.forEach(c => {
            let rowHtml = `<tr><td><strong>${c}</strong></td>`;
            segments.forEach(s => {
                const sVal = grid[c][s].sales;
                const pVal = grid[c][s].profit;
                rowHtml += `
                    <td>
                        <div>$${sVal.toLocaleString(undefined, {maximumFractionDigits:0})}</div>
                        <div style="font-size:11px; color:${pVal < 0 ? 'var(--danger-color)' : 'var(--success-color)'}">
                            $${pVal.toLocaleString(undefined, {maximumFractionDigits:0})} Profit
                        </div>
                    </td>`;
            });
            rowHtml += `</tr>`;
            tbody.innerHTML += rowHtml;
        });
    }

    // Initialize Map Visual (Leaflet.js)
    function initMap() {
        if (!mapInstance) {
            // Center map on United States
            mapInstance = L.map('map').setView([37.0902, -95.7129], 4);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap contributors'
            }).addTo(mapInstance);
        }
        updateMap(getFilteredData());
    }

    // Update Map Markers
    function updateMap(data) {
        if (!mapInstance) return;

        // Clear existing markers
        mapMarkers.forEach(m => mapInstance.removeLayer(m));
        mapMarkers = [];

        // Aggregate by state
        const stateMap = {};
        data.states.forEach(s => {
            if (!stateMap[s.state]) {
                stateMap[s.state] = { sales: 0, profit: 0, lat: s.lat, lng: s.lng };
            }
            stateMap[s.state].sales += s.sales;
            stateMap[s.state].profit += s.profit;
        });

        Object.keys(stateMap).forEach(name => {
            const info = stateMap[name];
            const isLoss = info.profit < 0;
            const color = isLoss ? 'var(--danger-color)' : 'var(--success-color)';

            // Circle Radius maps to sales scale
            const radius = Math.max(10, Math.min(45, Math.sqrt(info.sales) * 0.15));

            const circle = L.circleMarker([info.lat, info.lng], {
                radius: radius,
                fillColor: color,
                color: color,
                fillOpacity: 0.6,
                weight: 1
            }).addTo(mapInstance);

            const popupContent = `
                <div style="font-family:sans-serif; min-width:140px;">
                    <h4 style="margin-bottom:6px; font-weight:700;">${name}</h4>
                    <div style="font-size:12px; margin-bottom:4px;">Revenue: <strong>$${info.sales.toLocaleString(undefined, {maximumFractionDigits:2})}</strong></div>
                    <div style="font-size:12px; color:${isLoss ? 'var(--danger-color)' : 'var(--success-color)'}">
                        Profit: <strong>$${info.profit.toLocaleString(undefined, {maximumFractionDigits:2})}</strong>
                    </div>
                </div>
            `;
            circle.bindPopup(popupContent);
            mapMarkers.push(circle);
        });
    }

    // Initialize Dashboard
    updateDashboard();
});
