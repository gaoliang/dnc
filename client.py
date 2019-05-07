import socketio
from logzero import logger

sio = socketio.Client()


# 1. 连接成功后自动注册设备，data为设备的device_id
@sio.on('connect')
def on_connect():
    sio.emit('register', data='THIS_IS_DEVICE_TWO')


@sio.on('pong')
def handle_pong(data):
    logger.info('pong! it works!')


@sio.on('echo')
def handle_echo(msg):
    logger.info("echo: {}".format(msg))


if __name__ == "__main__":
    sio.connect('http://dnc.leanapp.cn')
    logger.info('sending ping!')
    sio.emit('ping')
