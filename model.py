import peewee as pw

from peewee import SqliteDatabase, Model
from flask_admin.contrib.peewee import ModelView

DATABASE = 'machines.db'
database = SqliteDatabase(DATABASE)


class BaseModel(Model):
    class Meta:
        database = database


class Machine(BaseModel):
    id = pw.AutoField(primary_key=True)
    device_id = pw.CharField(unique=True)
    program_list = pw.TextField(null=True)
    status = pw.TextField(null=True)
    room_id = pw.CharField(max_length=100)
    ip = pw.CharField(max_length=15)


class MachineAdmin(ModelView):
    pass


class Program(BaseModel):
    id = pw.AutoField(primary_key=True)
    name = pw.CharField(max_length=200)
    desc = pw.CharField(max_length=200)
    content = pw.TextField()


def create_tables():
    with database:
        database.create_tables([Program])


if __name__ == "__main__":
    create_tables()
