import json

from flask import Flask, request, jsonify
from flask_admin import Admin
from flask_cors import CORS
from flask_socketio import SocketIO
from logzero import logger
from playhouse.shortcuts import model_to_dict, dict_to_model

from model import Machine, MachineAdmin, Program
from utils import encrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
admin = Admin(app, name='dnc_admin', template_mode='bootstrap3')
admin.add_view(MachineAdmin(Machine))
socketio = SocketIO(app, engineio_logger=True)
CORS(app)


@socketio.on('register')
def handle_register(device_id):
    """
    注册设备，并记录设备的room_id，以保证可以和设备进行单独通信
    :param device_id:
    :return: a json string
    """
    machine = Machine.select().where(Machine.device_id == device_id).first()
    if not machine:
        machine = Machine()
        machine.device_id = device_id
        logger.info('register new device: {} from {}'.format(device_id, request.remote_addr))
    machine.ip = request.remote_addr
    machine.room_id = request.sid
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
    update = Machine.update(status=json.dumps(status)).where(Machine.device_id == device_id)
    update.execute()


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
    update = Machine.update(program_list=json.dumps(program_list)).where(Machine.device_id == device_id)
    update.execute()


@socketio.on('disconnect')
def handle_disconnect(data):
    room_id = request.sid
    machine = Machine.select().where(Machine.room_id == room_id).get()
    machine.status


# 下面是http接口，用于桌面端调用

@app.route('/download_program', methods=['POST'])
def download_program():
    """
    下载程序到设指定设备
    :return:
    """
    data = request.get_json()
    room_id = data.get('room_id')
    program_id = data.get('program_id')
    key = data.get('key')
    iv = data.get('iv')
    program = Program.select().where(Program.id == program_id).get()
    program_data = json.dumps(model_to_dict(program))
    encrypted_data = encrypt(key, iv, program_data)
    socketio.emit('download_program', {'encrypted_data': encrypted_data}, room=room_id)
    return jsonify({'success': True})


@socketio.on('ping')
def handle_ping():
    socketio.emit('pong')


@app.route('/need_program_list/<room_id>')
def get_program_list(room_id):
    socketio.emit('need_program_list', room=room_id)
    return jsonify({'success': True})


@app.route('/get_machine_by_room_id/<room_id>')
def get_machine_by_room_id(room_id):
    machine = Machine.select().where(Machine.room_id == room_id).get()
    return jsonify(model_to_dict(machine))


@app.route('/delete_program/<room_id>/<program_id>')
def test_delete_program(room_id, program_id):
    socketio.emit('delete_program', program_id, room=room_id)
    return jsonify({'success': True})


@app.route('/test_room/<room_id>')
def send(room_id):
    socketio.emit('echo', 'hello, {}'.format(room_id), room=room_id)
    return jsonify({'success': True})


@app.route('/pong')
def pong():
    socketio.emit('pong')
    return jsonify({'success': True})


@app.route('/stop')
def stop():
    socketio.stop()
    return 'ok', 200


@app.route('/list_machines')
def list_machines():
    machines = Machine.select()
    return jsonify([model_to_dict(machine) for machine in machines])


@app.route('/list_programs')
def list_programs():
    programs = Program.select()
    return jsonify([model_to_dict(program) for program in programs])


@app.route('/delete_program/<program_id>')
def delete_program(program_id):
    Program.delete_by_id(program_id).execute()
    return jsonify({'success': True})


@app.route('/add_program', methods=['POST'])
def add_program():
    program = dict_to_model(Program, request.json)
    program.save()
    return jsonify({'success': True})


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')
