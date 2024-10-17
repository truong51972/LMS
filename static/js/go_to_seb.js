const seb_link = document.getElementById('start_assign_btn').getAttribute("sebLink");
const hostname = window.location.hostname
document.getElementById('start_assign_btn').addEventListener('click', function() {
    window.location.href = `seb://${hostname}${seb_link}`;
});