// Select all elements with the class 'message_timer'
var message_timers = document.querySelectorAll('.message_timer');

// Loop through all elements and set a timeout to hide them
message_timers.forEach(function(message_timer) {
    setTimeout(function() {
        message_timer.style.display = 'none';
    }, 5000);
});