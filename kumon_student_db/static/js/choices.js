var chartHow = c3.generate({
    bindto: '#chart-how',
    data: {
        url: '/registration/api/how_choice_data/',
        mimeType: 'json',
        type: 'donut',
    },
});

var chartWhy = c3.generate({
    bindto: '#chart-why',
    data: {
        url: '/registration/api/why_choice_data/',
        mimeType: 'json',
        type: 'donut',
    },
});
