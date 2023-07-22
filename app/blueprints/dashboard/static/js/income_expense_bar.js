new Chart(
    document.getElementById('income_expense_bar').getContext('2d'),
    {
        type: 'bar',
        data: {
            labels: bar_labels,
            datasets: [{
                label: 'Income vs Expenses',
                data: bar_data,
                backgroundColor: backgroundColor
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            maintainAspectRatio: false
        }
    }
);
