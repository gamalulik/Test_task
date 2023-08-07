from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import unittest

USERNAME_FIELD = 'passp-field-login'
PASSWORD_FIELD = 'passp-field-passwd'
LOGIN_BUTTON = 'passp:sign-in'
ERROR_MESSAGE = 'field:input-passwd:hint'
ERROR_MESSAGE_LOGIN = 'field:input-login:hint'

VALID_USERNAME = 'YOUR_VALID_USERNAME'
VALID_PASSWORD = 'YOUR_VALID_PASSWORD'
INVALID_USERNAME = 'YOUR_INVALID_USERNAME'
INVALID_PASSWORD = 'YOUR_INVALID_PASSWORD'

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def login(self, username, password):
        self.driver.find_element(By.ID, USERNAME_FIELD).send_keys(username)
        self.driver.find_element(By.ID, LOGIN_BUTTON).click()
        try:
            element_present = EC.presence_of_element_located((By.ID, PASSWORD_FIELD))
            WebDriverWait(self.driver, timeout=10).until(element_present)
            self.driver.find_element(By.ID, PASSWORD_FIELD).send_keys(password)
            self.driver.find_element(By.ID, LOGIN_BUTTON).click()

        except TimeoutException:
            print("User does not exist")
            return False

        return True

    def test_case_1_valid_credentials(self):
        self.driver.get('https://passport.yandex.ru/auth/add?origin=dzen&retpath=https%3A%2F%2Fsso.passport.yandex.ru%2Fpush%3Fuuid%3D41c22b8e-1071-4ae0-91c6-de181')
        self.login(VALID_USERNAME, VALID_PASSWORD)

    def test_case_2_invalid_password(self):
        self.driver.get('https://passport.yandex.ru/auth/add?origin=dzen&retpath=https%3A%2F%2Fsso.passport.yandex.ru%2Fpush%3Fuuid%3D41c22b8e-1071-4ae0-91c6-de181')
        if self.login(VALID_USERNAME, INVALID_PASSWORD):
            element_present = EC.presence_of_element_located((By.ID, ERROR_MESSAGE))
            WebDriverWait(self.driver, timeout=10).until(element_present)
            error_message = self.driver.find_element(By.ID, ERROR_MESSAGE).text
            self.assertIn('Неверный пароль', error_message)

    def test_case_3_invalid_username(self):
        self.driver.get('https://passport.yandex.ru/auth/add?origin=dzen&retpath=https%3A%2F%2Fsso.passport.yandex.ru%2Fpush%3Fuuid%3D41c22b8e-1071-4ae0-91c6-de181')
        if self.login(INVALID_USERNAME, VALID_PASSWORD):
            error_message = self.driver.find_element(By.ID, ERROR_MESSAGE).text
            self.assertIn('username is incorrect', error_message)

    def test_case_4_empty_fields(self):
            self.driver.get(
                'https://passport.yandex.ru/auth/add?origin=dzen&retpath=https%3A%2F%2Fsso.passport.yandex.ru%2Fpush%3Fuuid%3D41c22b8e-1071-4ae0-91c6-de181')
            self.driver.find_element(By.ID, LOGIN_BUTTON).click()
            element_present = EC.presence_of_element_located((By.ID, ERROR_MESSAGE_LOGIN))
            WebDriverWait(self.driver, timeout=10).until(element_present)
            error_message = self.driver.find_element(By.ID, ERROR_MESSAGE_LOGIN).text
            self.assertIn('Логин не указан', error_message)

    # Additional test cases...

if __name__ == "__main__":
    unittest.main()
