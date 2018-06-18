$(document).ready(function () {
    var pathname = window.location.pathname; 
    var parts = pathname.split("/");
    var last_part = parts[parts.length-1];

    var room_url = `https://chatxiec888.herokuapp.com/chatroom`;

    var room_socket = io(room_url);

    room_socket.emit('joinroom', last_part);

    room_socket.on('server_send_noti_to_user_join_room', function(data){
        console.log(data);
    });


    var currentdate = new Date(); 
    var datetime = "Now: " + currentdate.getDate() + "/"
                + (currentdate.getMonth()+1)  + "/" 
                + currentdate.getFullYear() + " @ "  
                + currentdate.getHours() + ":"  
                + currentdate.getMinutes() + ":" 
                + currentdate.getSeconds();

    room_socket.on('connect', function () {
        var id = socket_message.io.engine.id;

        $('#message-input').keypress(function (event) {
            var keycode = (event.keyCode ? event.keyCode : event.which);
            if (keycode == '13') {
                var value = $('#message-input').val();
                var data = {
                    userid: id,
                    message: value,
                    date : datetime,
                    roomid: last_part
                }

                if ($('#message-input').val() != '') {
                    room_socket.emit('client_sent_message_to_room', data);
                    $('#message-input').val('');
                }
            }
        });

        room_socket.on('server_sent_message_to_room', function (data) {
            if (data.clientid != id) {
                $('#message-contain').append(`<div id='message-inside-left' class='d-flex align-items-md-center'>
<img src='http://placehold.it/100x100' class='rounded-circle message-object' height='30' width='30'>
<h4 id='name' class='message-object text-muted'>`+ data.username + `</h4>
<div id='message-box' class='message-border'>
<h4 id='message' class='message-object text-white'><span>`+ data.message + `</span></h4>
</div>
</div>`);
                //By jQuery scrollTop
                $("#message-contain").scrollTop($("#message-contain")[0].scrollHeight);

            } else if (data.clientid == id) {
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

  });