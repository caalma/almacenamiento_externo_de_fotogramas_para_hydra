let hydra = new Hydra({canvas: window.soporte, detectAudio: false}),
    capture_fps,
    video_fps,
    format_frame,
    quality_frame,
    video_name,
    server_host,
    server_port,
    sendInterval;


function sendFrame() {
    hydra.getScreenImageNDL(blob => {
        if (socket.readyState === WebSocket.OPEN) {
            socket.send(blob);
        }
    }, format_frame, quality_frame);
}


function startStream() {
    socket = new WebSocket(`ws://${server_host}:${server_port}`);
    socket.addEventListener('open', () => {
        socket.send(JSON.stringify({
            format: format_frame,
            fps: video_fps,
            filename: video_name
        }));
    });
    clearInterval(sendInterval);
    sendInterval = setInterval(() => {
        sendFrame();
    }, 1000 / video_fps);
}


function stopStream() {
    if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({ action: 'done' }));
        socket.close();
    }
    clearInterval(sendInterval);
}


function capturar(width=333, height=333, cfps=12, vfps=12, vname='video_00', format='jpeg', quality=0.95){
    if(format == 'jpg'){ format = 'jpeg'; }
    capture_fps = cfps;
    video_fps = vfps;
    video_name = vname;
    format_frame = format;
    jpeg_quality = quality;
    setResolution(width, height);
    startStream();
}


function finalizar(reload=false){
    stopStream();
    if(reload === true){
        window.location.reload();
    }
}


function server(host='localhost', port='9009'){
    server_host = host;
    server_port = port;
}

server();
setResolution(333, 333);
speed = 0.5;
osc(4, 0.1, 1.2).rotate(0, 0.3).out();
