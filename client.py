import socketio
from logzero import logger


class Machine:
    def __init__(self):
        # 每个设备独一无二的ID
        self.device_id = 'Machine_A'

        # 机床程序列表例子
        self.program_list = [
            {'id': 1, 'name': 'program_A', 'desc': 'this is program A'},
            {'id': 2, 'name': 'program_B', 'desc': 'this is program B'},
        ]

        # 机床状态例子
        self.status = {
            'power_on': True,
            'status_A': 'status_A_value',
            'status_B': 'status_B_value',
            'system_params_A': 'system_params_A_value'
        }


machine = Machine()
sio = socketio.Client()


# 1. 连接成功后自动注册设备，参数为设备的device_id
@sio.on('connect')
def on_connect():
    sio.emit('register', machine.device_id)


# 2. 侦听上传程序列表的需求， 监听到后发送程序列表，参数为json，内容为{device_id: string, program_list: []}
@sio.on('need_program_list')
def on_need_program_list(data):
    sio.emit('upload_program_list', {'device_id': machine.device_id, 'program_list': machine.program_list})


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
