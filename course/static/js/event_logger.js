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
    time = new Date();
    console.log('Tab đã bị chuyển đi - ' + time);
    log_tab_behavior(time=time, behave="blur")
});

window.addEventListener('focus', () => {
    time = new Date();
    console.log('Tab đã được quay lại - ' + time);
    log_tab_behavior(time=time, behave="focus")
});

// window.onbeforeunload = function() {
//     document.querySelector("#submit").click();
//     console.log("hahaha");
//     return "Bạn có chắc chắn muốn rời khỏi trang này?";
// };
