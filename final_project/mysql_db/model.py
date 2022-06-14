from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Test_users(Base):

    __tablename__ = 'test_users'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<Test_users(" \
               f"id='{self.id}'," \
               f"name='{self.name}', " \
               f"surname='{self.surname}', " \
               f"middle_name='{self.middle_name}', " \
               f"username='{self.username}', " \
               f"password='{self.password}', " \
               f"email='{self.email}', " \
               f"access='{self.access}', " \
               f"active='{self.active}', " \
               f"start_active_time='{self.start_active_time}'" \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(255), nullable=False)
    surname = Column(String(255), nullable=False)
    middle_name = Column(String(255), nullable=True)
    username = Column(String(16), nullable=True, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(64), nullable=False, unique=True)
    access = Column(Integer, nullable=True)
    active = Column(Integer, nullable=True)
    start_active_time = Column(Date, nullable=True)
