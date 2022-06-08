import sqlalchemy
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker
from homework7.model import Base


class MysqlORMClient:

    def __init__(self, user, password, db_name, host='localhost', port=3306):
        self.user = user
        self.password = password
        self.db_name = db_name

        self.host = host
        self.port = port

        self.engine = None
        self.connection = None
        self.session = None

    def connect(self, db_created=True):
        db = self.db_name if db_created else ''
        url = f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{db}'

        self.engine = sqlalchemy.create_engine(url, encoding='utf8')
        self.connection = self.engine.connect()

        sm = sessionmaker(bind=self.connection.engine)  # session creation wrapper
        self.session = sm()

    def recreate_db(self):
        self.connect(db_created=False)

        # these two requests we need to do in ras SQL syntax
        self.execute_query(f'DROP database if exists {self.db_name}', fetch=False)
        self.execute_query(f'CREATE database {self.db_name}', fetch=False)

        self.connection.close()

    def execute_query(self, query, fetch=True):
        res = self.connection.execute(query)
        if fetch:
            return res.fetchall()

    def create_methods_amount(self):
        if not inspect(self.engine).has_table('methods_amount'):
            Base.metadata.tables['methods_amount'].create(self.engine)

    def create_10_frequent_request(self):
        if not inspect(self.engine).has_table('top_10_frequent_requests'):
            Base.metadata.tables['top_10_frequent_requests'].create(self.engine)

    def create_5_biggest_request_w_client_error(self):
        if not inspect(self.engine).has_table('5_biggest_request_w_client_error'):
            Base.metadata.tables['5_biggest_request_w_client_error'].create(self.engine)

    def create_5_users_w_server_error_request(self):
        if not inspect(self.engine).has_table('5_users_w_server_error_request'):
            Base.metadata.tables['5_users_w_server_error_request'].create(self.engine)
