function resizeHeader() {
    var w = document.documentElement.clientWidth;
    var h = document.documentElement.clientHeight;
    var link = document.getElementsByClassName("nav_links")[0]
    var rightContainerbtns = document.getElementsByClassName("right")[0];
    var burger = document.getElementsByClassName("right-burger")[0]
    if (w < 945) {

        link.style.display = "none"

        rightContainerbtns.style.display = "none"
        burger.style.display = "block"

    } else {

        link.style.display = "block"

        rightContainerbtns.style.display = "block"

        burger.style.display = "none"

    }


}

function openNav() {
    document.getElementById("myNav").style.height = "100%";
    document.getElementById("myNav").style.width = "100%";
}

/* Close */
function closeNav() {
    document.getElementById("myNav").style.height = "0%";
}


function countDownTimer(daysEle, hoursEle, minsEle, secsEle, date, state) {
    var countDownDate = new Date(date).getTime();

    if (state == "awaiting") {
        document.getElementById(daysEle).innerHTML = "closed"
        document.getElementById(hoursEle).innerHTML = "closed"
        document.getElementById(minsEle).innerHTML = "closed"
        document.getElementById(secsEle).innerHTML = "closed"
        return;

    }


    // Update the count down every 1 second
    var x = setInterval(function () { // Get today's date and time
        var now = new Date().getTime();

        // Find the distance between now and the count down date
        var distance = countDownDate - now;

        // Time calculations for days, hours, minutes and seconds
        var days = Math.floor(distance / (1000 * 60 * 60 * 24));
        var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((distance % (1000 * 60)) / 1000);

        // Display the result in the element with id="demo"
        document.getElementById(daysEle).innerHTML = "<b>" + days + "<br>days</b> "
        document.getElementById(hoursEle).innerHTML = "<b>" + hours + "<br>hours</b> "
        document.getElementById(minsEle).innerHTML = "<b>" + minutes + "<br>mins</b> "
        document.getElementById(secsEle).innerHTML = "<b>" + seconds + "<br>secs </b>"


        // If the count down is finished, write some text
        if (distance < 0) {
            clearInterval(x);
            document.getElementById(daysEle).innerHTML = 0 + "<br>days "
            document.getElementById(hoursEle).innerHTML = 0 + "<br>hours "
            document.getElementById(minsEle).innerHTML = 0 + "<br>mins "
            document.getElementById(secsEle).innerHTML = 0 + "<br>seconds "
        }
    }, 1000);

}

function setPercentageRaffleCompletion() {
    var elements = document.getElementsByClassName("progress-bar")
    for (i = 0; i < elements.length; i ++) {
        var currentVal = elements[i].getAttribute('aria-valuenow')
        var ticketLimit = elements[i].getAttribute('aria-valuemax')
        var percent = (currentVal / ticketLimit) * 100
        if (percent > 100) { // checks to see if entry is not greater than 100 from postal entries.
            elements[i].style.width = 100 + "%"
            elements[i].innerHTML = 100 + "% sold"
        }
        else if (percent > 20) {
            elements[i].style.width = percent + "%"
            elements[i].innerHTML = Math.round(percent) + "% sold"

        } else {
            elements[i].style.width = 20 + "%"
            elements[i].innerHTML = Math.round(percent) + "% sold"
        }


    }
}


function getCurrentYear() {
    return new Date().getFullYear();
}

function setFooterDate() {
    document.getElementById("footer-date").innerHTML = "©" + getCurrentYear() + " Copyright:";
}
