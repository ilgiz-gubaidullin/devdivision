import sqlalchemy
from sqlalchemy.orm import sessionmaker


class MysqlORMClient:

    def __init__(self, user, password, db_name, host='localhost', port=3307):
        self.user = user
        self.password = password
        self.db_name = db_name

        self.host = host
        self.port = port

        self.engine = None
        self.connection = None
        self.session = None

    def connect(self):
        db = self.db_name
        url = f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{db}'

        self.engine = sqlalchemy.create_engine(url, encoding='utf8')
        self.connection = self.engine.connect()

        sm = sessionmaker(bind=self.connection.engine)  # session creation wrapper
        self.session = sm()

    def execute_query(self, query, fetch=True):
        res = self.connection.execute(query)
        if fetch:
            return res.fetchall()

    def get_metadata(self):
        metadata = sqlalchemy.MetaData(bind=self.engine)
        test_users_table = sqlalchemy.Table('test_users', metadata, autoload=True, autoload_with=self.engine)
        return test_users_table

    def find_in_db_by_username(self, value):
        test_users_table = self.get_metadata()
        query = sqlalchemy.select([test_users_table]).where(test_users_table.columns.username == value)
        return self.execute_query(query)

    def find_in_db_by_email(self, value):
        test_users_table = self.get_metadata()
        query = sqlalchemy.select([test_users_table]).where(test_users_table.columns.email == value)
        return self.execute_query(query)


