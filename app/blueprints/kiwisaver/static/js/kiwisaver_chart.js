new Chart(
    document.getElementById('kiwisaver-chart').getContext('2d'),
    {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'KiwiSaver',
                data: data,
                borderColor: '#6A0DAD'
            }]
        },
        options: {
            maintainAspectRatio: false,
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'day'
                    }
                }
            },
            elements: {
                point: {
                    radius: 0
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    }
);