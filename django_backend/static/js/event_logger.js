function log_tab_behavior(time, behavior){

    body = JSON.stringify({
        time: time,
        behavior: behavior
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
    // console.log('Tab đã bị chuyển đi - ' + time);
    log_tab_behavior(time=time, behavior="blur")
});


window.addEventListener('focus', () => {
    time = Date.now();
    // console.log('Tab đã được quay lại - ' + time);
    log_tab_behavior(time=time, behavior="focus")
});