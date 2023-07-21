function CustomPeriod(periodInSeconds) {
    this.periodInSeconds = periodInSeconds;
}

CustomPeriod.prototype.get = function() {
    return this.periodInSeconds;
}

CustomPeriod.prototype.timeFormat = function() {
    function num(val){
        val = Math.floor(val);
        return val < 10 ? '0' + val : val;
    }
    var sec = this.periodInSeconds
          , hours = sec / 3600  % 24
          , minutes = sec / 60 % 60
          , seconds = sec % 60
        ;
    return num(hours) + ":" + num(minutes) + ":" + num(seconds);
    
}