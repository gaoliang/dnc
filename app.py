from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from logzero import logger

from model import Machine

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@socketio.on('register')
def handle_register(device_id):
    """
    注册设备，并记录设备的room_id，以保证可以和设备进行单独通信
    :param device_id:
    :return: a json string
    """
    query = Machine.query
    query.equal_to('device_id', device_id)
    query_list = query.find()
    if query_list:
        machine = query_list[0]
        logger.info('update device {} ip to {}'.format(device_id, request.remote_addr))
    else:
        machine = Machine()
        machine.set('device_id', device_id)
        logger.info('register new device: {} from {}'.format(device_id, request.remote_addr))
    machine.set('ip', request.remote_addr)
    machine.set('room_id', request.sid)
    machine.save()
    return {
        'success': True,
        'message': 'register successful!'
    }


@socketio.on('refresh_status')
def handle_refresh(data):
    """
    设备主动上报状态
    :return:
    """
    device_id = data.get('device_id')
    status = data.get('status')
    logger.info("收到来自device_id: {} 的机床状态更新， 内容为 {}".format(device_id, status))
    Machine.query.equal_to('device_id', device_id)
    machine = Machine.query.find()[0]
    machine.set('status', status)
    machine.save()


@socketio.on('upload_program_list')
def handle_upload_program_list(data):
    """
    接收来自设备上报的设备程序列表
    :param data: 包含program_list和device_id的json dict
    :return:
    """
    device_id = data.get('device_id')
    program_list = data.get('program_list')
    logger.info("收到来自device_id: {} 的程序列表， 内容为 {}".format(device_id, program_list))
    Machine.query.equal_to('device_id', device_id)
    machine = Machine.query.find()[0]
    machine.set('program_list', program_list)
    machine.save()


@app.route('/stop')
def stop():
    socketio.stop()
    return 'ok', 200


@socketio.on('ping')
def handle_ping():
    socketio.emit('pong')


@app.route('/download')
def download_test():
    socketio.emit('download', {'program_id': 1001, 'content': {'data_section_1': 'xxxx'}})
    return '', 200


@app.route('/need_program_list/<room_id>')
def get_program_list(room_id):
    socketio.emit('need_program_list', room_id=room_id)
    return jsonify({'success': True})


@app.route('/need_program_list_by_device_id/<device_id>')
def get_program_list_by_device_id(device_id):
    room_id = Machine.get_room_id_by_device_id(device_id)
    return get_program_list(room_id)


@app.route('/delete_program')
def test_delete_program():
    socketio.emit('delete_program', 1001, callback=lambda x: print(x))
    return jsonify({'success': True})


@app.route('/all_data')
def get_all_data():
    query = Machine.query
    return jsonify(query.find())


@app.route('/test_room/<room_id>')
def send(room_id):
    socketio.emit('echo', 'hello, {}'.format(room_id), room=room_id)
    return jsonify({'success': True})


if __name__ == '__main__':
    socketio.run(app, debug=True)
