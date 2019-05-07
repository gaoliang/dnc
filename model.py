import leancloud


# 可以用继承的方式定义 leancloud.Object 的子类
class Machine(leancloud.Object):
    @property
    def room_id(self):
        return self.get('room_id')

    @classmethod
    def get_room_id_by_device_id(cls, device_id):
        cls.query.equal_to('device_id', device_id)
        machine = cls.query.find()[0]
        return machine.room_id
