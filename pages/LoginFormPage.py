from locators import LoginForm
from .BasePage import BasePage
from time import sleep


class LoginFormPage(BasePage):

    def user_login(self, email, password):
        sleep(1)
        self._wait_for_clickable(LoginForm.select_email_type)
        self._click(LoginForm.select_email_type)
        self._wait_for_clickable(LoginForm.email_field)
        self._input(LoginForm.email_field, email)
        self._click(LoginForm.email_confirm_btn)
        sleep(1)
        self._wait_for_clickable(LoginForm.password_field)
        self._input(LoginForm.password_field, password)
        self._click(LoginForm.password_confirm_btn)
        sleep(10)

