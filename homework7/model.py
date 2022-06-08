from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Methods(Base):
    __tablename__ = 'methods_amount'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<Methods(" \
               f"id='{self.id}'," \
               f"method='{self.method}', " \
               f"quantity='{self.quantity}'" \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    method = Column(String(300))
    quantity = Column(Integer)


class FrequentRequests(Base):
    __tablename__ = 'top_10_frequent_requests'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<Requests(" \
               f"id='{self.id}'," \
               f"request='{self.request}', " \
               f"quantity='{self.quantity}'" \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    request = Column(String(300))
    quantity = Column(Integer)


class ClientErrorRequests(Base):
    __tablename__ = '5_biggest_request_w_client_error'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<Requests(" \
               f"id='{self.id}'," \
               f"user='{self.user}', " \
               f"request='{self.request}', " \
               f"status_code='{self.status_code}', " \
               f"size='{self.size}'" \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(String(300))
    request = Column(String(300))
    status_code = Column(Integer)
    size = Column(Integer)


class ServerErrorUsers(Base):
    __tablename__ = '5_users_w_server_error_request'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<Requests(" \
               f"id='{self.id}'," \
               f"user='{self.user}', " \
               f"quantity='{self.quantity}'" \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(String(300))
    quantity = Column(Integer)
