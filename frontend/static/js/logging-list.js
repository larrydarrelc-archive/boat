(function() {
    var $ = function(selector) {
        return document.querySelector(selector);
    };

    var tmpl = function (markup, data) {
            var pattern = /<%=([\w ]+)%>/g,
                key;

            while ((key = pattern.exec(markup)) !== null) {
                markup = markup.replace(key[0], data[key[1].trim()]);
            }

            return markup;
        };


    var list = $('.logging-list__items'),
        itemTmpl = $('.logging-list__items__item-tmpl').innerHTML;

    var ws = new WebSocket('ws://127.0.0.1:1235/client');

    ws.onopen = function (e) {
        console.log('Connection established.');

        window.setInterval(function (e) {
            console.log('Polling logging records.');
            ws.send('logging-poll:');
        }, 3000);
    };

    ws.onmessage = function (e) {
        var message = JSON.parse(e.data);

        console.log('New message received.', e.data);

        if (message.event === 'logging') {
            console.log('New logging record arrived.');
            list.innerHTML = list.innerHTML + tmpl(itemTmpl, message.data);
        }

        if (message.event === 'logging-poll') {
            var records = message.data,
                content = '';

            for (var i = 0; i < records.length; i++) {
                content = content + tmpl(itemTmpl, message.data);
            }
            list.innerHTML = content;
        }
    };

    ws.onclose = function (e) {
        console.log('Connection closed.');
    };
})();
