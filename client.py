import json

import socketio
from logzero import logger

from utils import decrypt


class Machine:
    """
    这里模拟了一个机床，数据是我编造的。格式也是我随便定的
    """

    def __init__(self):
        # 每个设备独一无二的ID
        self.device_id = 'ttt'

        # 机床程序列表例子
        self.program_list = [
            {'id': 1, 'name': 'program_A', 'desc': 'this is program A', 'content': 'content A'},
            {'id': 2, 'name': 'program_B', 'desc': 'this is program B', 'content': 'content B'},
        ]

        # 加密配置
        self.key = '1234123412ABCDEF'
        self.iv = 'ABCDEF1234123412'

        # 机床状态例子
        self.status = {
            'power_on': True,
            'status_A': 'status_A_value',
            'status_B': 'status_B_value',
            'system_params_A': 'system_params_A_value'
        }


machine = Machine()
sio = socketio.Client(engineio_logger=True)


def callback_register(data):
    print(data)


# 1. 连接成功后自动注册设备，参数为设备的device_id
@sio.on('connect')
def on_connect():
    sio.emit('register', machine.device_id, callback=callback_register)


# 2. 侦听上传程序列表的需求， 监听到后发送程序列表，参数为json，内容为{device_id: string, program_list: []}
@sio.on('need_program_list')
def on_need_program_list(data):
    logger.info("server need program list! uploading program list")
    sio.emit('upload_program_list', {'device_id': machine.device_id, 'program_list': machine.program_list})


# 3. 监听删除程序的需求， 监听到后删除指定id的程序
@sio.on('delete_program')
def on_delete_program(program_id):
    program_id = int(program_id)
    for index, program in enumerate(machine.program_list):
        if program.get('id') == program_id:
            machine.program_list.pop(index)
            print(machine.program_list)
            break
    sio.emit('upload_program_list', {'device_id': machine.device_id, 'program_list': machine.program_list})


# 4. 监听下发程序的需求，触发后自动保存程序到当前程序列表，如果id相同则更新
@sio.on('download_program')
def on_download_program(data):
    encrypted_data = data.get('encrypted_data')
    download_program = json.loads(decrypt(machine.key, machine.iv, encrypted_data))
    logger.info('download program : {}'.format(download_program))
    program_id = download_program.get('id')
    for program in machine.program_list:
        # 有同id的程序在，则更新
        if program['id'] == program_id:
            program['content'] = download_program['content']
            program['name'] = download_program['name']
            program['desc'] = download_program['desc']
            sio.emit('upload_program_list', machine.program_list)
            return
    machine.program_list.extend(download_program)


@sio.on('pong')
def handle_pong(data):
    logger.info('pong! it works!')


@sio.on('echo')
def handle_echo(msg):
    logger.info("echo: {}".format(msg))


if __name__ == "__main__":
    sio.connect('http://47.106.155.88:5000')
    logger.info('sending ping!')
    sio.emit('ping')
