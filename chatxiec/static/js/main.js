var socket_message = io("http://localhost:3000/message");

$(document).ready(function(){
    $('#text-message').keypress(function(event){
        var keycode = (event.keyCode ? event.keyCode: event.which);
        if(keycode == '13'){
            if ($('#text-message').val() != ""){
                socket_message.emit('Client-send-message', $('#text-message').val());
                $('#text-message').val('');
            }
                        
        }
    });

    socket_message.on('Server-send-message', function(data){
        $('#message-container').append('<li>'+ data + '</li>')
    });

});
