function Sockets(){
    // Chat Socket default
    this.chat_socket = new WebSocket("ws://" + window.location.host + "/lobby/chat/");

    // Control Socket Default
    this.control_socket = new WebSocket("ws://" + window.location.host + "/lobby/control/");
}

Sockets.prototype.getChatSocket = function(){
    return this.chat_socket;
};

Sockets.prototype.getControlSocket = function(){
    return this.control_socket;
};
