from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


# todo 利用room机制实现对机床的单独消息发送

@socketio.on('register')
def handle_register(device_id):
    """
    注册新设备
    :param device_id:
    :return: a json string
    """
    print('register device: {}'.format(device_id))
    return {
        'success': True,
        'message': 'register successful!'
    }


@socketio.on('upload')
def handle_upload(device_id, data):
    """
    设备主动上传数据到dnc
    :param device_id
    :param data, a dict with machine data
    :return: a json string
    """
    print("收到来自device_id: {} 的数据， 内容为 {}".format(device_id, data))

    return {
        'success': True,
        'message': 'receive data successfully'
    }


@socketio.on('refresh_status')
def handle_refresh(device_id, data):
    """
    设备主动上报状态
    :param device_id:
    :param data: 具体结构需要定义
    :return:
    """
    print("收到来自device_id: {} 的机床状态更新， 内容为 {}".format(device_id, data))


@socketio.on('upload_program_list')
def handle_upload_program_list(device_id, program_list):
    """
    接收来自设备上报的设备程序列表
    :param device_id:
    :param program_list:
    :return:
    """
    print("收到来自device_id: {} 的程序列表， 内容为 {}".format(device_id, program_list))


@app.route('/stop')
def stop():
    socketio.stop()


@app.route('/download')
def download_test():
    socketio.emit('download', {'program_id': 1001, 'content': {'data_section_1': 'xxxx'}})
    return '', 200


@app.route('/need_program_list')
def get_program_list():
    socketio.emit('need_program_list')
    return "ok", 200


@app.route('/delete_program')
def test_delete_program():
    socketio.emit('delete_program', 1001, callback=lambda x: print(x))
    return 'ok', 200


if __name__ == '__main__':
    socketio.run(app, debug=True)