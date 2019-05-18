import socketio

sio = socketio.Client(engineio_logger=True)


@sio.on('connect')
def on_connect():
    print("连接成功")


@sio.on('pong')
def handle_pong(data):
    print('pong! it works!')


if __name__ == "__main__":
    sio.connect('http://47.106.155.88:5000')
    print('sending ping!')
    sio.emit('ping')
