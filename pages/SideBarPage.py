from locators import SideBar
from .BasePage import BasePage
from time import sleep


class SideBarPage(BasePage):
    def user_sign_in(self):
        sleep(1)
        self._wait_for_clickable(SideBar.sign_in_btn)
        return self._click(SideBar.sign_in_btn)
