document.addEventListener('DOMContentLoaded', function() {
    var socket = new WebSocket(`ws://localhost:8000/ws/notify/`)

    socket.onopen = function(e) {
        console.log("Connection established")
    }

    socket.onmessage = function(e) {
        var data = JSON.parse(e.data)
        setTimeout(function() {
            var audio = new Audio('/media/notify_sound/Ivory.mp3')
            audio.volume = 0.3
            audio.play()
        }, 50)

        $.notify(
            data.message,
            { 
                className: "info",         
                autoHideDelay: 10000,      
                position: "bottom right"   
            }
        )
    }

    socket.onclose = function(e) {
        console.log("Connection closed")
    }
})