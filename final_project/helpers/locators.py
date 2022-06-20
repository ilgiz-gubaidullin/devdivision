class LoginPageLocators:

    USERNAME_INPUT = "[name='username']"
    PASSWORD_INPUT = "[name='password']"
    SUBMIT = "[name='submit']"

    CREATE_ACCOUNT = "[href='/reg']"


class MainPageLocators:

    LOGGED_NAME = '#login-name li:first-child'

    WHAT_IS_API_ICON = "[src='/static/images/laptop.png']"
    INTERNET_FUTURE_ICON = "[src='/static/images/loupe.png']"
    SMTP_ICON = "[src='/static/images/analytics.png']"

    PYTHON_HOVER = "[href='https://www.python.org/']"
    PYTHON_HISTORY = "[href='https://en.wikipedia.org/wiki/History_of_Python']"
    ABOUT_FLASK = "[href='https://flask.palletsprojects.com/en/1.1.x/#']"

    LINUX_HOVER = "header > nav > ul > li:nth-child(4) > a"
    DOWNLOAD_CENTOS = "[href='https://getfedora.org/ru/workstation/download/']"

    NETWORK_HOVER = "header > nav > ul > li:nth-child(5) > a"
    WIRESHARK_NEWS = "header > nav > ul > li.uk-parent.uk-open > div > ul > li:nth-child(1) > ul > li:nth-child(1) > a"
    WIRESHARK_DOWNLOAD = "header > nav > ul > li.uk-parent.uk-open > div > ul > li:nth-child(1) > ul > li:nth-child(2) > a"
    TCDUMP_EXAMPLES = "header > nav > ul > li.uk-parent.uk-open > div > ul > li:nth-child(2) > ul > li > a"

    FOOTER_TEXT = "body > footer > div > p:nth-child(1)"

    LOGOUT_BUTTON = "[href='/logout']"

    TM_ICON = "header > nav > ul > a"
    HOME_ICON = "header > nav > ul > li:nth-child(2) > a"


class RegPageLocators:

    NAME = "#user_name"
    SURNAME = "#user_surname"
    MIDDLENAME = "#user_middle_name"
    USERNAME = "#username"
    EMAIL = "#email"
    PASSWORD = "#password"
    REPEAT_PASSWORD = "#confirm"
    SDET_CHECKBOX = "#term"
    SUBMIT = "#submit"

    LOG_IN_LINK = "[href='/login']"
