from pages import HeaderToolbarPage, LoginFormPage, Testdata, SideBarPage
import pickle
import allure


@allure.epic("Authorization cases")
@allure.description('Open sidebar')
def test_user_login(driver):
    with allure.step('Open SideBar'):
        HeaderToolbarPage(driver) \
            .go_to_login_form()
        allure.attach(driver.get_screenshot_as_png(), attachment_type=allure.attachment_type.PNG)
    with allure.step('Open SignIn Page'):
        SideBarPage(driver).user_sign_in()
    with allure.step('Login'):
        LoginFormPage(driver) \
            .user_login(Testdata.email, Testdata.password)

    """"saving cookies in the file 'cookies.pkl' for further authorization"""
    pickle.dump(driver.get_cookies(), open('cookies.pkl', 'wb'))
