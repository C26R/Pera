new Chart(
    document.getElementById('paye_pie').getContext('2d'),
    {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                label: 'NZD',
                data: data,
                backgroundColor: backgroundColor
            }]
        },
        options: {}
    }
);