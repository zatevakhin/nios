// $(document).ready(function() {
//     if (!window.WebSocket) {
//         if (window.MozWebSocket) {
//             window.WebSocket = window.MozWebSocket;
//         } else {
//             $('#messages').append("<li>Your browser doesn't support WebSockets.</li>");
//         }
//     }
//     ws = new WebSocket('ws://127.0.0.1:8080/websocket');
//     ws.onopen = function(evt) {
//         $('#messages').append('<li>WebSocket connection opened.</li>');
//     }
//     ws.onmessage = function(evt) {
//         $('#messages').append('<li>' + evt.data + '</li>');
//     }
//     ws.onclose = function(evt) {
//         $('#messages').append('<li>WebSocket connection closed.</li>');
//     }
//     $('#send').submit(function() {
//         ws.send($('input:first').val());
//         $('input:first').val('').focus();
//         return false;
//     });
// });