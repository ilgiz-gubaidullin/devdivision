class SiteData:

    # Использую эти наружные подключения при дебаге тестов
    # url = "http://127.0.0.1:8082/"
    # vk_url = "http://127.0.0.1:8005/"
    # db_host = 'localhost'
    # port = 3307

    # Внутри docker сети
    url = "http://my-cool-app:8082/"
    vk_url = "http://vk_api:8005/"
    db_host = 'mysql_db_container'
    port = 3306

    main_user = "main_user"
    main_user_pass = "password"

    test_cases = "https://docs.google.com/spreadsheets/d/1dZTGr1vcxKbGGx-0hitCPwRqLdQXRqxZPMwCmAewVMI/edit#gid=0"


class MainPageLinks:
    container_links = [
        "https://en.wikipedia.org/wiki/Application_programming_interface",
        "https://www.popularmechanics.com/technology/infrastructure/a29666802/future-of-the-internet/",
        "https://ru.wikipedia.org/wiki/SMTP"]
    header_links = [
        "https://en.wikipedia.org/wiki/History_of_Python",
        "https://flask.palletsprojects.com/en/1.1.x/#",
        "https://www.wireshark.org/news/",
        "https://www.wireshark.org/#download",
        "https://hackertarget.com/tcpdump-examples/"
    ]