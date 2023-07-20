new Chart(
    document.getElementById('category_pie').getContext('2d'),
    {
        type: 'pie',
        data: {
            labels: pie_labels,
            datasets: [{
                label: 'NZD',
                data: pie_data,
                backgroundColor: backgroundColor
            }]
        },
        options: {}
    }
);
