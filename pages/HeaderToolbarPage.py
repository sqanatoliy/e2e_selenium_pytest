from locators import HeaderToolbar
from .BasePage import BasePage
from time import sleep


class HeaderToolbarPage(BasePage):

    def go_to_login_form(self):
        sleep(1)
        self._wait_for_clickable(HeaderToolbar.login_btn)
        return self._click(HeaderToolbar.login_btn)
