function DailyReport(
    id, date,
    averageAmperage, averageGasConsumption, averageWireConsumption, 
    expendedWire, expendedGas,
    worker,
    runningTimeInSeconds, idleTimeInSeconds) {

        this.id = id;
        this.date = new Date(date.year, date.month - 1, date.day);

        this.averageAmperage = averageAmperage;
        this.averageGasConsumption = averageGasConsumption;
        this.averageWireConsumption = averageWireConsumption;

        this.expendedWire = expendedWire;
        this.expendedGas = expendedGas;

        this.worker = worker ? (Worker.fromOblect(worker)) : (null);

        this.runningTimeInSeconds = new CustomPeriod(runningTimeInSeconds);
        this.idleTimeInSeconds = new CustomPeriod(idleTimeInSeconds);
}

DailyReport.prototype.calculatePerformance = function() {
    const totalTime = this.runningTimeInSeconds.get() + this.idleTimeInSeconds.get()

    if (totalTime == 0) return 0
    const performance =  this.runningTimeInSeconds.get() / totalTime * 100;

    return performance;
}


DailyReport.fromObject = (__object) => {
    const dataJSON = __object;

    return new DailyReport(
        dataJSON.id, dataJSON.date,
        dataJSON.average_amperage, dataJSON.average_gas_consumption, dataJSON.average_wire_consumption,
        dataJSON.expended_wire, dataJSON.expended_gas, 
        dataJSON.worker,
        dataJSON.running_time_in_seconds, dataJSON.idle_time_in_seconds
    )
}
DailyReport.prototype.linkToDailyStats = function() {
    const currentURL = new URL(window.location.href);

    const origin = currentURL.origin;
    const pathname = currentURL.pathname;
    let updatePathname = pathname.split('/');
    updatePathname[updatePathname.length - 1] = "daily";
    const newPathname = updatePathname.join('/');

    const year = this.date.getFullYear();
    const month = this.date.getMonth() + 1;
    const day = this.date.getDate();
    const interval = 15;

    const queryset = {
        "year": year,
        "month": month,
        "day": day,
        "interval": interval
    }



    let newURL = new URL(origin+newPathname);
    for (var key in queryset) {
        newURL.searchParams.set(key, queryset[key])
    }
    return newURL.href;
}

DailyReport.prototype.createForHTML = function(parent) {
    let newH2 = document.createElement("h2");
    newH2.className = "stat_title";
    let newSpan10 = document.createElement("span");

    newSpan10.innerHTML = `${this.date.getFullYear()}/${this.date.getMonth()+1}/${this.date.getDate()}`;
    
    newH2.appendChild(newSpan10)
    parent.appendChild(newH2)

    const variables = [
        {
            value: this.averageAmperage.toFixed(2),
            title: "Средняя сила тока",
            measurementSystem: " А"
        },
        {
            value: this.averageGasConsumption.toFixed(2),
            title: "Средний расход газа",
            measurementSystem: " л/час"
        },
        {
            value: this.averageWireConsumption.toFixed(2),
            title: "Средний расход провлоки",
            measurementSystem: " кг/час"
        },
        {
            value: this.expendedWire.toFixed(2),
            title: "Потрачено сварочной проволки",
            measurementSystem: " кг"
        },
        {
            value: this.expendedGas.toFixed(2),
            title: "Потрачено сварочного газа",
            measurementSystem: " л"
        },
        {
            value: this.worker ? this.worker.fullName() : "Пеннивайз 🤡",
            title: "Сварщик",
            measurementSystem: ""
        },
        {
            value: this.runningTimeInSeconds.timeFormat(),
            title: "Время работы",
            measurementSystem: ""
        },
        {
            value: this.idleTimeInSeconds.timeFormat(),
            title: "Время простоя",
            measurementSystem: ""
        }
    ];



    variables.forEach((element, index, array) => {
        let newDiv = document.createElement("div");
        newDiv.className = "stat_detail";

        let newP1 = document.createElement("p");
        newP1.innerHTML = element.title;

        let newSpan1 = document.createElement("span");
        newSpan1.className = "stat_detail__value";
        newSpan1.innerHTML = element.value;

        let newSpan2 = document.createElement("span");
        newSpan2.className = "stat_detail__unit"
        newSpan2.innerHTML = element.measurementSystem;

        let newP2 = document.createElement("p");
        newP2.appendChild(newSpan1);
        newP2.appendChild(newSpan2);


        let newDiv2 = document.createElement("div");
        newDiv2.className = "dots";

        newDiv.appendChild(newP1);
        newDiv.appendChild(newDiv2);
        newDiv.appendChild(newP2);

        parent.appendChild(newDiv)
    });


    let newLink = document.createElement("a");
    newLink.innerHTML = "Подробнее";
    newLink.target = "_black";
    newLink.href = this.linkToDailyStats();
    parent.appendChild(newLink)
}
