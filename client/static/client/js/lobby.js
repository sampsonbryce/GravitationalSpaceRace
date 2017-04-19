var sockets = new Sockets();
$(function(){
    // set get message
    sockets.getChatSocket().onmessage = function(e) {
        console.log('e', e);
        var el = $('<p></p>').text(e.data).addClass('message');
        $('#messages').append(el);
    };

    // send on enter
    $('#message-input').keyup(function(e){
        if(e.keyCode == 13){
            if (sockets.getChatSocket().readyState == WebSocket.OPEN) {
                sockets.getChatSocket().send($(this).val());
            }
        }
    });

    sockets.getControlSocket().onmessage = function(e){
        console.log('control socket', e);
        var data = JSON.parse(e.data);
        if(data.action == "start"){
            window.location.href = "/client"
        }
        if(data.action == "user_join"){
            //reload
        }
    };

    // on start click
    $('#start-button').click(function(e){
        if (sockets.getControlSocket().readyState == WebSocket.OPEN) {
            sockets.getControlSocket().send('start')
        }
    });
});