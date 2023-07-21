




function generateColor() {
    return '#' + Math.floor(Math.random()*16777215).toString(16)
}




class WeeklyStatisticsСhart {

    constructor(canvas, statistics) {

        this.canvas = canvas;
        this.statistics = statistics;


        this.data = {
            labels: [],
            datasets: [{
                label: 'Показатели производительности',
                data: [],
                backgroundColor: [],
                borderColor: [],
                borderWidth: 1
            }]
        };
    }


    getConfig() {
        const __statistics = this.statistics
        const config = {
            type: 'bar',
            data: this.data,
            options: {
                plugins: {
                    tooltip: {
                        enabled: true,
                        callbacks: {
                            label: function(context) {
                                console.log(context);
                                const dataIndex = context.dataIndex
                                const statistic = __statistics.at(dataIndex)


                                
                                let father = document.getElementById('father')
                                new DetailedIndicationsForWork(father).creat(statistic)

                                const welder = statistic.worker


                                if (context.parsed.y !== null) {
                                    let text = 'Неизвестный сварщик'
                                    if (welder) text = `${welder.first_name} ${welder.second_name}`
                                    text += `: ${context.parsed.y.toFixed(2)*100}%`;
                                    return text;
                                }
                            }
                        }
                    }
                },
                scales: {
                y: {
                    beginAtZero: true,
                    max: 1
                    }
                },
            },
            //plugins: [customTooltip]
        };
        return config;
    }


    getChart() {
        const config = this.getConfig();
        return new Chart(
            this.canvas,
            config
        );
    }


    setLable() {
        for (let i = 0; i < this.statistics.length; ++i) {
            let statistic = this.statistics[i];
            const date = statistic.date
            const lable = `${date.getDay()}.${date.getMonth()}.${date.getFullYear()}`
            console.log(lable)
            this.data.labels.push(lable);
        }
        return this;
    }

    setData() {
        for (let i = 0; i < this.statistics.length; ++i) {
            performance = 0;
            let statistic = this.statistics[i];
            if (statistic.sensor_id)
                performance =  statistic.running_time_in_seconds / (statistic.running_time_in_seconds + statistic.idle_time_in_seconds);
            this.data.datasets[0].data.push(performance);
        }
        return this;
    }
};