
document.addEventListener("DOMContentLoaded", function () {
    let timeLeft = 10;

    const countdown = document.getElementById("countdown");

    const timer = setInterval(function () {
        timeLeft--;

        countdown.textContent = timeLeft;

        if (timeLeft <= 0) {
            clearInterval(timer);
            window.location.href = "/";
        }
    }, 1000);
});
