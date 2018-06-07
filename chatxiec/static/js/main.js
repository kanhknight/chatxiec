var socket_message = io("http://localhost:3000/message");

$(document).ready(function(){

    // Hàm gửi tin nhắn cho server
    $('#text-message').keypress(function(event){
        var keycode = (event.keyCode ? event.keyCode: event.which);
        if(keycode == '13'){
            if ($('#text-message').val() != ""){
                socket_message.emit('Client-send-message', $('#text-message').val());
                $('#text-message').val('');
            }
        }
    });

    // Nhận tin nhắn server gửi vể
    socket_message.on('Server-send-message', function(data){
        $('#message-container').append('<li>'+ data + '</li>')
    });

});
