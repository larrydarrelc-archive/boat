(function() {
    var container = document.querySelector('.main'),
        eventName = document.querySelector('input[name="control__event-name"]'),
        eventData = document.querySelector('input[name="control__event-data"]'),
        controlBtn = document.querySelector('button.control__submit');

    var ws = new WebSocket('ws://127.0.0.1:1235/client');

    ws.onopen = function (e) {
        console.log('Connection established.');

        window.setInterval(function (e) {
            ws.send('hello:foobar');
        }, 3000);
    };

    ws.onmessage = function (e) {
        container.innerHTML += '<p>' + e.data + '</p>';
    };

    ws.onclose = function (e) {
        container.innerHTML += '<p>Connection closed.</p>';
    };

    controlBtn.onclick = function (e) {
        ws.send(eventName.value + ':' + eventData.value);
        eventName.value = eventData.value = '';
    };
})();
