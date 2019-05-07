import socketio
from logzero import logger

sio = socketio.Client()


@sio.on('connect')
def on_connect():
    sio.emit('register', data={'hello': 'world'})


@sio.on('pong')
def handle_pong(data):
    logger.info('pong! it works!')


if __name__ == "__main__":
    sio.connect('http://127.0.0.1:5000')
    logger.info('sending ping!')
    sio.emit('ping')
