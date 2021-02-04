window.onload = function () {
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function () {
    };
    var send_input = document.querySelector("#send_input")
    var send_button = document.querySelector('#send_button')
    document.onkeydown = function (event) {
        console.log('css')
        var event = event || window.event;
        var key = event.which || event.keyCode || event.charCode;
        if (key == 13) {
            /*Do something. 调用一些方法*/
            newMessage(send_input.value)
            send_input.value = ''
        }

    }
    send_button.addEventListener('click', function () {
        console.log('发送消息', send_input.value)
        newMessage(send_input.value)
        send_input.value = ''

    })

    updater.start();
    var showmessage = document.querySelector('.show_message')
    showmessage.scrollTop = showmessage.scrollHeight
};

function newMessage(text) {

    updater.socket.send(text);

}

var updater = {
    socket: null,

    start: function () {
        var url = "ws://" + location.host + "/chatsocket";
        updater.socket = new WebSocket(url);
        updater.socket.onmessage = function (event) {
            updater.showMessage(JSON.parse(event.data));
        }
    },

    showMessage: function (message) {
        var showmessage = document.querySelector('.show_message')
        var message_text = message.text
        var message_time = message.time
        console.log('message;', message)
        console.log('text', message_text)
        console.log('time', message_time)

        var temp_message = '<div class="message">' + message_text + '<small>' + message_time + '</small></div>'
        showmessage.innerHTML = showmessage.innerHTML + temp_message
        showmessage.scrollTop = showmessage.scrollHeight

    }
};