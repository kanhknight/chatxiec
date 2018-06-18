var socket_message = io("https://chatxiec888.herokuapp.com/message");
var socket_private_message = io("https://chatxiec888.herokuapp.com/private-mesage");
var socket_player = io("https://chatxiec888.herokuapp.com/player");

$(document).ready(function(){

    // Chọn file tải lên màn hình tạo room
    $('#drop-place').click(function(){
        var filepath = $('#inputGroupFile01').val();
        $('#inputGroupFile01').click();
        console.log(filepath);
        $('#file-selected').append(filepath);
    });
});
