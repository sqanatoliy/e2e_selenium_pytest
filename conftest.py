import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--browser_ver", action="store", default="")
    parser.addoption("--headless", action="store", default=False)
    parser.addoption("--remote", action="store", default=False)
    parser.addoption("--hub", action="store", default="https://prom.ua/ua/")


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture()
def config(request):
    browser = request.config.getoption("--browser")
    version = request.config.getoption("--browser_ver")
    hub = request.config.getoption("--hub")
    headless = False
    remote = False
    if request.config.getoption("--headless"):
        headless = True
    if request.config.getoption("--remote"):
        remote = True

    return {"remote": remote,
            "version": version,
            "browser": browser,
            "headless": headless,
            "hub": hub}


def get_chrome_options(config):
    options = ChromeOptions()
    options.headless = config["headless"]
    return options


def get_firefox_options(config):
    options = FirefoxOptions()
    options.headless = config["headless"]
    return options


def create_remote_driver(config):
    if config["browser"] == "chrome":
        options = get_chrome_options(config)
        options.browser_version = config["version"]
        options.accept_insecure_certs = True
        options.screenResolution = "1920x1080x24"
    else:
        options = get_firefox_options(config)
        options.browser_version = config["version"]
        options.accept_insecure_certs = True
        options.screenResolution = "1920x1080x24"
    return webdriver.Remote(command_executor="http://{}:4444/wd/hub".format(config["hub"]),
                            options=options)


def create_local_driver(config):
    driver = None
    if config["browser"] == "chrome":
        options = get_chrome_options(config)
        # service = Service(executable_path='C:\\chromedriver\\chromedriver.exe')
        driver = webdriver.Chrome(options=options)
    elif config["browser"] == "firefox":
        options = get_firefox_options(config)
        service = Service(executable_path=GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
    return driver


@pytest.fixture()
def url(request):
    return request.config.getoption("--hub")


@pytest.fixture()
def driver(request, config, url):
    driver = None
    if config["remote"]:
        driver = create_remote_driver(config)
    else:
        driver = create_local_driver(config)
        driver.maximize_window()

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
