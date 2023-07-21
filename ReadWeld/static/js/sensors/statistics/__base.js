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






function BarСhart(canvas, labels, dataset, name, color=undefined) {

    this.labels = labels;
    this.dataset = dataset;
    this.canvas = canvas;

    const __colorForLine = color.creat()
    const __colorForBar = color.reduceBrightness(2).creat()

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


BarСhart.prototype.creat = function(max=undefined, __callbacks={}) {
    const config = {
        type: 'bar',
        data: this.data,
        options: {
            plugins: {
                tooltip: {
                    enabled: true,
                    callbacks: __callbacks
                }
            },
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
