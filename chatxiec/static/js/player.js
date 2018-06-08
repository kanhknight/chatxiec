
// 1. This code loads the IFrame Player API code asynchronously.
var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);


// 2. This function creates an <iframe> (and YouTube player)
//    after the API code downloads.
var player;
function onYouTubeIframeAPIReady() {
    player = new YT.Player('player', {
        height: '390',
        width: '640',
        videoId: 'geKpK_TyH9Y',
        events: {
            'onReady': onPlayerReady
        }
    });
    // document.getElementById('play-pause').onclick = function () {
    //     player.playVideo();
    // };
    // document.getElementById('pause').onclick = function () {
    //     player.pauseVideo();
    // };
}

$(document).ready(
    function(){
        socket_player.emit('connect');
    }
);

// 3. The API will call this function when the video player is ready.
function onPlayerReady(event) {
    var x = 0;
    $('#play-pause').click(function () {
        if (x == 0) {
            socket_player.on('server-send-play-pause', function(data){
                event.target.playVideo();
                x = 1;
            });
            socket_player.emit('client-send-play-pause', event.target.playVideo());
        } else {
            socket_player.on('server-send-play-pause', function(data){
                event.target.pauseVideo();
                x = 0;
            });
            socket_player.emit('client-send-play-pause', event.target.pauseVideo());
        }
    });
}