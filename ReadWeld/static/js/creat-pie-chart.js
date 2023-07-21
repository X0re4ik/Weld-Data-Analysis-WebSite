



function creatPerformancePieChart(chart, workAndKaifInSeconds) {
        
    const workInSeconds = workAndKaifInSeconds[0];
    const kaifInSeconds = workAndKaifInSeconds[1];
    const totalTime = workInSeconds + kaifInSeconds || 1;
    const workInPercent = workInSeconds / totalTime;

    const data = {
        labels: [
            'Работа',
            'Простой'
        ],
        datasets: [{
            label: '',
            data: [workInPercent, 1-workInPercent],
            backgroundColor: [
            'rgba(242, 7, 7, 1)',
            'rgba(1, 22, 84, 1)'
            ],
            hoverOffset: 4
        }]
    };
    const config = {
        type: 'doughnut',
        data: data,
        options: {
            plugins: {
                tooltip: {
                    enabled: true,
                    callbacks: {
                        label: function(context) {
                            const lable = context.label;
                            const value = context.parsed.toFixed(2)*100
                            return `${lable}: ${value}%`;
                        }
                    }
                }
            }
        }
    };
    return new Chart(chart, config);
}


function creatPerformancePieCharts(charts, efficiencyOfWelders) {
    for (let i = 0; i < charts.length; ++i) {
        let chart                   = charts[i]
        let welderEfficiency       = efficiencyOfWelders[i];

        creatPerformancePieChart(chart, welderEfficiency)
    }
}