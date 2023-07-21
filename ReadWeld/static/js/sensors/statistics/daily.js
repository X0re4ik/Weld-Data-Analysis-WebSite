


function makerRGBA(R, G, B, A) {
    this.rgba = [R, G, B, A]
}


makerRGBA.prototype.reduceBrightness = function(x) {
    if (x != 0) this.rgba[3] = this.rgba[3] / x
    return this
}

makerRGBA.prototype.creat = function() {
    return `rgba(${this.rgba[0]}, ${this.rgba[1]}, ${this.rgba[2]}, ${this.rgba[3]})`
}




function PageHandle() {
    this.name = "Страница статистики"
    this.url = new URL(window.location.href)

    this.currentDate = new Date(
        this.url.searchParams.get("year"),
        this.url.searchParams.get("month") - 1,
        this.url.searchParams.get("day")
    )


    
}


PageHandle.init = () =>  {
    let ph = new PageHandle();

    ph.setDefaultForm();
    ph.refreshButtonListener();
}

PageHandle.prototype.setDefaultForm = function() {
    let chooseInterval = document.getElementById('choose-interval');
    const interval = this.url.searchParams.get("interval")
    chooseInterval.setAttribute("value", interval)

    formatDate = (date) => {

        var dd = date.getDate();
        if (dd < 10) dd = '0' + dd;
      
        var mm = date.getMonth() + 1;
        if (mm < 10) mm = '0' + mm;
      
        var yy = date.getFullYear();
      
        return yy + '-' + mm + '-' + dd;
      }

    let chooseDate = document.getElementById('choose-date');
    chooseDate.setAttribute("value", formatDate(this.currentDate))

}


PageHandle.prototype.refreshButtonListener = function() {
    let refreshButton = document.getElementById('refresh-button')
    const currentURL = this.url;
    refreshButton.onclick = function() {
        const interval = document.getElementById('choose-interval').value;
        const dateInList = document.getElementById('choose-date').value.split('-')
        const date = new Date(Number(dateInList[0]), Number(dateInList[1]), Number(dateInList[2]));
        let newURL = new URL(`${currentURL.origin}${currentURL.pathname}`);
        newURL.searchParams.set("year", date.getFullYear());
        newURL.searchParams.set("month", date.getMonth());
        newURL.searchParams.set("day", date.getDate());
        newURL.searchParams.set("interval", interval);
        console.log(newURL.href)
        window.location.href = newURL.href;
    }

}



function creatCharts(canvases, statistics) {



    data = {}
    const parametrs = [["performance", "Производительность", new makerRGBA(235, 0, 0, 0.8), "%", 100], 
        ["amperage", "Сила тока", new makerRGBA(209, 65, 8, 0.8), "А", 500], 
        ["gas_consumption", "Расход газа", new makerRGBA(189, 171, 9, 0.8), "л/мин", 50], 
        ["wire_consumption", "Расход проволки", new makerRGBA(8, 161, 51, 0.8), "кг/час"],
        ["date", "Время", "", ""]
    ];
    parametrs.forEach(
        (value, index, array) => {
            data[value[0]] = {
                "title": value[1],
                "color": value[2],
                "values": [],
                "canvas": canvases[index],
                "ms": value[3],
                "max": value[4]
            }
        }
    )


    for (let i = 0; i < statistics.length; ++i) {
        let statistic = statistics[i];
        const keys = Object.keys(data);

        for (let j = 0; j < keys.length; ++j) {
            const key = keys[j];
            const value = statistic[key];
            data[key].values.push(value)  
        }
    }

    const lables = data.date.values;
    for (const [key, value] of Object.entries(data)) {
        if (key == "date") continue;
        (new BarСhart(value.canvas, lables, value.values, value.title, value.color)).creat(value.max);
    }
    return data
}


function BarСhart(canvas, labels, dataset, name, color=undefined) {

    this.labels = labels;
    this.dataset = dataset;
    this.canvas = canvas;

    const __colorForLine = color.creat()
    const __colorForBar = color.reduceBrightness(5).creat()

    console.log(__colorForLine, __colorForBar)

    this.data = {
        labels: this.labels,
        datasets: [{
                label: name + " bar",
                data: this.dataset,
                backgroundColor: [__colorForBar],
                borderColor: [__colorForBar],
                borderWidth: 0.5
            },{
                label: name + " line",
                data: this.dataset,
                backgroundColor: [__colorForLine],
                borderColor: [__colorForLine],
                borderWidth: 2,
                type: 'line',
                order: 0
            }
        ]
    };
}


BarСhart.prototype.creat = function(max=undefined) {
    const config = {
        type: 'bar',
        data: this.data,
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    max: max
                }
            }
        },
    };
    return new Chart(
        this.canvas, config
    );
}
