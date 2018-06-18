$(document).ready(function () {
    var socket_message = io('http://localhost:3000/message');




    socket_message.on('connect', function () {
        var id = socket_message.io.engine.id;

        socket_message.on('server_sent_count', function (data) {
            $('#number-count').text(data);
        });

        $('#message-input').keypress(function (event) {
            var keycode = (event.keyCode ? event.keyCode : event.which);
            if (keycode == '13') {
                var value = $('#message-input').val();
                var data = {
                    message: value,
                    clientId: id
                }
                if ($('#message-input').val() != '') {
                    socket_message.emit('client-sent-message', data);
                    $('#message-input').val('');
                }
            }
        });

        socket_message.on('server_sent_message', function (data) {
            if (data.clientId != id) {
                $('#message-contain').append(`<div id='message-inside-left' class='d-flex align-items-md-center'>
<img src='http://placehold.it/100x100' class='rounded-circle message-object' height='30' width='30'>
<h4 id='name' class='message-object text-muted'>`+ data.clientId + `</h4>
<div id='message-box' class='message-border'>
<h4 id='message' class='message-object text-white'><span>`+ data.message + `</span></h4>
</div>
</div>`);
                //By jQuery scrollTop
                $("#message-contain").scrollTop($("#message-contain")[0].scrollHeight);

            } else if (data.clientId == id) {
                $('#message-contain').append(`<div id='message-inside-right' class="d-flex align-items-md-center d-flex justify-content-end">
<div id='message-box' class="message-border">
<h4 id='message' class ='message-object rounded text-white'><span>`+ data.message + `</span></h4>
</div>
<img id='host-image' src="http://placehold.it/100x100" class="rounded-circle message-object" alt="" height="30" width="30">
</div>`);
                //By jQuery scrollTop
                $("#message-contain").scrollTop($("#message-contain")[0].scrollHeight);
            }
        });
    });



    // Chọn file tải lên màn hình tạo room
    $('#drop-place').click(function(){
        var filepath = $('#inputGroupFile01').val();
        $('#inputGroupFile01').click();
        console.log(filepath);
        $('#file-selected').append(filepath);
    });
});