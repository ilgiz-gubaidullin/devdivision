import pytest
from homework7.base import MysqlBase
from collections import Counter
from homework7.model import *


class TestMysqlCreate(MysqlBase):

    @pytest.mark.DB
    def test_get_rows_amount(self):
        count = sum(1 for line in self.logfile)
        assert count == 225133

    @pytest.mark.DB
    def test_methods_amount(self):
        methods_list = []
        for line in self.logfile:
            log_str = line.split()
            methods_list.append(log_str[5])
        s = Counter(methods_list)

        self.mysql.create_methods_amount()
        for k, v in s.items():
            method = Methods(method=k, quantity=v)
            self.mysql.session.add(method)
            self.mysql.session.commit()

    @pytest.mark.DB
    def test_top_ten_requests(self):
        requests_list = []
        for line in self.logfile:
            log_str = line.split()
            requests_list.append(log_str[6])
        s = Counter(requests_list).most_common(10)

        self.mysql.create_10_frequent_request()
        for i in s:
            request = FrequentRequests(request=i[0], quantity=i[1])
            self.mysql.session.add(request)
            self.mysql.session.commit()

    @pytest.mark.DB
    def test_top_five_big_req_w_client_err(self):
        requests_list_w_client_err = []
        for line in self.logfile:
            log_str = line.split()
            if log_str[8].startswith('4'):
                requests_list_w_client_err.append(log_str)
        sorted_list = (sorted(requests_list_w_client_err, key=lambda i: int(i[9]), reverse=True))

        self.mysql.create_5_biggest_request_w_client_error()
        for n in sorted_list[0:5]:
            request_list = ClientErrorRequests(
                user=n[0],
                request=n[6],
                status_code=n[8],
                size=n[9])
            self.mysql.session.add(request_list)
            self.mysql.session.commit()

    @pytest.mark.DB
    def test_top_five_user_w_server_err(self):
        users_list = []
        for line in self.logfile:
            log_str = line.split()
            if log_str[8].startswith('5'):
                users_list.append(log_str[0])
        s = Counter(users_list).most_common(5)

        self.mysql.create_5_users_w_server_error_request()
        for i in s:
            user = ServerErrorUsers(user=i[0], quantity=i[1])
            self.mysql.session.add(user)
            self.mysql.session.commit()
