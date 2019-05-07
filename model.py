import leancloud


# 可以用继承的方式定义 leancloud.Object 的子类
class Machine(leancloud.Object):
    @property
    def room_id(self):
        return self.get('room_id')
