from pages import HeaderToolbarPage, LoginFormPage, Testdata
import pickle


def test_user_login(driver):
    HeaderToolbarPage(driver) \
        .go_to_login_form()
    LoginFormPage(driver) \
        .user_login(Testdata.email, Testdata.password)

    """"saving cookies in the file 'cookies.pkl' for further authorization"""
    pickle.dump(driver.get_cookies(), open('cookies.pkl', 'wb'))
