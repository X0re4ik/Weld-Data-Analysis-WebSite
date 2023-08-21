




class PageHandle {
    constructor() {
        this.name = "Страница статистики"
        this.url = new URL(window.location.href)

        this.currentYear    = this.url.searchParams.get("year")
        this.numberOfWeek   = this.url.searchParams.get("number_of_week")


        this.dataForCharts = {
            labels: ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        }

        const __value = `${this.currentYear}-W${(this.numberOfWeek < 10) ? ('0'+this.numberOfWeek): (this.numberOfWeek)}`; 
        document.getElementById('choose-week').setAttribute("value", __value);
        document.getElementById('refresh-button').onclick = this.toUpdatePage;
    }



    dataСollection(reports) {
        this.dailyReports = []
        for (let i = 0; i < reports.length; ++i){
            const report = reports[i];
            this.dailyReports.push(DailyReport.fromObject(report));
        }
        return this;
    }



    tableForMainChart(dailyReport) {
        let parent = document.getElementById('for-data');
        while (parent.firstChild) {
            parent.removeChild(parent.firstChild);
        }
        dailyReport.createForHTML(parent);
    }

    creatAuxiliaryCharts() {
        let expendedWire = []
        let expendedGas = []
        let performance = []
        for (let i = 0; i < this.dailyReports.length; ++i) {
            const dailyReport = this.dailyReports[i];
            expendedWire.push(dailyReport.expendedWire);
            expendedGas.push(dailyReport.expendedGas);
            performance.push(dailyReport.calculatePerformance())
        }

        const weeklyCharts = document.getElementsByClassName('weekly-charts');
        const expended = [
        {
            "values": performance,
            "title": "Загрузка обороужования",
            "color": new makerRGBA(196, 35, 35, 1),
            "canvas": weeklyCharts[0],
            "max": 100,
            "ms": "%"
        },
        {
            "values": expendedGas,
            "title": "Расход газа",
            "color": new makerRGBA(185, 194, 14, 1),
            "canvas": weeklyCharts[1],
            "ms": "л"
        }, {
            "values": expendedWire,
            "title": "Расход проволки",
            "color": new makerRGBA(44, 173, 9, 1),
            "canvas": weeklyCharts[2],
            "ms": "кг"
        }];

        const __dailyReports = this.dailyReports;
        const __func = this.tableForMainChart;

        const __callbacks = function(ms) {
            return {
                label: function(context) {
                    const dataIndex = context.dataIndex
                    const dailyReport = __dailyReports.at(dataIndex)
                    
                    __func(dailyReport);
    
    
                    const welder = dailyReport.worker;
    
                    if (context.parsed.y !== null) {
                        let text = 'Неизвестный сварщик'
                        if (welder) text = `${welder.firstName} ${welder.secondName}`
                        text += `: ${context.parsed.y.toFixed(2)} ${ms}`;
                        return text;
                    }
                }      
            };
        }

        expended.forEach(
            (value, index, array) => {
                const newChart = (new BarСhart(value.canvas, this.dataForCharts.labels, 
                    value.values, value.title, 
                    value.color)).creat(value.max, __callbacks(value.ms));

                function clickHandler(evt) {
                    const points = newChart.getElementsAtEventForMode(evt, 'nearest', { intersect: true }, true);
                
                    if (points.length) {
                        const firstPoint = points[0];
                        window.open(__dailyReports[firstPoint.index].linkToDailyStats())
                    }
                }
        
                value.canvas.onclick = clickHandler;
            }
        )
        return this;
    }

    toUpdatePage() {
        const yearWithNumberOfWeek = document.getElementById('choose-week').value;
        let data = yearWithNumberOfWeek.split('-');
        const newYear = Number(data[0])
        const newNumberOfWeek = Number(data[1].substring(1));

        let currentURL = new URL(window.location.href)

        currentURL.searchParams.set("year", newYear);
        currentURL.searchParams.set("number_of_week", newNumberOfWeek);
        window.location.href = currentURL.href;
    }
}






var pageHandle = new PageHandle();