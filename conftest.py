import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options as FFOptions
from selenium.webdriver.firefox.service import Service as FFService


"""
    def pytest_addoption(parser):
        parser.addoption("--browser", action="store", default="chrome")
    Функція pytest для додавання додаткових параметрів. 
    Всі додані параметри будуть доступні в фікстурі з переданим в неї об'єктом request.
    Наприклад: 
    @pytest.fixture()
    def config(request):
        browser = request.config.getoption("--browser")

"""


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--headless", action="store", default=False)
    parser.addoption("--remote", action="store", default=False)
    parser.addoption("--url", action="store", default="https://prom.ua/ua/")


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture()
def config(request):
    browser = request.config.getoption("--browser")
    url = request.config.getoption("--url")
    headless = False
    remote = False
    if request.config.getoption("--headless"):
        headless = True
    if request.config.getoption("--remote"):
        remote = True

    return {"remote": remote,
            "browser": browser,
            "headless": headless,
            "url": url}


def get_chrome_options(config):
    options = ChromeOptions()
    options.headless = config["headless"]
    return options


def get_firefox_options(config):
    options = FFOptions()
    options.headless = config["headless"]
    return options


def create_remote_driver(config):
    if config["browser"] == "chrome":
        options = get_chrome_options(config)
        options.accept_insecure_certs = True
        options.screenResolution = "1920x1080x24"
    else:
        options = get_firefox_options(config)
        options.accept_insecure_certs = True
        options.screenResolution = "1920x1080x24"
    return webdriver.Remote(command_executor="http://{}:4444/wd/hub".format(config["url"]),
                            options=options)


def create_local_driver(config):
    driver = None
    if config["browser"] == "chrome":
        options = get_chrome_options(config)
        chrome_service = ChromeService(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=chrome_service, options=options)
    elif config["browser"] == "firefox":
        options = get_firefox_options(config)
        firefox_service = FFService(executable_path=GeckoDriverManager().install())
        driver = webdriver.Firefox(service=firefox_service, options=options)
    return driver


@pytest.fixture()
def url(request):
    return request.config.getoption("--url")


@pytest.fixture()
def driver(request, config, url):
    driver = None
    if config["remote"]:
        driver = create_remote_driver(config)
    else:
        driver = create_local_driver(config)
        # driver.maximize_window()
        driver.set_window_size(1920, 1080)

    def tear_down():
        if request.node.rep_call.failed:
            allure.attach(driver.get_screenshot_as_png(), attachment_type=allure.attachment_type.PNG)
        driver.quit()

    request.addfinalizer(tear_down)

    def open(path=""):
        return driver.get(url + path)

    driver.open = open
    driver.open()

    yield driver
