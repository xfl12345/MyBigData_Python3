import sqlalchemy
from sqlalchemy import MetaData
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import registry
from mybigdata.src.main.model.conf.app_config import APP_CONFIG

# mapper_registry = registry()
#
# Base = mapper_registry.generate_base()

Base = declarative_base()
Base.metadata = MetaData()

# class StringContent(Base):
#     # __tablename__ = "string_content"
#     __tablename__ = APP_CONFIG.CORE_TABLE_NAME.string_type
#     global_id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True)
#     data_format = sqlalchemy.Column(sqlalchemy.BigInteger)
#     content_length = sqlalchemy.Column(sqlalchemy.SmallInteger)
#     content = sqlalchemy.Column(sqlalchemy.VARCHAR)
#
#
# stmt = sqlalchemy.select(StringContent).where(StringContent.content == 'text')
# print(stmt.compile(dialect=mysql.dialect(), compile_kwargs={"literal_binds": True}))




class_name = 'StringContent'
bases = (Base,)
class_dict = {
    "__tablename__": "string_content222",
    "global_id" : sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True),
    "data_format" : sqlalchemy.Column(sqlalchemy.BigInteger),
    "content_length" : sqlalchemy.Column(sqlalchemy.SmallInteger),
    "content" : sqlalchemy.Column(sqlalchemy.VARCHAR)
}
StringContent = type(class_name, bases, class_dict)
print(StringContent.__dict__)



# 允许热修改类的结构，避免重启APP
def change_tablename(tablename: str):
    global class_dict, StringContent, mapper_registry
    # mapper_registry.dispose(cascade=True)
    class_dict["__tablename__"] =  tablename
    StringContent = type(class_name, bases, class_dict)



stmt = sqlalchemy.select(StringContent).where(StringContent.content == 'text')
print(stmt.compile(dialect=mysql.dialect(), compile_kwargs={"literal_binds": True}))


Base.metadata.clear()
sqlalchemy.orm.clear_mappers()

change_tablename("string_content")
# APP_CONFIG.CORE_TABLE_NAME.string_type = "xfl666"

stmt = sqlalchemy.select(StringContent).where(StringContent.content == 'text')
print(stmt.compile(dialect=mysql.dialect(), compile_kwargs={"literal_binds": True}))

# sc = StringContent()

# t = table("my_table", column("content"), column("global_id"))
# print(t.select().compile(dialect=mysql.dialect()))
