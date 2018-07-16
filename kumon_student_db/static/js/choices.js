var chartHow = c3.generate({
    bindto: '#chart-how',
    data: {
        columns: [
            ['data1', 30,],
            ['data2', 50,]
        ],
        type: 'donut',
    },
});

var chartWhy = c3.generate({
    bindto: '#chart-why',
    data: {
        columns: [
        ],
        type: 'donut',
    },
});
