function log_tab_behavior(time, behave){

    body = JSON.stringify({
        time: time,
        behave: behave
    })
    console.log(body)
    fetch("tab_behavior_logger/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: body,
    }).then(response => response.json())
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}


window.addEventListener('blur', () => {
    time = Date.now();
    console.log('Tab đã bị chuyển đi - ' + time);
    log_tab_behavior(time=time, behave="blur")
});


window.addEventListener('focus', () => {
    time = Date.now();
    console.log('Tab đã được quay lại - ' + time);
    log_tab_behavior(time=time, behave="focus")
});


function startTimer(duration, display) {
    var start = new Date(document.querySelector("#time_start").getAttribute("time_start")).getTime(),
        diff,
        hours,
        minutes,
        seconds;
    function timer() {
        diff = duration - (((Date.now() - start) / 1000) | 0);

        hours = (diff / 3600) | 0;
        minutes = ((diff % 3600) / 60) | 0;
        seconds = (diff % 60) | 0;

        hours = hours < 10 ? "0" + hours : hours;
        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = "Time Left: " + hours + ":" + minutes + ":" + seconds;

        if (diff <= 0) {
            document.querySelector('#submit_btn').click();
        }
    };
    // Run the timer function every second
    timer();
    setInterval(timer, 1000);
}

window.onload = function () {
    var duration = document.querySelector('#time_limit').getAttribute('value') *60;
    var display = document.querySelector('#timer');

    startTimer(duration, display);
};