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
        if(data.action == "lobby_change"){
            lobby.getData();
        }
    };

    // on start click
    $('#start-button').click(function(e){
        if (sockets.getControlSocket().readyState == WebSocket.OPEN) {
            sockets.getControlSocket().send('start')
        }
    });
});

var lobby = new Vue({
    delimiters: ["[[", "]]"],
    el: '#lobby',
    data: {
        lobby_data: null
    },
    mounted: function(){
        console.log('in mount');
        this.getData();
    },
    methods:{
        getData: function(){
            console.log('getting data');
            var scope = this;
            $.getJSON("data/", function(data, textStatus, jqXHR){
                console.log('data', data);
                window.data = data;
                scope.lobby_data = data;
            });
        }
    }
});

window.lobby = lobby;
