from peewee import *
# db = SqliteDatabase("foobar.db")
from playhouse.pool import PooledMySQLDatabase

db = PooledMySQLDatabase(
    "xfl_mybigdata",
    user="root",
    password="xflisthebest110",
    charset="utf8mb4",
    max_connections=32
)


def class_generator(class_name, value_dict: dict):
    def get_table_name(model_class):
        return model_class.__name__

    value_dict['Meta'] = type('Meta', (object,), {'database': db, 'table_function': get_table_name})
    return type(class_name, (Model,), value_dict)


if __name__ == "__main__":
    dataFoo = class_generator("foo", {
        "lalala": CharField(null=True)
    })

    db.create_tables([dataFoo])
    # db.drop_tables([dataFoo, dataBar])
